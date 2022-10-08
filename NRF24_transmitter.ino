#include <SPI.h>
// #include <nRF24L01.h>
#include <RF24.h>

RF24 radio(7, 8); // CE, CSN

const byte address[6] = "00001"; // need 2 for bidirectional communication

void setup() {
  radio.begin();
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_MAX); // set power level - available power levels are MIN, LOW, HIGH, and MAX
  radio.setDataRate(RF24_250KBPS); // 250 kpbs or 1000 kpbs or 2000 kpbs - lowest possible data rate + highest power = longest range
  radio.stopListening(); // because not using bidirectional communication, just sending
}

void loop() {
  const char text[] = "Signal Available";
  radio.write(&text, sizeof(text));
  delay(1000); // wait 1 second
}
