# main.py - API de Processamento Raster com FastAPI

import os
import json
import uuid
import numpy as np
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import rasterio
from rasterio.io import MemoryFile
from rasterio.features import shapes
from shapely.geometry import shape, mapping, Polygon
from shapely.ops import unary_union
import geopandas as gpd
from pydantic import BaseModel
import asyncio
import aiofiles
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializa FastAPI
app = FastAPI(
    title="Raster OS - API de Processamento Geoespacial",
    description="Sistema de inteligência territorial para comparação de matrizes raster",
    version="1.0.0"
)

# Configura CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique o domínio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Diretório para arquivos temporários
TEMP_DIR = "temp_uploads"
os.makedirs(TEMP_DIR, exist_ok=True)

# Modelos de resposta
class ProcessResponse(BaseModel):
    task_id: str
    status: str
    message: str
    bounds: Optional[Dict[str, float]] = None
    changed_areas: Optional[List[Dict[str, Any]]] = None
    stats: Optional[Dict[str, Any]] = None

class TaskStatus(BaseModel):
    task_id: str
    status: str
    progress: int
    result: Optional[Dict[str, Any]] = None

# =============================================
# FUNÇÕES DE PROCESSAMENTO RASTER
# =============================================

def calculate_threshold(data: np.ndarray, threshold: float = 0.3) -> np.ndarray:
    """
    Calcula máscara binária baseada em limiar
    
    Args:
        data: Array numpy com dados do raster
        threshold: Limiar de alteração (0.0 a 1.0)
    
    Returns:
        Máscara binária (0 ou 1)
    """
    # Normaliza dados entre 0 e 1
    data_min = data.min()
    data_max = data.max()
    
    if data_max - data_min == 0:
        return np.zeros_like(data, dtype=np.uint8)
    
    data_norm = (data - data_min) / (data_max - data_min)
    
    # Aplica limiar
    mask = (data_norm > threshold).astype(np.uint8)
    
    return mask

def detect_changes(raster_path: str, threshold: float = 0.3) -> Dict[str, Any]:
    """
    Detecta mudanças em um arquivo raster
    
    Args:
        raster_path: Caminho para o arquivo GeoTIFF
        threshold: Limiar de detecção
    
    Returns:
        Dicionário com resultados do processamento
    """
    with rasterio.open(raster_path) as src:
        # Lê a primeira banda
        band = src.read(1)
        
        # Calcula estatísticas básicas
        stats = {
            "min": float(band.min()),
            "max": float(band.max()),
            "mean": float(band.mean()),
            "std": float(band.std()),
            "shape": band.shape
        }
        
        # Aplica threshold
        mask = calculate_threshold(band, threshold)
        
        # Converte máscara para polígonos
        results = []
        polygons = []
        
        for geom, value in shapes(mask.astype(np.uint8), mask=mask, transform=src.transform):
            if value == 1:  # Apenas áreas de mudança
                poly = shape(geom)
                # Simplifica polígono para reduzir número de vértices
                if poly.area > 0:
                    simplified = poly.simplify(tolerance=0.0001, preserve_topology=True)
                    polygons.append(simplified)
                    
                    # Obtém bounds do polígono
                    bounds = poly.bounds
                    results.append({
                        "type": "Feature",
                        "geometry": mapping(simplified),
                        "properties": {
                            "area": poly.area,
                            "bounds": {
                                "minx": bounds[0],
                                "miny": bounds[1],
                                "maxx": bounds[2],
                                "maxy": bounds[3]
                            },
                            "change_intensity": float(band[int(poly.centroid.y), int(poly.centroid.x)]) if 0 <= int(poly.centroid.y) < band.shape[0] and 0 <= int(poly.centroid.x) < band.shape[1] else 0
                        }
                    })
        
        # Calcula bounds gerais
        if polygons:
            combined = unary_union(polygons)
            total_bounds = combined.bounds
        else:
            total_bounds = src.bounds
        
        return {
            "features": results,
            "bounds": {
                "minx": float(total_bounds[0]),
                "miny": float(total_bounds[1]),
                "maxx": float(total_bounds[2]),
                "maxy": float(total_bounds[3])
            },
            "stats": stats,
            "changed_areas_count": len(results),
            "changed_area_total": float(sum(p.area for p in polygons)) if polygons else 0,
            "original_bounds": {
                "minx": float(src.bounds.left),
                "miny": float(src.bounds.bottom),
                "maxx": float(src.bounds.right),
                "maxy": float(src.bounds.top)
            }
        }

# =============================================
# ENDPOINTS DA API
# =============================================

@app.get("/")
async def root():
    """Endpoint raiz com informações da API"""
    return {
        "name": "Raster OS API",
        "version": "1.0.0",
        "endpoints": {
            "/process-raster": "POST - Processa arquivo GeoTIFF e detecta mudanças",
            "/task/{task_id}": "GET - Verifica status de processamento",
            "/health": "GET - Verifica saúde do servidor"
        }
    }

@app.get("/health")
async def health_check():
    """Verifica saúde do servidor"""
    return {
        "status": "healthy",
        "timestamp": str(np.datetime64('now'))
    }

@app.post("/process-raster", response_model=ProcessResponse)
async def process_raster(
    file: UploadFile = File(...),
    threshold: float = 0.3,
    background_tasks: BackgroundTasks = None
):
    """
    Processa arquivo GeoTIFF e detecta áreas de mudança
    
    Args:
        file: Arquivo GeoTIFF para processamento
        threshold: Limiar de detecção (0.0 a 1.0)
    
    Returns:
        JSON com resultados do processamento
    """
    # Validações
    if not file.filename.endswith(('.tif', '.tiff', '.geotiff', '.GeoTIFF')):
        raise HTTPException(status_code=400, detail="Arquivo deve ser GeoTIFF (.tif)")
    
    if not 0 <= threshold <= 1:
        raise HTTPException(status_code=400, detail="Threshold deve estar entre 0 e 1")
    
    # Gera ID único para a tarefa
    task_id = str(uuid.uuid4())
    temp_path = os.path.join(TEMP_DIR, f"{task_id}_{file.filename}")
    
    try:
        # Salva arquivo temporariamente
        async with aiofiles.open(temp_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        logger.info(f"Arquivo salvo: {temp_path}, tamanho: {len(content)} bytes")
        
        # Processa raster
        result = detect_changes(temp_path, threshold)
        
        # Remove arquivo temporário após processamento
        if background_tasks:
            background_tasks.add_task(os.remove, temp_path)
        
        return ProcessResponse(
            task_id=task_id,
            status="completed",
            message=f"Processamento concluído. {result['changed_areas_count']} áreas de mudança detectadas.",
            bounds=result["bounds"],
            changed_areas=result["features"],
            stats=result["stats"]
        )
        
    except Exception as e:
        logger.error(f"Erro no processamento: {str(e)}")
        # Limpa arquivo em caso de erro
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=f"Erro no processamento: {str(e)}")

@app.post("/process-raster-multi")
async def process_raster_multi(
    files: List[UploadFile] = File(...),
    threshold: float = 0.3
):
    """
    Processa múltiplos arquivos GeoTIFF simultaneamente
    """
    results = []
    
    for file in files:
        try:
            temp_path = os.path.join(TEMP_DIR, f"multi_{uuid.uuid4()}_{file.filename}")
            
            async with aiofiles.open(temp_path, 'wb') as f:
                content = await file.read()
                await f.write(content)
            
            result = detect_changes(temp_path, threshold)
            results.append({
                "filename": file.filename,
                "result": result
            })
            
            os.remove(temp_path)
            
        except Exception as e:
            results.append({
                "filename": file.filename,
                "error": str(e)
            })
    
    return {
        "task_id": str(uuid.uuid4()),
        "status": "completed",
        "results": results
    }

@app.get("/task/{task_id}")
async def get_task_status(task_id: str):
    """
    Verifica status de uma tarefa de processamento
    (Útil para processamentos longos)
    """
    # Em uma implementação real, consultaria um banco de dados
    return TaskStatus(
        task_id=task_id,
        status="completed",
        progress=100,
        result={"message": "Processamento concluído"}
    )

@app.delete("/cleanup")
async def cleanup_temp():
    """
    Limpa todos os arquivos temporários
    """
    count = 0
    for filename in os.listdir(TEMP_DIR):
        file_path = os.path.join(TEMP_DIR, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                count += 1
        except Exception as e:
            logger.error(f"Erro ao remover {file_path}: {e}")
    
    return {"message": f"Limpeza concluída", "files_removed": count}

# =============================================
# CONFIGURAÇÃO PARA EXECUÇÃO
# =============================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
