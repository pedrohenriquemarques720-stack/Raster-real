// script.js - Lógica do frontend

// =============================================
// VARIÁVEIS GLOBAIS
// =============================================
let socket = null;
let connected = false;
let rpmChart, tempChart, oscilloscope;
let rpmData = [];
let tempData = [];
let timeData = [];
let oscData = [[], [], []];
let oscRunning = false;

// =============================================
// INICIALIZAÇÃO
// =============================================
document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
    initializeWebSocket();
    loadDevices();
    startUptimeCounter();
});

// =============================================
// WEBSOCKET PARA DADOS EM TEMPO REAL
// =============================================
function initializeWebSocket() {
    // Conecta ao backend Streamlit/WebSocket
    socket = new WebSocket('ws://localhost:8501/ws');
    
    socket.onopen = function() {
        addLog('✅ Conectado ao servidor');
    };
    
    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        updateDashboard(data);
    };
    
    socket.onclose = function() {
        addLog('❌ Desconectado do servidor');
        setTimeout(initializeWebSocket, 3000);
    };
}

// =============================================
// GRÁFICOS
// =============================================
function initializeCharts() {
    // Gráfico de RPM
    const rpmCtx = document.getElementById('rpmChart').getContext('2d');
    rpmChart = new Chart(rpmCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'RPM',
                data: [],
                borderColor: '#ff6600',
                backgroundColor: 'rgba(255,102,0,0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: false,
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: '#2e343f' },
                    ticks: { color: '#9aa4b8' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#9aa4b8' }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });

    // Gráfico de Temperatura
    const tempCtx = document.getElementById('tempChart').getContext('2d');
    tempChart = new Chart(tempCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Temperatura °C',
                data: [],
                borderColor: '#ff3333',
                backgroundColor: 'rgba(255,51,51,0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: false,
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: '#2e343f' },
                    ticks: { color: '#9aa4b8' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#9aa4b8' }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });

    // Osciloscópio
    const oscCtx = document.getElementById('oscilloscope').getContext('2d');
    oscilloscope = new Chart(oscCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'CH1',
                    data: [],
                    borderColor: '#ffff00',
                    borderWidth: 1,
                    pointRadius: 0,
                    tension: 0.1
                },
                {
                    label: 'CH2',
                    data: [],
                    borderColor: '#00ffff',
                    borderWidth: 1,
                    pointRadius: 0,
                    tension: 0.1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: false,
            scales: {
                y: {
                    beginAtZero: false,
                    grid: { color: '#2e343f' }
                },
                x: {
                    display: false
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}

// =============================================
// ATUALIZAÇÃO DO DASHBOARD
// =============================================
function updateDashboard(data) {
    // Atualiza medidores
    document.getElementById('rpmValue').textContent = data.rpm || 0;
    document.getElementById('speedValue').textContent = data.speed || 0;
    document.getElementById('tempValue').textContent = data.temp || 0;
    document.getElementById('batteryValue').textContent = (data.battery || 0).toFixed(1);
    
    // Atualiza barras
    document.getElementById('rpmBar').style.width = ((data.rpm || 0) / 8000 * 100) + '%';
    document.getElementById('speedBar').style.width = ((data.speed || 0) / 200 * 100) + '%';
    document.getElementById('tempBar').style.width = ((data.temp || 0) / 120 * 100) + '%';
    document.getElementById('batteryBar').style.width = ((data.battery || 0) / 15 * 100) + '%';
    
    // Atualiza dados do veículo
    if (data.vehicle) {
        document.getElementById('manufacturer').textContent = data.vehicle.manufacturer || '---';
        document.getElementById('model').textContent = data.vehicle.model || '---';
        document.getElementById('year').textContent = data.vehicle.year || '---';
        document.getElementById('engine').textContent = data.vehicle.engine || '---';
        document.getElementById('ecu').textContent = data.vehicle.ecu || '---';
    }
    
    // Atualiza gráficos
    if (data.rpm) {
        rpmData.push(data.rpm);
        if (rpmData.length > 60) rpmData.shift();
        
        timeData.push(new Date().toLocaleTimeString());
        if (timeData.length > 60) timeData.shift();
        
        rpmChart.data.labels = timeData;
        rpmChart.data.datasets[0].data = rpmData;
        rpmChart.update();
    }
    
    if (data.temp) {
        tempData.push(data.temp);
        if (tempData.length > 60) tempData.shift();
        
        tempChart.data.labels = timeData;
        tempChart.data.datasets[0].data = tempData;
        tempChart.update();
    }
    
    // Atualiza tabela de dados
    updateEngineData(data);
    
    // Atualiza dados em tempo real
    updateLiveData(data);
}

// =============================================
// TABELA DE DADOS DO MOTOR
// =============================================
function updateEngineData(data) {
    const params = [
        { name: 'Pressão do Óleo', value: data.oilPressure || 0, unit: 'bar', status: 'Normal' },
        { name: 'Carga do Motor', value: data.engineLoad || 0, unit: '%', status: 'Normal' },
        { name: 'Temperatura do Ar', value: data.intakeTemp || 0, unit: '°C', status: 'Normal' },
        { name: 'Avanço Ignição', value: data.timingAdvance || 0, unit: '°', status: 'Normal' },
        { name: 'Sonda Lambda', value: data.o2Sensor || 0, unit: 'V', status: 'Normal' },
        { name: 'Pressão Combustível', value: data.fuelPressure || 0, unit: 'kPa', status: 'Normal' },
        { name: 'Posição Acelerador', value: data.throttle || 0, unit: '%', status: 'Normal' },
        { name: 'Fluxo de Ar', value: data.maf || 0, unit: 'g/s', status: 'Normal' }
    ];
    
    let html = '';
    params.forEach(p => {
        html += `
            <tr>
                <td>${p.name}</td>
                <td>${p.value}</td>
                <td>${p.unit}</td>
                <td><span class="badge success">${p.status}</span></td>
            </tr>
        `;
    });
    
    document.getElementById('engineDataBody').innerHTML = html;
}

// =============================================
// DADOS EM TEMPO REAL
// =============================================
function updateLiveData(data) {
    const params = [
        { param: 'RPM', value: data.rpm || 0 },
        { param: 'Velocidade', value: (data.speed || 0) + ' km/h' },
        { param: 'Temp. Motor', value: (data.temp || 0) + ' °C' },
        { param: 'Bateria', value: (data.battery || 0).toFixed(1) + ' V' },
        { param: 'Pressão Óleo', value: (data.oilPressure || 0) + ' bar' },
        { param: 'Carga Motor', value: (data.engineLoad || 0) + ' %' },
        { param: 'Sonda Lambda', value: (data.o2Sensor || 0) + ' V' },
        { param: 'Avanço', value: (data.timingAdvance || 0) + ' °' }
    ];
    
    let html = '';
    params.forEach(p => {
        html += `
            <div class="live-item">
                <span class="param">${p.param}:</span>
                <span class="value">${p.value}</span>
            </div>
        `;
    });
    
    document.getElementById('liveData').innerHTML = html;
}

// =============================================
// CÓDIGOS DE FALHA (DTC)
// =============================================
function updateDTCs(dtcs) {
    let html = '';
    dtcs.forEach(dtc => {
        html += `
            <tr>
                <td><span class="dtc-code">${dtc.code}</span></td>
                <td>${dtc.description}</td>
                <td>${dtc.system}</td>
                <td><span class="badge ${dtc.severity}">${dtc.severity}</span></td>
            </tr>
        `;
    });
    
    document.getElementById('dtcBody').innerHTML = html;
}

// =============================================
// OSCILOSCÓPIO
// =============================================
function startOsc() {
    oscRunning = true;
    simulateOscilloscope();
}

function stopOsc() {
    oscRunning = false;
}

function simulateOscilloscope() {
    if (!oscRunning) return;
    
    const points = 100;
    const time = Array.from({length: points}, (_, i) => i);
    
    // Simula ondas senoidais
    const ch1 = Array.from({length: points}, (_, i) => 
        Math.sin(i * 0.2 + Date.now() * 0.01) * 0.5
    );
    
    const ch2 = Array.from({length: points}, (_, i) => 
        Math.sin(i * 0.1 + Date.now() * 0.02) * 5 + 7
    );
    
    oscilloscope.data.labels = time;
    oscilloscope.data.datasets[0].data = ch1;
    oscilloscope.data.datasets[1].data = ch2;
    oscilloscope.update();
    
    setTimeout(simulateOscilloscope, 50);
}

// =============================================
// AÇÕES DO USUÁRIO
// =============================================
function scanVehicle() {
    addLog('🔍 Escaneando veículo...');
    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({action: 'scan'}));
    }
}

function readDTC() {
    addLog('⚠️ Lendo códigos de falha...');
    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({action: 'read_dtc'}));
    }
}

function clearDTC() {
    if (confirm('Tem certeza que deseja limpar os códigos de falha?')) {
        addLog('✅ Limpando códigos de falha...');
        if (socket && socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify({action: 'clear_dtc'}));
        }
    }
}

function liveData() {
    addLog('📊 Coletando dados em tempo real...');
    document.querySelector('.main-area').scrollTop = 0;
}

function reprogramECU() {
    if (confirm('⚠️ ATENÇÃO! A reprogramação da ECU pode danificar o veículo se feita incorretamente. Deseja continuar?')) {
        addLog('⚡ Iniciando reprogramação da ECU...');
        if (socket && socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify({action: 'reprogram'}));
        }
    }
}

// =============================================
// CONEXÃO
// =============================================
document.getElementById('connectBtn').addEventListener('click', function() {
    const device = document.getElementById('deviceSelect').value;
    if (!device) {
        alert('Selecione um dispositivo');
        return;
    }
    
    const btn = this;
    if (!connected) {
        btn.innerHTML = '<span>🔌</span> DESCONECTAR';
        btn.style.background = '#ff3d00';
        document.querySelector('.led').classList.add('connected');
        document.getElementById('statusText').textContent = 'Conectado';
        connected = true;
        addLog(`✅ Conectado ao dispositivo ${device}`);
        
        if (socket && socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify({action: 'connect', device: device}));
        }
    } else {
        btn.innerHTML = '<span>🔌</span> CONECTAR';
        btn.style.background = '#ff6600';
        document.querySelector('.led').classList.remove('connected');
        document.getElementById('statusText').textContent = 'Desconectado';
        connected = false;
        addLog('❌ Desconectado');
    }
});

// =============================================
// SELEÇÃO DE DISPOSITIVOS
// =============================================
document.querySelectorAll('.conn-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        document.querySelectorAll('.conn-btn').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        loadDevices(this.dataset.conn);
    });
});

function loadDevices(type = 'bluetooth') {
    const select = document.getElementById('deviceSelect');
    select.innerHTML = '<option value="">Buscando dispositivos...</option>';
    
    // Simula busca de dispositivos
    setTimeout(() => {
        let devices = [];
        if (type === 'bluetooth') {
            devices = [
                'OBDII-BT-001 (ELM327)',
                'OBDII-BT-002 (STN2120)',
                'Scanner Pro BT-01'
            ];
        } else if (type === 'wifi') {
            devices = [
                'OBDII-WiFi-192.168.0.10',
                'OBDII-WiFi-192.168.0.11'
            ];
        } else if (type === 'usb') {
            devices = [
                'COM3 - USB Serial',
                'COM4 - USB Serial',
                '/dev/ttyUSB0'
            ];
        }
        
        let options = '<option value="">Selecione o dispositivo...</option>';
        devices.forEach(d => {
            options += `<option value="${d}">${d}</option>`;
        });
        
        select.innerHTML = options;
        addLog(`📡 ${devices.length} dispositivos encontrados`);
    }, 2000);
}

// =============================================
// LOGS E UTILITÁRIOS
// =============================================
function addLog(message) {
    const logArea = document.getElementById('logArea');
    const time = new Date().toLocaleTimeString();
    logArea.innerHTML = `<span class="log-entry">[${time}] ${message}</span>` + logArea.innerHTML;
    
    // Limita número de logs
    if (logArea.children.length > 10) {
        logArea.removeChild(logArea.lastChild);
    }
}

function startUptimeCounter() {
    let seconds = 0;
    setInterval(() => {
        seconds++;
        const hours = Math.floor(seconds / 3600);
        const mins = Math.floor((seconds % 3600) / 60);
        const secs = seconds % 60;
        document.getElementById('uptime').textContent = 
            `${hours.toString().padStart(2,'0')}:${mins.toString().padStart(2,'0')}:${secs.toString().padStart(2,'0')}`;
    }, 1000);
}

// =============================================
// SIMULAÇÃO DE DADOS (para testes sem hardware)
// =============================================
setInterval(() => {
    if (!connected) return;
    
    const mockData = {
        rpm: Math.floor(Math.random() * 3000) + 750,
        speed: Math.floor(Math.random() * 80),
        temp: Math.floor(Math.random() * 20) + 80,
        battery: 12 + Math.random() * 2,
        oilPressure: 3 + Math.random() * 2,
        engineLoad: Math.floor(Math.random() * 40) + 20,
        intakeTemp: Math.floor(Math.random() * 15) + 25,
        timingAdvance: Math.floor(Math.random() * 20) + 5,
        o2Sensor: 0.7 + Math.random() * 0.2,
        fuelPressure: 350 + Math.random() * 50,
        throttle: Math.floor(Math.random() * 30) + 10,
        maf: 5 + Math.random() * 10
    };
    
    updateDashboard(mockData);
}, 500);