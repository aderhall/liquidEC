#include <SPI.h>
// #include <nRF24L01.h>
#include <RF24.h>

#define LED_PIN 4
RF24 radio(7, 8); // CE, CSN
const byte address[6] = "00001";

void setup() {
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(9600); // 
  radio.begin();
  radio.openReadingPipe(0, address); // initializes reading pipe
  radio.setPALevel(RF24_PA_MAX);
  radio.setDataRate(RF24_250KBPS);
  radio.startListening();
}

void loop() {
  if (radio.available()) {
    char text[32] = "";
    radio.read(&text, sizeof(text));
    Serial.println(text);
    digitalWrite(LED_PIN, HIGH);
    delay(500);
    digitalWrite(LED_PIN, LOW); // if signal is transmitting, LED should turn on for 0.5 seconds every 1 second
    Serial.println("No Signal");
    digitalWrite(LED_PIN, LOW);
    delay(500);
  }
  else{
    
  }
}
