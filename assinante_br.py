import paho.mqtt.client as mqtt
import json
import os
# Adicionamos timezone e timedelta na importação
from datetime import datetime, timezone, timedelta 

MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "prof_thiago/unip/pd2/thiago/dados"
CSV_FILE = "dados_estacao_3.csv"

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w") as f:
        f.write("data_hora,temperatura,umidade,luminosidade_pct\n")

def on_connect(client, userdata, flags, rc):
    print(f"📡 Conectado com sucesso! Escutando: {MQTT_TOPIC}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        dados = json.loads(msg.payload.decode())
        
        # 1. Configura o fuso horário de Brasília (UTC-3)
        fuso_br = timezone(timedelta(hours=-3))
        
        # 2. Pega a hora local do fuso e inclui os segundos (%S)
        data_hora_atual = datetime.now(fuso_br).strftime("%d/%m/%Y %H:%M:%S")
        
        nova_linha = f"{data_hora_atual},{dados['temperatura']},{dados['umidade']},{dados['luminosidade_pct']}\n"
        
        with open(CSV_FILE, "a") as f:
            f.write(nova_linha)
            
        print(f"📥 [Nova Leitura Gravada]: {nova_linha.strip()}")
        
    except Exception as e:
        print(f"⚠️ Erro ao processar mensagem: {e}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()