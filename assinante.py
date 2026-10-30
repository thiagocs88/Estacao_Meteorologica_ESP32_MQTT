#{"temperatura": 24.5, "umidade": 62.0, "luminosidade_pct": 75}



# Programa assinante.py

import paho.mqtt.client as mqtt
import json
import os
from datetime import datetime

# Configurações de Conexão com o Servidor Padrão
MQTT_BROKER = "mqtt-dashboard.com"
MQTT_PORT = 1883
MQTT_TOPIC = "prof_thiago/unip/pd2/thiago/dados" # ⚠️ AJUSTE AQUI O NÚMERO DO SEU GRUPO
CSV_FILE = "dados_estacao_2.csv"

# Cria o arquivo de dados com o cabeçalho se ele não existir
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w") as f:
        f.write("data_hora,temperatura,umidade,luminosidade_pct\n")

def on_connect(client, userdata, flags, rc):
    print(f"📡 Conectado com sucesso! Escutando: {MQTT_TOPIC}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    dados = json.loads(msg.payload.decode())
    data_hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    # Organiza em formato CSV
    nova_linha = f"{data_hora_atual},{dados['temperatura']},{dados['umidade']},{dados['luminosidade_pct']}\n"
    
    with open(CSV_FILE, "a") as f:
        f.write(nova_linha)
        
    print(f"📥 [Nova Leitura Gravada]: {nova_linha.strip()}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
