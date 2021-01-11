#include "SR04.h"

#define TRIG_PIN 5
#define ECHO_PIN 6
#define LED_YLW 10
#define LED_RED 11
SR04 sr04 = SR04(ECHO_PIN,TRIG_PIN);
long a;

int i = 0;
int mode = 0;

void setup() {
   Serial.begin(9600);
   pinMode(LED_YLW, OUTPUT);
   pinMode(LED_RED, OUTPUT);
   
   digitalWrite(LED_YLW, HIGH);
   digitalWrite(LED_RED, HIGH);
   
   delay(1000);

   digitalWrite(LED_YLW, LOW);
   digitalWrite(LED_RED, LOW);
}

void loop() {
   a=sr04.Distance();
   Serial.print(a);
   Serial.println("cm");

   int msg = Serial.read();
   Serial.read();
   if (msg != -1) {
    mode = msg - 48;
    Serial.println(msg);
   }
   
   switch (mode) {
    case 1:
      digitalWrite(LED_YLW, HIGH);
      digitalWrite(LED_RED, LOW);
      break;
    case 2:
      digitalWrite(LED_YLW, HIGH);
      digitalWrite(LED_RED, HIGH);
      break;
    default:
      digitalWrite(LED_YLW, LOW);
      digitalWrite(LED_RED, LOW);
      break;
   }
   
   delay(5000);
   digitalWrite(LED_RED, LOW);
}
