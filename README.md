# GaismuPults
Tālvadības gaismu pults uz arduino pamata izmantojot DMX512 standartu.

Projekts ir izveidots ar mērķi padarīt skatuves apgaismošanu maksimāli lētu, ērtu un praktisku.

Darbs atrodas izstrādes procesā un ikdienā tiek uzlabots.

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
Jebkurš Esp8266 mikrokontrolieris,
Arduino Uno Rev3,
Arduino Nano,
Arduino Uno Ethernet Shield Rev3,

2 DMX/XLR 3 pin female connector,
max485 rs485 transceiver circuit module

## Instalācija
Arduino IDE vidē jāinstalē esp8266 papildinājumu
[instrukcija](https://randomnerdtutorials.com/how-to-install-esp8266-board-arduino-ide/)

Pieslēgt nepieciešamos mikrokontrolierus pie datora, un Arduino IDE vidē izvēlēties jauno COM portu, un uzinstalēt katram mikrokontrolierim atbilstošo kodu no direktorijas [hardware](https://github.com/Hlebusek/GaismuPults/blob/main/hardware/)

[instrukcija](https://support.arduino.cc/hc/en-us/articles/4733418441116-Upload-a-sketch-in-Arduino-IDE)

Mikrokontrolieri ir savienoti šādā slēgumā

<img src="https://github.com/Hlebusek/GaismuPults/blob/main/images/Wiring.png?raw=true" width=40% height=40%>



# Programmas lietošana
<img src="https://github.com/Hlebusek/GaismuPults/blob/main/images/AppMain.png?raw=true" width=50% height=50%>

## Pamatfunkcijas 
1. Saglabāt uzstādītās gaismas/gaismu vērtības
2. Visi saglabāto vērtību ieraksti
3. Saglabāt visu gaismu adrešu konfigurāciju
4. Importēt gaismu adrešu konfigurāciju 
5. Uzstādīt visu gaismu vērtības uz 0, jeb izslēgt visas gaismas
6. Izveidot jaunu gaismu (ierīci), uzstādot vērtību adreses
7. Visas 1. DMX universe adreses
8. Visas 2. DMX universe adreses
9. Uzstādīt izvēlētajai adresei maksimālo vērtību
10. Uzstādīt izvēlētajai adresei vērtību
11. Pārslēgt adrešu lapu atpakaļ
12. Pārslēgt adrešu lapu uz priekšu

## Kā pievienot ierīci?

<img src="https://github.com/Hlebusek/GaismuPults/blob/main/images/AppAddDevice.png?raw=true" width=50% height=50%>
  Uzspiežot uz pogu 6. atveras logs kurā var uzstādīt gaismas iekārtas vērtību adreses un nosaukumu
  
## Kā saglabāt/importēt izveidotās ierīces?
  Uzspiežot uz pogu 3. atveras logs kurā var saglabāt visu uzstādīto gaismu ierīču adreses.
  Lai importētu gaismu ierīču adrese jāspiež uz pogas 4. un jaunajā logā jāizvēlas saglabātais fails.
  
  <img src="https://github.com/Hlebusek/GaismuPults/blob/main/images/AppImported.png?raw=true" width=50% height=50%>
  
## Kā saglabāt uzstādītās vērtības?

<img src="https://github.com/Hlebusek/GaismuPults/blob/main/images/AppSaveRec.png?raw=true" width=50% height=50%>

Uzpiežot uz pogas 1. atveras logs kurā var saglabāt visu gaismas iekārtu vai konkrētas iekārtas vērtības.
Visi saglabātie vērtību ieraksti ir atrodami nospiežot uz pogas 2., nospiežot uz kuriem saglabātās vērtības atgriežas.

<img src="https://github.com/Hlebusek/GaismuPults/blob/main/images/AppRecords.png?raw=true" width=50% height=50%>
  

```diff
-Created by Daniels Rudovičs :')
```


