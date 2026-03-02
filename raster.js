// script.js - Funcionalidades interativas

let ctx1, ctx2;
let animationId1, animationId2;
let time = 0;

// =============================================
// INICIALIZAÇÃO
// =============================================
window.onload = function() {
    // Inicializa canvas
    ctx1 = document.getElementById('oscilloscope1').getContext('2d');
    ctx2 = document.getElementById('oscilloscope2').getContext('2d');
    
    // Configura listeners
    setupEventListeners();
    
    // Simula dados iniciais
    simulateOscilloscope();
};

// =============================================
// EVENT LISTENERS
// =============================================
function setupEventListeners() {
    // Botão conectar
    document.getElementById('connectBtn').addEventListener('click', toggleConnection);
    
    // Botões de ação
    document.getElementById('scanBtn').addEventListener('click', scanVehicle);
    document.getElementById('readDTCBtn').addEventListener('click', readDTC);
    document.getElementById('clearDTCBtn').addEventListener('click', clearDTC);
    document.getElementById('liveDataBtn').addEventListener('click', liveData);
    document.getElementById('reprogramBtn').addEventListener('click', reprogramECU);
    
    // Botões iniciar/parar
    document.getElementById('startBtn').addEventListener('click', startAcquisition);
    document.getElementById('stopBtn').addEventListener('click', stopAcquisition);
    
    // Controles do osciloscópio
    document.getElementById('startOsc').addEventListener('click', startOscilloscope);
    document.getElementById('stopOsc').addEventListener('click', stopOscilloscope);
}

// =============================================
// CONEXÃO
// =============================================
function toggleConnection() {
    const btn = document.getElementById('connectBtn');
    const led = btn.querySelector('.led-small');
    
    if (btn.classList.contains('connected')) {
        btn.classList.remove('connected');
        btn.innerHTML = '<span class="led-small"></span> CONECTAR';
        led.style.backgroundColor = '#888';
        updateLog('Desconectado do veículo');
    } else {
        btn.classList.add('connected');
        btn.innerHTML = '<span class="led-small" style="background:#00ff00"></span> DESCONECTAR';
        led.style.backgroundColor = '#00ff00';
        updateLog('Conectado ao veículo - Protocolo CAN 500kbps');
    }
}

// =============================================
// AÇÕES
// =============================================
function scanVehicle() {
    updateLog('🔍 Escaneando veículo...');
    setTimeout(() => {
        document.getElementById('manufacturer').textContent = 'VOLKSWAGEN';
        document.getElementById('model').textContent = 'GOL 1.6 MSI';
        document.getElementById('year').textContent = '2024';
        document.getElementById('engine').textContent = 'EA211 (16V)';
        document.getElementById('vin').textContent = '9BWZZZ377VT004251';
        updateLog('✅ Veículo identificado: VW GOL 1.6 2024');
    }, 2000);
}

function readDTC() {
    updateLog('⚠️ Lendo códigos de falha...');
    setTimeout(() => {
        addHistory('3 códigos de falha encontrados');
        updateLog('✅ P0301, P0420, P0171 detectados');
    }, 1500);
}

function clearDTC() {
    if (confirm('Limpar códigos de falha?')) {
        updateLog('✅ Códigos de falha limpos');
        addHistory('Falhas limpas');
    }
}

function liveData() {
    updateLog('📊 Coletando dados em tempo real');
}

function reprogramECU() {
    if (confirm('⚠️ ATENÇÃO! A reprogramação pode danificar a ECU. Continuar?')) {
        updateLog('⚡ Iniciando reprogramação...');
        let progress = 0;
        const interval = setInterval(() => {
            progress += 10;
            updateLog(`⚡ Reprogramando: ${progress}%`);
            if (progress >= 100) {
                clearInterval(interval);
                updateLog('✅ Reprogramação concluída!');
            }
        }, 500);
    }
}

// =============================================
// OSCILOSCÓPIO
// =============================================
function startOscilloscope() {
    stopOscilloscope();
    animateOscilloscope();
    updateLog('▶️ Osciloscópio iniciado');
}

function stopOscilloscope() {
    if (animationId1) {
        cancelAnimationFrame(animationId1);
        cancelAnimationFrame(animationId2);
    }
    updateLog('⏹️ Osciloscópio parado');
}

function animateOscilloscope() {
    drawChannel1();
    drawChannel2();
}

function drawChannel1() {
    const width = ctx1.canvas.width;
    const height = ctx1.canvas.height;
    
    ctx1.clearRect(0, 0, width, height);
    ctx1.strokeStyle = '#ffff00';
    ctx1.lineWidth = 2;
    ctx1.beginPath();
    
    for (let x = 0; x < width; x++) {
        // Onda senoidal para sensor de detonação
        const y = height/2 + Math.sin(x * 0.02 + time) * 30 + 
                  Math.sin(x * 0.1 + time * 2) * 10;
        
        if (x === 0) {
            ctx1.moveTo(x, y);
        } else {
            ctx1.lineTo(x, y);
        }
    }
    
    ctx1.stroke();
    
    // Atualiza valor
    const value = (0.4 + Math.sin(time) * 0.1).toFixed(2);
    document.getElementById('ch1Value').textContent = value + ' V';
    
    time += 0.1;
    animationId1 = requestAnimationFrame(drawChannel1);
}

function drawChannel2() {
    const width = ctx2.canvas.width;
    const height = ctx2.canvas.height;
    
    ctx2.clearRect(0, 0, width, height);
    ctx2.strokeStyle = '#00ffff';
    ctx2.lineWidth = 2;
    ctx2.beginPath();
    
    for (let x = 0; x < width; x++) {
        // Sinal quadrado para bomba injetora
        const y = height/2 + (Math.sin(x * 0.05 + time * 2) > 0 ? 40 : -40);
        
        if (x === 0) {
            ctx2.moveTo(x, y);
        } else {
            ctx2.lineTo(x, y);
        }
    }
    
    ctx2.stroke();
    
    // Atualiza valor
    const value = (12 + Math.sin(time) * 0.5).toFixed(1);
    document.getElementById('ch2Value').textContent = value + ' V';
    
    animationId2 = requestAnimationFrame(drawChannel2);
}

// =============================================
// INICIAR/PARAR AQUISIÇÃO
// =============================================
function startAcquisition() {
    updateLog('▶️ Iniciando aquisição de dados');
    // Simula atualização de dados
    updateDataInterval = setInterval(updateRealTimeData, 1000);
}

function stopAcquisition() {
    updateLog('⏹️ Aquisição parada');
    if (updateDataInterval) {
        clearInterval(updateDataInterval);
    }
}

function updateRealTimeData() {
    // Simula dados em tempo real
    document.getElementById('rpm').textContent = Math.floor(Math.random() * 1000 + 750);
    document.getElementById('temp').textContent = Math.floor(Math.random() * 20 + 80);
    document.getElementById('voltage').textContent = (12 + Math.random() * 2).toFixed(1);
    document.getElementById('oilPressure').textContent = (3 + Math.random() * 2).toFixed(1);
    document.getElementById('engineLoad').textContent = Math.floor(Math.random() * 30 + 15);
    
    addHistory(`RPM: ${document.getElementById('rpm').textContent}`);
}

// =============================================
// UTILITÁRIOS
// =============================================
function updateLog(message) {
    const logArea = document.getElementById('logArea');
    const time = new Date().toLocaleTimeString();
    logArea.innerHTML = `> [${time}] ${message}`;
}

function addHistory(message) {
    const historyList = document.getElementById('historyList');
    const time = new Date().toLocaleTimeString();
    const newItem = document.createElement('div');
    newItem.className = 'history-item';
    newItem.textContent = `${time} - ${message}`;
    
    historyList.insertBefore(newItem, historyList.firstChild);
    
    // Limita número de itens
    if (historyList.children.length > 10) {
        historyList.removeChild(historyList.lastChild);
    }
}

// =============================================
// ATUALIZAÇÃO PERIÓDICA
// =============================================
setInterval(() => {
    // Atualiza dados a cada 2 segundos se conectado
    const connectBtn = document.getElementById('connectBtn');
    if (connectBtn.classList.contains('connected')) {
        updateRealTimeData();
    }
}, 2000);
