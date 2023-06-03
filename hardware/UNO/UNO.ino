#include <SPI.h>
#include <Ethernet.h>
#include <DmxSimple.h>

byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED};

IPAddress ip(192, 168, 1, 177);

EthernetServer server(80);

String GetUrl;
int value = 0;
int channel = 1;
int group = 1;


void setup() {
  DmxSimple.usePin(3); 
  Serial.begin(9600);
  while (!Serial) {
    ; 
  }

  Ethernet.begin(mac, ip);

  if (Ethernet.hardwareStatus() == EthernetNoHardware) {
    while (true) {
      delay(1); 
    }
  }


  server.begin();

}


void loop() {
  EthernetClient client = server.available();
  if (client) {

    boolean currentLineIsBlank = true;

    while (client.connected()) {

      if (client.available()) {

        char c = client.read();
        GetUrl += c;
        if (c == '\n' && currentLineIsBlank) {

          client.println("HTTP/1.1 200 OK");
          client.println("Content-Type: text/html");
          client.println();
          client.println("<!DOCTYPE HTML>");
          client.println("<html>");
          //client.println(GetUrl);
          //client.println("Connection: close");

          if (GetUrl.indexOf("COMMAND") != -1){
            int val = 0;
            for(int i = GetUrl.indexOf("GROUP=") + 6; true; i++){
              val = val * 10 + (GetUrl[i] - '0');
              if(GetUrl[i+1] == '&'){
                group = val;
                val = 0;
                break;
              }
            }

            for(int i = GetUrl.indexOf("CHANNEL=") + 8; true; i++){
              val = val * 10 + (GetUrl[i] - '0');
              if(GetUrl[i+1] == '&'){
                channel = val;
                val = 0;
                break;
              }
            }

            for(int i = GetUrl.indexOf("VALUE=") + 6; true; i++){
              val = val * 10 + (GetUrl[i] - '0');
              if(GetUrl[i+1] == '&'){
                value = val;
                val = 0;
                break;
              }
            }
          }
          client.println(group);
          client.println(channel);
          client.println(value);
          GetUrl = "";
          break;
        }

        if (c == '\n') {
          currentLineIsBlank = true;
        } else if (c != '\r') {
          currentLineIsBlank = false;
        }

      }
    }
    if (group == 1){
      DmxSimple.write(channel, value);
    }
    else{
      Serial.print(group);
      Serial.print("g");
      Serial.print(channel);
      Serial.print("c");
      Serial.print(value);
      Serial.print("v");
    }
    delay(1);
    client.stop();
  
  }

}

