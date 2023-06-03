#include <DmxSimple.h>




void setup() {
  Serial.begin(9600);
  DmxSimple.usePin(3); 


}

int value = 0;
int channel = 1;
int group = 2;

void loop() {
  int c;

  while (!Serial.available());
  c = Serial.read();
  if ((c >= '0') && (c <= '9')) {
    value = 10 * value + c - '0';
  } else {
    if (c == 'c') channel = value;
    else if (c == 'g') group = value;
    else if (c == 'v') {
      if (group = 2){
        DmxSimple.write(channel, value);
      }


    }
    value = 0;
  }
}