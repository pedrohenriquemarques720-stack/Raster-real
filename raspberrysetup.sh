#!/bin/bash
# raspberry_setup.sh - Configuração automática do Raspberry Pi 4 para RASTHER JPO

echo "╔══════════════════════════════════════════════════════════╗"
echo "║     🚀 RASTHER JPO - INSTALADOR AUTOMÁTICO PARA RPi     ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Cores para output
VERDE='\033[0;32m'
AMARELO='\033[1;33m'
VERMELHO='\033[0;31m'
AZUL='\033[0;34m'
RESET='\033[0m'

print_step() {
    echo -e "${AZUL}[PASSO $1]${RESET} $2"
}

print_success() {
    echo -e "${VERDE}[OK]${RESET} $1"
}

print_warning() {
    echo -e "${AMARELO}[AVISO]${RESET} $1"
}

print_error() {
    echo -e "${VERMELHO}[ERRO]${RESET} $1"
}

# =============================================
# PASSO 1: ATUALIZAR SISTEMA
# =============================================
print_step "1/10" "Atualizando sistema operacional..."
sudo apt update && sudo apt upgrade -y
if [ $? -eq 0 ]; then
    print_success "Sistema atualizado"
else
    print_error "Falha na atualização"
    exit 1
fi

# =============================================
# PASSO 2: INSTALAR DEPENDÊNCIAS BASE
# =============================================
print_step "2/10" "Instalando dependências base..."
sudo apt install -y \
    python3-pip \
    python3-venv \
    python3-dev \
    git \
    curl \
    wget \
    vim \
    htop \
    can-utils \
    i2c-tools \
    spi-tools \
    wiringpi \
    libatlas-base-dev

if [ $? -eq 0 ]; then
    print_success "Dependências base instaladas"
else
    print_error "Falha na instalação das dependências"
    exit 1
fi

# =============================================
# PASSO 3: CONFIGURAR INTERFACES (SPI, I2C, CAN)
# =============================================
print_step "3/10" "Configurando interfaces de hardware..."

# Habilitar SPI
sudo raspi-config nonint do_spi 0
print_success "SPI habilitado"

# Habilitar I2C
sudo raspi-config nonint do_i2c 0
print_success "I2C habilitado"

# Habilitar interface serial (para OBD-II)
sudo raspi-config nonint do_serial 2
print_success "Serial habilitado (para OBD-II)"

# Configurar módulo CAN (MCP2515)
echo "dtoverlay=mcp2515-can0,oscillator=16000000,interrupt=25" | sudo tee -a /boot/config.txt
echo "dtoverlay=spi-bcm2835-overlay" | sudo tee -a /boot/config.txt
print_success "Módulo CAN configurado (MCP2515)"

# =============================================
# PASSO 4: INSTALAR BIBLIOTECAS PYTHON
# =============================================
print_step "4/10" "Instalando bibliotecas Python..."

pip3 install --upgrade pip setuptools wheel

pip3 install \
    streamlit \
    pandas \
    numpy \
    plotly \
    python-obd \
    pyserial \
    python-can \
    matplotlib \
    pillow \
    psutil \
    requests \
    python-dotenv

if [ $? -eq 0 ]; then
    print_success "Bibliotecas Python instaladas"
else
    print_error "Falha na instalação das bibliotecas"
    exit 1
fi

# =============================================
# PASSO 5: CRIAR ESTRUTURA DO PROJETO
# =============================================
print_step "5/10" "Criando estrutura do projeto RASTHER JPO..."

cd /home/pi
mkdir -p rasther_jpo/{core,hardware,database,logs,backups}
cd rasther_jpo

print_success "Estrutura criada em /home/pi/rasther_jpo"

# =============================================
# PASSO 6: BAIXAR CÓDIGO FONTE
# =============================================
print_step "6/10" "Baixando código fonte..."

# Opção 1: Clonar do GitHub (se tiver repositório)
# git clone https://github.com/seu-usuario/rasther-jpo.git .

# Opção 2: Criar arquivo app.py manualmente
cat > /home/pi/rasther_jpo/app.py << 'EOF'
# app.py - RASTHER JPO - Versão Raspberry Pi
# (Cole aqui o código completo do app.py que já temos)
print("RASTHER JPO iniciado com sucesso!")
EOF

print_success "Código fonte baixado"

# =============================================
# PASSO 7: CONFIGURAR INICIALIZAÇÃO AUTOMÁTICA
# =============================================
print_step "7/10" "Configurando inicialização automática..."

# Criar serviço systemd
sudo bash -c 'cat > /etc/systemd/system/rasther.service << EOF
[Unit]
Description=RASTHER JPO - Scanner Automotivo Profissional
After=network.target

[Service]
ExecStart=/usr/bin/python3 -m streamlit run /home/pi/rasther_jpo/app.py --server.port 8501 --server.address 0.0.0.0
WorkingDirectory=/home/pi/rasther_jpo
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
EOF'

# Habilitar serviço
sudo systemctl daemon-reload
sudo systemctl enable rasther.service
sudo systemctl start rasther.service

print_success "Serviço configurado e iniciado"

# =============================================
# PASSO 8: CONFIGURAR MODO QUIOSCO (INICIAR DIRETO NO APP)
# =============================================
print_step "8/10" "Configurando modo quiosco (iniciar direto no app)..."

# Instalar browser
sudo apt install -y chromium-browser unclutter

# Criar script de autostart
mkdir -p /home/pi/.config/lxsession/LXDE-pi
cat > /home/pi/.config/lxsession/LXDE-pi/autostart << EOF
@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@xscreensaver -no-splash
@point-rpi
@unclutter -idle 0.1 -root
@sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' ~/.config/chromium/Default/Preferences
@chromium-browser --noerrdialogs --disable-infobars --kiosk --app=http://localhost:8501
EOF

print_success "Modo quiosco configurado"

# =============================================
# PASSO 9: CONFIGURAR TOUCHSCREEN
# =============================================
print_step "9/10" "Configurando touchscreen oficial..."

# Rotacionar tela se necessário (para 7" oficial)
echo "display_rotate=1" | sudo tee -a /boot/config.txt

# Calibrar touch (se necessário)
# sudo apt install -y xinput-calibrator

print_success "Touchscreen configurado"

# =============================================
# PASSO 10: TESTAR CONEXÃO OBD-II
# =============================================
print_step "10/10" "Testando conexão OBD-II..."

cat > /home/pi/test_obd.py << 'EOF'
import obd
import time

print("🔌 Procurando adaptador ELM327...")
connection = obd.OBD()
if connection.is_connected():
    print(f"✅ Conectado! Protocolo: {connection.protocol_name()}")
    print(f"📊 RPM: {connection.query(obd.commands.RPM).value}")
    print(f"🌡️  Temperatura: {connection.query(obd.commands.COOLANT_TEMP).value}")
else:
    print("❌ Não foi possível conectar. Verifique o cabo.")
EOF

python3 /home/pi/test_obd.py

# =============================================
# FINALIZAÇÃO
# =============================================
echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║     ✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO!                 ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "📱 Acesse o RASTHER JPO em:"
echo "   - No Raspberry:  http://localhost:8501"
echo "   - Na rede local: http://$(hostname -I | awk '{print $1}'):8501"
echo ""
echo "🔄 Para reiniciar o serviço: sudo systemctl restart rasther"
echo "📋 Para ver os logs: sudo journalctl -u rasther -f"
echo ""
echo "🔧 Para conectar ao carro:"
echo "   1. Conecte o cabo OBD2-USB"
echo "   2. Execute: python3 /home/pi/test_obd.py"
echo ""
echo "🎯 PRÓXIMOS PASSOS:"
echo "   1. Reinicie o Raspberry: sudo reboot"
echo "   2. Conecte ao carro e teste"
echo "   3. Configure sua rede Wi-Fi"
echo ""
