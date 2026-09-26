#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* serverUrl = "http://YOUR_SERVER_IP:8000/api/sensors/data";

#define SOIL_PIN 34
#define PUMP_PIN 26

void setup() {
  Serial.begin(115200);
  pinMode(PUMP_PIN, OUTPUT);
  digitalWrite(PUMP_PIN, LOW);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    int raw = analogRead(SOIL_PIN);
    float moisture = map(raw, 3200, 1200, 0, 100);
    moisture = constrain(moisture, 0, 100);

    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");
    String payload = "{\"device_id\":\"PLANT-001\",\"soil_moisture\":" + String(moisture) + ",\"temperature\":28.0,\"humidity\":60.0,\"light_level\":75.0}";
    int httpCode = http.POST(payload);
    http.end();
  }
  delay(5000);
}