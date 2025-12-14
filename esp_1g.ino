#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <DHT.h>

const char* ssid = "TP-Link_194B";
const char* password = "46488862";
const char* serverUrl = "http://";

#define DHTPIN 0
#define DHTTYPE DHT11
#define SOIL_PIN A0

DHT dht(DHTPIN, DHTTYPE);
WiFiClient client;
HTTPClient http;

float airTemperature = 0.0;
float airHumidity = 0.0;
int soilMoisture = 0;

String token = "sdkjfhskdhfsk324";
String userId = "1234590";

unsigned long lastSend = 0;
const long sendInterval = 30000;

void setupWiFi() {
  Serial.begin(115200);
  delay(100);
  
  Serial.println();
  Serial.println("Подключение к WiFi...");
  
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("\nWiFi подключен!");
  Serial.print("IP адрес: ");
  Serial.println(WiFi.localIP());
}

void readSensors() {
  airTemperature = dht.readTemperature();
  airHumidity = dht.readHumidity();
  soilMoisture = analogRead(SOIL_PIN);
  
  Serial.print("Температура: ");
  Serial.print(airTemperature);
  Serial.print("°C, Влажность воздуха: ");
  Serial.print(airHumidity);
  Serial.print("%, Почва: ");
  Serial.println(soilMoisture);
}

void setup() {
  setupWiFi();
  dht.begin();
  delay(2000);
  Serial.println("Система готова к работе!");
  Serial.println("==========================");
}

void loop() {
  readSensors();
  
  if (millis() - lastSend >= sendInterval) {
    lastSend = millis();
  }
  
  delay(1000);
}
