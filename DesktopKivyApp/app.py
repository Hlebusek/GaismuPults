from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy import utils
from tkinter import Tk , filedialog
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
import json

import requests



Window.maximize()


Sliders = []
Devices = []
Groups = []
page = 1
AllSliders = []

UniverseDropdown = DropDown()
WaitingValues = []

DEBUG = True
IsConnected = False
SelectedDevice = None

SliderValues = {"1":{},"2":{}}

Records = []

Builder.load_file("./AddWindow.kv")
Builder.load_file("./main.kv")
Builder.load_file("./RecordWindow.kv")


class RecordsWindow(GridLayout):
    def __init__(self,**kwargs):
        super(RecordsWindow, self).__init__(**kwargs)
        self.size = (Window.width*0.5, Window.height*0.5)
        RecordCount = len(Records)
        CeiledRoot = int(-(-RecordCount**(1/2)//1))
        self.rows = CeiledRoot
        self.cols = CeiledRoot
        #print(f"CR >> {CeiledRoot}")

        for record in Records:
            RecordButton = Button(text = record["name"], size_hint = (None,None), size = (self.width/CeiledRoot, self.height/CeiledRoot), halign = "center", valign = "middle", font_size = "20dp")
            RecordButton.rec = record
            RecordButton.bind(on_press = APP.a.LoadRecord)
            self.add_widget(RecordButton)
            
        




class SaveRecordWindow(GridLayout):
    def __init__(self,**kwargs):
        super(SaveRecordWindow, self).__init__(**kwargs)
        self.size = (Window.width*0.32, Window.height*0.2)
        self.AddSelector = "SCENE"


    def Save(self):
        global Records
        universe = str(SelectedDevice["universe"])
        NewRecord = {"name": self.ids.RecordNameInp.text}
        NewRecord["values"] = {"1":{},"2":{}}
        if self.AddSelector == "DEVICE":
            NewRecord["type"] = "DEVICE"
            for ind in list(SelectedDevice["channels"].values()):
                if ind in SliderValues[universe]:
                    NewRecord["values"][universe][ind] = SliderValues[universe][ind]
                else:
                    NewRecord["values"][universe][ind] = 0


        elif self.AddSelector == "SCENE":
            for i in range(1,3):
                for ind in list(SliderValues[str(i)].keys()):
                    NewRecord["values"][str(i)][ind] = SliderValues[str(i)][ind]


            NewRecord["type"] = "SCENE"

        Records.append(NewRecord)
        #print(NewRecord)



class LeftBarButton(Button):

    def __init__(self, **kwargs):
        super(LeftBarButton, self).__init__(**kwargs)
        self.size_hint = (1, None)
        self.halign = "center"
        self.valign = "middle"
        self.font_size = "20dp"

class AddWindow(GridLayout):

    def __init__(self,**kwargs):
        super(AddWindow, self).__init__(**kwargs)
        self.size = (Window.width*0.4, Window.height*0.4)
        self.AddSelector = None

    def Confirm(self):
        #print(self.AddSelector)

        if self.AddSelector in [None, "DEVICE"]:
            NewDevice = {
            "name": self.ids.NInp.text,
            "color": (0.2,0.4,0.6,1),
            "universe": str(elf.ids.UInp.text),
            "channels": {
                "R": int(self.ids.RInp.text),
                "G": int(self.ids.GInp.text),
                "B": int(self.ids.BInp.text),
                "M": int(self.ids.MInp.text)
                }
            }   
            Devices.append(NewDevice)
            APP.a.AddDeviceButton(NewDevice)
        elif self.AddSelector == "GROUP":
            NewGroup = {"name": self.ids.NInp.text,"devices": []}
            Groups.append(NewGroup)

class MainWindow(Widget):


    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)

        self.size = Window.size
        with self.canvas.before:
            Rectangle(source='Background2.png', pos=self.pos, size = Window.size)

        for i in range(10):
            SliderLayout = GridLayout(rows=3, cols=1, size_hint = (None, 1), width = self.ids.InnerBox.width/12, height = self.ids.InnerBox.height-20, spacing = (0,34))
            
            Sliders.append([
                Slider(disabled=True,value_track_color=(0,0,0,1),cursor_disabled_image = "./SliderCursor.png",cursor_image = "./SliderCursor.png",background_width="100sp",cursor_size =("30sp","40sp"),sensitivity = "all",min=0, max=255, value=0,orientation = "vertical",value_track = True,size_hint = (None,None), height = SliderLayout.height*0.8, step = 1),
                Label(text=f"", halign = 'center', size_hint = (None,None), height = SliderLayout.height*0.04, font_size='20sp'),
                Button(text ='MAX',font_size='20sp',size_hint =(None, None), height = SliderLayout.height*0.1,color=(1,1,1,1), background_color=(1,1,1,0.7))
                ])

            Sliders[i][0].bind(value=self.SliderValueChange)
            Sliders[i][0].Addr = "0"
        
            Sliders[i][2].bind(on_press = self.MaxOn)
            Sliders[i][2].bind(on_release=self.MaxOff)

            for element in Sliders[i]:
                element.i = i

            SliderLayout.add_widget(Sliders[i][1])
            SliderLayout.add_widget(Sliders[i][0])
            SliderLayout.add_widget(Sliders[i][2])

            self.ids.InnerBox.add_widget(SliderLayout) 

        PreviousButton = Button(font_size = '40sp',text = "<", size_hint = (None,None), height = SliderLayout.height/8, width = SliderLayout.width, background_color=(1,1,1,0.4))
        NextButton = Button(font_size = '40sp',text = ">", size_hint = (None,None), height = SliderLayout.height/8, width = SliderLayout.width, background_color=(1,1,1,0.4))
        
        PreviousButton.bind(on_press = self.PrevPage)
        NextButton.bind(on_press = self.NextPage)

        RightBarLayout = GridLayout(rows = 5, cols = 1, size_hint = (None, None),size = SliderLayout.size)
        RightBarLayout1 = GridLayout(rows = 2, cols =1, size_hint = (None, None),size = SliderLayout.size)

        MoreButtonsLayout = GridLayout(size_hint=(None,None), height =SliderLayout.height - NextButton.height)

        RightBarLayout.add_widget(MoreButtonsLayout)
        RightBarLayout1.add_widget(GridLayout(size_hint=(None,None), height =SliderLayout.height - NextButton.height))

        RightBarLayout.add_widget(NextButton)
        RightBarLayout1.add_widget(PreviousButton)

        self.ids.InnerBox.add_widget(RightBarLayout1)
        self.ids.InnerBox.add_widget(RightBarLayout)

        for device in [{"name": "Universe1","universe": "1","color": [1,1,1,1],"channels": "@"},{"name": "Universe2","universe": "2","color": [1,1,1,1],"channels": "@"}]:
            self.AddDeviceButton(device)


    def ImportScene(self):
        global Devices
        global Records
        Tk().withdraw()
        FileLoc = filedialog.askopenfilename(title = "Import scene", initialdir = "./..", multiple = False, filetypes=[("Lightscene files", ".lscn")])
        self.ids.TopBarLayout.clear_widgets()
        self.ids.TopBarLayout.add_widget(self.ids.AddDeviceButton)
        for device in [{"name": "Universe1","universe": "1","color": [1,1,1,1],"channels": "@"},{"name": "Universe2","universe": "2","color": [1,1,1,1],"channels": "@"}]:
            self.AddDeviceButton(device)
        if (FileLoc):
            try:
                with open(FileLoc, "r") as f:
                    SceneData = json.load(f)
                    f.close()
                    Devices = SceneData["devices"]
                    Records = SceneData["records"]
                    #print(Records)
            except:
                print(f"Failed to import scene file >> \"{FileLoc}\"")
                return

            for item in SceneData["devices"]:
                self.AddDeviceButton(item)

    def AddDeviceButton(self, data):
        DeviceButton = Button(text = data["name"],background_color = data["color"],size_hint = (None, None),size = self.ids.AddDeviceButton.size)
        DeviceButton.data = data
        DeviceButton.bind(on_press = self.Select)
        self.ids.TopBarLayout.add_widget(DeviceButton)  

    def SaveScene(self):
        global Devices
        Tk().withdraw()
        FileLoc = filedialog.asksaveasfilename(title = "Save scene as", initialdir = "./..", filetypes=[("Lightscene files", ".lscn")])
        SaveData = {
            "devices": Devices,
            "records": Records
        }
        if not FileLoc.endswith(".lscn"):
            FileLoc = FileLoc + ".lscn"
        with open(f"{FileLoc}", "w") as f:
            json.dump(SaveData, f, indent = 4)
            f.close()

    def Create(self):
        window = AddWindow()
        AddPopup = Popup(title = "Add", content = window,size = (window.width+28, window.height+62), size_hint = (None, None))
        AddPopup.open()

    def Select(self, instance):
        global SelectedDevice
        global page
        page = 1
        SelectedDevice = instance.data
        self.LoadSliders(instance.data)

        #print(instance.data)

    def LoadSliders(self, data):
        if data["channels"] == "@":
            for i in range(10):
                Sliders[i][1].text = f"\nCH\n{i+1}"
                Sliders[i][0].universe = data["universe"]
                Sliders[i][0].disabled = False
                Sliders[i][2].disabled = False
                Sliders[i][0].Addr = str(i+1)
                try:
                    val = SliderValues[SelectedDevice["universe"]][str(i+1)]
                    Sliders[i][0].value = val
                except:
                    Sliders[i][0].value = 0
                Sliders[i][0].disabled = False

            return
                
        i = 0
        for key, value in data["channels"].items():
            if i == 10:
                break
            Sliders[i][1].text = key
            Sliders[i][0].universe = data["universe"]
            Sliders[i][0].disabled = False
            Sliders[i][2].disabled = False
            Sliders[i][0].Addr = str(value)
            try:
                val = SliderValues[SelectedDevice["universe"]][str(value)]
                Sliders[i][0].value = val
            except:
                Sliders[i][0].value = 0
            Sliders[i][0].disabled = False
            i+=1
        for x in range(i, 10):
            Sliders[x][0].disabled = True
            Sliders[x][0].value = 0
            Sliders[x][0].Addr = "0"
            Sliders[x][1].text = ""
            Sliders[x][2].disabled = True

    def SliderValueChange(self, instance, value):
        try:
            SliderValues[str(instance.universe)][str(instance.Addr)] = value
        except:
            pass

        try:
            SliderValues[instance.universe][str(instance.Addr)] = value
        except:
            pass
        self.SendData(instance.universe, instance.Addr, value)
        pass


    def PrevPage(self, instance):
        ind = 0
        global page
        if page != 1:

            if SelectedDevice["channels"] == "@":
                for i in range(10):

                    ind = 10*(page-2) + i+1
                    Sliders[i][1].text = f"\nCH\n{ind}"
                    Sliders[i][0].universe = SelectedDevice["universe"]
                    Sliders[i][0].disabled = True
                    Sliders[i][2].disabled = False
                    Sliders[i][0].Addr = ind
                    try:
                        val = SliderValues[SelectedDevice["universe"]][str(ind)]
                        Sliders[i][0].value = val
                    except:
                        Sliders[i][0].value = 0
                    Sliders[i][0].disabled = False
                page-=1
                return

            data = list(SelectedDevice["channels"].items())
            for i in range(10* (page-1), 10*page ):
                ind = i-10*(page-1)
                Sliders[ind][1].text = data[i-10][0]
                Sliders[ind][0].universe = SelectedDevice["universe"]
                Sliders[ind][0].disabled = True
                Sliders[ind][2].disabled = False
                Sliders[ind][0].Addr = str(data[i-10][1])
                try:
                    val = SliderValues[SelectedDevice["universe"]][i-10]
                    Sliders[ind][0].value = val
                except:
                    Sliders[ind][0].value = 0
                Sliders[ind][0].disabled = False
            page-=1

    def NextPage(self, instance):
        global page
        if SelectedDevice:

            if SelectedDevice["channels"] == "@":
                if page < 52:
                    for i in range(10):
                        ind = i+10*(page)+1
                        Sliders[i][1].text = f"\nCH\n{ind}"
                        Sliders[i][0].universe = SelectedDevice["universe"]
                        Sliders[i][0].disabled = True
                        Sliders[i][2].disabled = False
                        Sliders[i][0].Addr = str(ind)
                        try:
                            val = SliderValues[SelectedDevice["universe"]][str(ind)]
                            Sliders[i][0].value = val
                        except:
                            Sliders[i][0].value = 0
                        Sliders[i][0].disabled = False    

                        if ind > 512:
                            Sliders[i][0].disabled = True
                            Sliders[i][0].Addr = "0"
                            Sliders[i][0].value = 0
                            Sliders[i][1].text = ""
                            Sliders[i][2].disabled = True

                    page+=1
                return

            if len(SelectedDevice["channels"]) > 10*page:
                data = list(SelectedDevice["channels"].items())  
                for i in range(10*page, 10*(page+1)+1):
                    ind = i-10*page-1
                    if len(data) >= i:
                        Sliders[ind][1].text = data[i-1][0]
                        Sliders[ind][0].universe = SelectedDevice["universe"]
                        Sliders[ind][0].disabled = True
                        Sliders[ind][2].disabled = False
                        Sliders[ind][0].Addr = str(data[i-1][1])

                        try:
                            val = SliderValues[SelectedDevice["universe"]][i-1]
                            Sliders[ind][0].value = val
                        except:
                            Sliders[ind][0].value = 0
                        Sliders[ind][0].disabled = False    

                    elif i > len(data):
                        Sliders[ind][0].disabled = True
                        Sliders[ind][0].Addr = "0"
                        Sliders[ind][0].value = 0
                        Sliders[ind][1].text = ""
                        Sliders[ind][2].disabled = True

                page+=1

    def FullStop(self):
        for i in range(10):
            Sliders[i][0].value = 0  
        global SliderValues
        for i in range(512):
            self.SendData(1,i,0)
            #self.SendData(2,i,0)
        SliderValues = {1:{},2:{}}

    def MaxOn(self, instance):
        Sliders[instance.i][0].lastval = Sliders[instance.i][0].value
        Sliders[instance.i][0].value = 255
        #print(f"max on > {instance.i}")

    def MaxOff(self, instance):
        Sliders[instance.i][0].value = Sliders[instance.i][0].lastval

    def SendData(self, G, C, V):
        try:
            a = requests.get(f"http://192.168.1.177:80/COMMAND?GROUP={G}&CHANNEL={C}&VALUE={int(V)}&", timeout=None)
            #print(f"Servers response > {a.text}")
            pass
        except:
            pass



    def ShowRecords(self):
        window = RecordsWindow()
        AddPopup = Popup(title = "Records", content = window,size = (window.width+28, window.height+62), size_hint = (None, None))
        AddPopup.open()

    def SaveRecord(self):
        window = SaveRecordWindow()
        AddPopup = Popup(title = "Save record", content = window,size = (window.width+28, window.height+62), size_hint = (None, None))
        AddPopup.open()

    def LoadRecord(self,instance):
        #print(instance.rec)
        for i in range(1,3):
            x = str(i)

            channels = instance.rec["values"][x]
            #print(channels)
            if instance.rec["type"] == "DEVICE":
                for key, value in channels.items():
                    SliderValues[x][str(key)] = value
                    self.SendData(x,key,value)



            elif instance.rec["type"] == "SCENE":
                for b in range(1,513):
                    if str(b) in channels:
                        SliderValues[x][str(b)] = channels[str(b)]
                        self.SendData(x,b,channels[str(b)])  
                    else:
                        try:
                            if str(b) in SliderValues[x]:
                                SliderValues[x][str(b)] = 0
                                self.SendData(x,b,0)
                        except:
                            if b in SliderValues[x]:
                                SliderValues[x][str(b)] = 0
                                self.SendData(x,b,0)
        #print(SliderValues)
        self.UpdateSliders()

    def UpdateSliders(self):
        if SelectedDevice:
            for i in range(10):
                Addr = Sliders[i][0].Addr

                universe = SelectedDevice["universe"]
                #print(f" ADDR > {Addr} U >> {universe}")
                if Addr in SliderValues[universe]:
                   # print(f"SI SI >> {SliderValues[universe][Addr]}")
                    Sliders[i][0].value = SliderValues[universe][Addr]


class DMX_MIXER(App):

    def build(self): 
        self.title = "DKM MIXER"
        self.a = MainWindow()
        return self.a


APP = DMX_MIXER()
APP.run()
