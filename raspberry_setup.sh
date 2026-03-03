#!/bin/bash
# raspberry_setup.sh - Configuração automática do Raspberry Pi 4

echo "🔧 RASTHER JPO - Configuração do Raspberry Pi 4"
echo "================================================"

# Atualizar sistema
echo "📦 Atualizando sistema..."
sudo apt update && sudo apt upgrade -y

# Instalar dependências
echo "📦 Instalando dependências..."
sudo apt install -y python3-pip python3-venv git \
    can-utils python3-serial python3-numpy \
    python3-pandas python3-matplotlib

# Habilitar SPI (para módulo CAN)
echo "🔌 Configurando SPI..."
sudo raspi-config nonint do_spi 0

# Configurar módulo CAN
echo "🔧 Configurando módulo CAN..."
echo "dtoverlay=mcp2515-can0,oscillator=16000000,interrupt=25" | sudo tee -a /boot/config.txt
echo "dtoverlay=spi-bcm2835-overlay" | sudo tee -a /boot/config.txt

# Criar ambiente virtual
echo "🐍 Criando ambiente virtual..."
python3 -m venv ~/rasther_env
source ~/rasther_env/bin/activate

# Instalar pacotes Python
echo "📦 Instalando pacotes Python..."
pip install streamlit pandas numpy python-can obd pyserial

# Criar diretório do projeto
echo "📁 Criando diretório do projeto..."
mkdir -p ~/rasther_jpo/{core,hardware,database}

# Configurar inicialização automática
echo "🚀 Configurando inicialização automática..."
cat > ~/.config/lxsession/LXDE-pi/autostart << EOF
@lxterminal -e bash -c "cd /home/pi/rasther_jpo && source ~/rasther_env/bin/activate && streamlit run app.py --server.port 8501 --server.address 0.0.0.0"
EOF

# Criar serviço systemd (opcional)
echo "⚙️ Criando serviço systemd..."
sudo bash -c 'cat > /etc/systemd/system/rasther.service << EOF
[Unit]
Description=RASTHER JPO Scanner
After=network.target

[Service]
ExecStart=/bin/bash -c "cd /home/pi/rasther_jpo && source /home/pi/rasther_env/bin/activate && streamlit run app.py --server.port 8501 --server.address 0.0.0.0"
User=pi
Restart=always

[Install]
WantedBy=multi-user.target
EOF'

sudo systemctl enable rasther.service

echo "✅ Configuração concluída!"
echo "Reinicie o Raspberry Pi para aplicar as mudanças."
