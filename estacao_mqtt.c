#include <WiFi.h>
#include <PubSubClient.h>
#include "DHT.h"

// --- Configurações de Wi-Fi ---
const char* ssid = "iPhone 15 Pro Max do Thiago";
const char* password = "internet";

// --- Configurações de MQTT ---
const char* mqtt_server = "mqtt-dashboard.com";
const int mqtt_port = 1883;
// Substitua NNNNNN pelo número do seu grupo no projeto de PD2
const char* mqtt_topic = "prof_thiago/unip/pd2/thiago/dados"; 

// --- Configurações dos Sensores ---
#define DHTPIN 5     
#define DHTTYPE DHT22   
DHT dht(DHTPIN, DHTTYPE);
#define LDRPIN 32 

// --- Instâncias de Rede ---
WiFiClient espClient;
PubSubClient client(espClient);

// Controle de tempo sem travar o processador (substitui o delay)
unsigned long ultimaMensagem = 0;
const long intervalo = 5000; // Publica a cada 5 segundos

void setup_wifi() {
  Serial.print(F("Conectando a "));
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(F("."));
  }
  Serial.println(F("\nWiFi conectado. IP: "));
  Serial.println(WiFi.localIP());
}

void reconnect() {
  // Entra em loop até reconectar ao broker MQTT
  while (!client.connected()) {
    Serial.print(F("Tentando conexão MQTT..."));
    // Cria um ID de cliente aleatório para evitar conflitos no broker público
    String clientId = "ESP32Client-";
    clientId += String(random(0xffff), HEX);
    
    if (client.connect(clientId.c_str())) {
      Serial.println(F("Conectado!"));
    } else {
      Serial.print(F("Falhou, rc="));
      Serial.print(client.state());
      Serial.println(F(" Tentando novamente em 5 segundos..."));
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  dht.begin();
  
  setup_wifi();
  
  // Configura o endereço e a porta do Broker MQTT
  client.setServer(mqtt_server, mqtt_port);
}

void loop() {
  // Garante que a conexão WiFi/MQTT está ativa
  if (!client.connected()) {
    reconnect();
  }
  client.loop(); // Mantém o processo do MQTT rodando em segundo plano

  unsigned long agora = millis();
  
  // Executa a leitura e publicação apenas a cada intervalo definido
  if (agora - ultimaMensagem >= intervalo) {
    ultimaMensagem = agora;

    float umidade = dht.readHumidity();
    float temperatura = dht.readTemperature();
    int leituraBrutaLDR = analogRead(LDRPIN);
    
    // Calcula a porcentagem mantendo as casas decimais (regra de 3 direta)
    float luminosidade = (leituraBrutaLDR / 4095.0) * 100.0;

    if (isnan(umidade) || isnan(temperatura)) {
      Serial.println(F("Falha ao ler o DHT22!"));
      return;
    }

    // Monta o JSON exato que o Python espera (usando luminosidade_pct)
    String payload = "{";
    payload += "\"temperatura\":" + String(temperatura, 1) + ",";
    payload += "\"umidade\":" + String(umidade, 1) + ",";
    payload += "\"luminosidade_pct\":" + String(luminosidade, 1);
    payload += "}";

    Serial.print(F("Publicando: "));
    Serial.println(payload);
    
    // Envia a mensagem para o tópico
    client.publish(mqtt_topic, payload.c_str());
  }
}