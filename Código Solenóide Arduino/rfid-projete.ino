#include <Arduino.h>
#include <rdm6300.h>

#define RDM6300_RX_PIN 4 // read the SoftwareSerial doc above! may need to change this pin to 10...
#define READ_LED_PIN 13

Rdm6300 rdm6300;

void setup(){
  Serial.begin(115200);
  rdm6300.begin(RDM6300_RX_PIN);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  digitalWrite(2, HIGH);
  digitalWrite(3, HIGH);
}

void loop() {
  byte block;
  byte len;

  if(Serial.available() > 0){
    char command = Serial.read();
    Serial.println(command);
    if(command == 'P'){
      Serial.println("Acionar relé para liberar catraca");
      digitalWrite(2, LOW);
      delay(3500);
      digitalWrite(2, HIGH);
      digitalWrite(3, HIGH);
    }
  }

  if (rdm6300.get_new_tag_id()) {
    uint32_t tagID = rdm6300.get_tag_id();
    
    String rfidData = String(tagID, HEX);
    Serial.println("Número do cartão RFID lido: " + rfidData);
    }
    delay(10);
  }