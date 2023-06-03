# GaismuPults
Tālvadības gaismu pults uz arduino pamata izmantojot DMX512 standartu
Projekts ir izveidots ar mērķi padarīt skatuves apgaismošanu maksimāli lētu, ērtu un praktisku.
Darbs atrodas izstrādes processā un ikdienā tiek uzlabots.

## Nepieciešamā programmatūra
Python 3.9 vai augstāka
Arduino IDE

## instalācija
```bash
pip  install -r requirements.txt
```
## Programmas startēšana
```bash
python DesktopKivyApp/App.py
```
# Pults konstruēšana
## nepieciešamie mikrokontrolieri un detaļas
Jebkurš Esp8266 mikrokontrolieris
Arduino Uno Rev3
Arduino Nano
Arduino Uno Ethernet Shield Rev3

2 DMX/XLR 3 pin female connector
max485 rs485 transceiver circuit module

## Instalācija
Arduino IDE vidē jāinstalē esp8266 papildinājumu
[instrukcija](https://randomnerdtutorials.com/how-to-install-esp8266-board-arduino-ide/)

Pieslēgt nepieciešamos mikrokontrolierus pie datora, un Arduino IDE vidē izvēlēties jauno COM portu, un uzinstalēt katram mikrokontrolierim atbilstošo kodu no direktorijas [hardware](https://github.com/Hlebusek/GaismuPults/blob/main/hardware/)

[instrukcija](https://support.arduino.cc/hc/en-us/articles/4733418441116-Upload-a-sketch-in-Arduino-IDE)

Pēc dotā attēla savienot mikrokontrolierus 
![](https://github.com/Hlebusek/GaismuPults/blob/main/Wiring.png?raw=true)



