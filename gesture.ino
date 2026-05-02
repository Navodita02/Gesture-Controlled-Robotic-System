#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include "DataParser.h"

const char* ssid = "Asdf";
const char* password = "12345678";

DataParser dataParser;

WiFiUDP udp;
const int udpPort = 12345;

// Motor driver pins (ESP8266)
int in1 = D1;
int in2 = D2;
int ena = D3;
int in3 = D4;
int in4 = D5;
int enb = D6;

int Speed = 80;
int Right_speed = 0;
int Left_speed = 0;

char incomingPacket[255];  

void setup() {
  Serial.begin(115200);

  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(ena, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  pinMode(enb, OUTPUT);

  WiFi.begin(ssid, password);
  Serial.println("Connecting...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConnected to WiFi");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  udp.begin(udpPort);
  Serial.println("UDP listening...");
}

void loop() {

  int packetSize = udp.parsePacket();
  if (packetSize) {
    int len = udp.read(incomingPacket, 255);
    if (len > 0) incomingPacket[len] = '\0';

    String IncomingData = incomingPacket;
    Serial.print("Received: ");
    Serial.println(IncomingData);

    dataParser.parseData(IncomingData, ',');

    Speed = dataParser.getField(1).toInt();
    Left_speed = Speed;
    Right_speed = Speed;
  }

  String cmd = dataParser.getField(0);

  if (cmd == "f") forward(Left_speed, Right_speed);
  else if (cmd == "b") backward(Left_speed, Right_speed);
  else if (cmd == "l") left(Left_speed, Right_speed);
  else if (cmd == "r") right(Left_speed, Right_speed);
  else if (cmd == "s") Stop();
}

void forward(int ls, int rs) {
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  analogWrite(ena, ls);
  analogWrite(enb, rs);
}

void backward(int ls, int rs) {
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  analogWrite(ena, ls);
  analogWrite(enb, rs);
}

void left(int ls, int rs) {
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  analogWrite(ena, ls);
  analogWrite(enb, rs);
}

void right(int ls, int rs) {
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  analogWrite(ena, ls);
  analogWrite(enb, rs);
}

void Stop() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
  analogWrite(ena, 0);
  analogWrite(enb, 0);
}
