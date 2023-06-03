/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                                                                                                                                                     //
//     V 1.3                                                  THIS SCRIPT WAS MADE BY ReverseGrowth#8225 :'(                                           //
//                                                                                                                                                     //
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <string>

const char* ssid = "GaismuPultsBuiltIn"; 
const char* password = "12345678"; 

IPAddress local_ip(192,168,1,177);
IPAddress gateway(192,168,1,1);
IPAddress subnet(255,255,255,0);

ESP8266WebServer server(80);

///// comunication values
int group = 1;
int channel = 1;
int value = 0;

/////////////////////////
bool NewDataFlag = false;
bool Switch = false;
int SwitchPin = 5;

/////////////////////////
void setup() {

  Serial.begin(9600);
  WiFi.softAP(ssid, password);
  WiFi.softAPConfig(local_ip, gateway, subnet);
  delay(100);

  /////// handling requests on =>
  server.on("/", handle_OnConnect);
  server.on("/COMMAND", GetCommand);
  server.on("/s", SwitchCheck); ////// DEBUG
  server.on("/SHOWUP", ShowUp)
  /////// handling unknown requests 
  server.onNotFound(handle_NotFound);

  /////////////////////////

  // Starting WebServer
  server.begin();
}

void loop() {
  // Make server do things.... :)
  server.handleClient();

  // Send Data
  if (NewDataFlag == true){
    Serial.print(String(group) + "g" + String(channel)  + "c" + String(value) + "v" + "\n")
    NewDataFlag = false;
  }
}

void GetCommand(){

  // Reading all request's arguments
  for (int i = 0; i < server.args(); i++) { 

    if (server.argName(i) == "GROUP"){
        group = server.arg(i).toInt();
    } 
    else if (server.argName(i) == "CHANNEL"){      
        channel = server.arg(i).toInt();
    }
    else if (server.argName(i) == "VALUE"){
        value = server.arg(i).toInt();
    }
    
  } 
  NewData = true;
  server.send(200, "text/html", "command completed!  g" + String(group) + "   c" + String(channel) + "   v" + String(value) + String(Switch)); 
}

void handle_OnConnect() {
  server.send(200, "text/html", "There is nothing yet"); 
}

void handle_NotFound(){
  server.send(200, "text/html", "Is this what you are looking for?"); 
}

void SwitchCheck(){ ////// DEBUG
  server.send(200,"text/html",String(digitalRead(4)));
}

void ShowUp(){
  server.send(200,"text/html","<|!|>\nVERSION > 1.3\n MODULE > ESP");
}



