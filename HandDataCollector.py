from tkinter import *
import random
import numpy as np
import pandas as pd
from tkinter import messagebox
from tkinter import filedialog
import serial


##Settings

root = Tk()
root.geometry("950x400")   #Size of window
root.resizable(0,0)        #Not resizable
root.configure(background="khaki")
root.title("Glove data Collector")

##Layout
dataFrame = Frame(root,width=600,height=400,bg="bisque",relief=SUNKEN)
dataFrame.pack(side=LEFT)

consoleFrame = Frame(root,width=400,height=200,bg="khaki",relief=SUNKEN)
consoleFrame.pack(side=TOP)
consoleFrame2 = Frame(root,width=400,height=200,bg="khaki",relief=SUNKEN)
consoleFrame2.pack(side=BOTTOM)

##=====================Global Variables and funtions====================

flexValues=np.zeros(5)
acValues=np.zeros(3)
gyValues=np.zeros(3)
selectedCom = ''
HandArduino=serial.Serial()
Dataset=np.full(11,10000)
filename=''
DataLabel=""

acceleromterNames=["acX: ","acY: ","acZ: "]
accelerometerLabels=[]
fingerNames=["Thumb: ","Index: ","Middle: ","Ring: ","Pinky: "]
fingerLabels=[]
gyroscopeNames = ["gyX: ","gyY: ","gyZ: "]
gyroscopeLabels=[]

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False
    
def SaveCom():
    global selectedCom
    global HandArduino
    x = comEntry.get()
    if x=='':
        messagebox.showerror("Error","No PORT was entered")

    elif not(is_number(x)):
        messagebox.showerror("Error","PORT number should be numeric value")
    else:
        temp='com'+x
        try:
            HandArduino = serial.Serial(temp,9600)
        except serial.serialutil.SerialException:
            messagebox.showerror("Error","Wrong Port Number or Arduino Not connected")
            selectedPortlabel.configure(text="Arduino not connected to Port: "+temp,
                                    fg="red")
        else:
            selectedCom=temp
            selectedPortlabel.configure(text="Arduino Connected to Port: "+selectedCom,
                                    fg="SpringGreen4")
        
def CollectData():
    global Dataset
    global flexValues
    global acValues
    global gyValues
    
    if selectedCom!='':
    
        HandArduino.write('S'.encode('utf-8'))
        while HandArduino.inWaiting()==0: pass
        dataString = HandArduino.readline().decode('ascii')
        print(dataString[0:-2])
        parsedData=dataString.split(' ')
        parsedData=parsedData[0:11]
        for i in range(11):
            Dataset[i]= int(parsedData[i])
            if i<5:
                flexValues[i] = Dataset[i]
            elif i<8:
                acValues[i-5] = Dataset[i]
            else:
                gyValues[i-8] = Dataset[i]
    else:
        messagebox.showerror("Error","Arduino not Connected")

def UpdateData():
    CollectData()
    
    for i in range(5):
        spaces = 5-len(str(flexValues[i]))
        fingerLabels[i].configure(text=fingerNames[i]+" "*spaces+str(flexValues[i]))
    for i in range(3):
        spaces = 5-len(str(acValues[i]))
        accelerometerLabels[i].configure(text = acceleromterNames[i]+" "*spaces+str(acValues[i]))
    for i in range(3):
        spaces = 5-len(str(gyValues[i]))
        gyroscopeLabels[i].configure(text=gyroscopeNames[i]+" "*spaces+str(gyValues[i]))
    #print(fingerText,acceleromterText,gyroscopeText)
    root.update()

def setLabel():
    global DataLabel
    templabel = outputEntry.get()
    if not templabel=='':
        DataLabel=templabel
        labelledlabel.configure(fg='SpringGreen4',
                                text="Selected Label: "+templabel)
    else:
        messagebox.showerror("Error","No Label value was entered")
        
def SaveToCSV():
    if filename!='':
        if selectedCom=='':
            messagebox.showerror("Error","Arduino not Connected")
        elif DataLabel=="":
            messagebox.showerror("Error","No Label value was entered")
        else:
            save = np.concatenate((Dataset,np.array(DataLabel)),axis=None)
            save = save.reshape(1,len(save))
            
            df = pd.DataFrame(save)
            df.to_csv(filename,mode='a',header=False, index=False)
            stat=""
            stat+= "<--Saved to "+filename+ ".csv-->"
            CSVstatus.configure(text=stat)
    else:
        messagebox.showerror("Error","Select a csv file first!")


def setFileName():
    global filename
    filename=str(filedialog.askopenfilename())
    if filename=='':
        messagebox.showerror("Error","No file selected")
        return
    temp = filename.split('/')[-1]
    if temp.split('.')[-1]!='csv':
        messagebox.showerror("Error","Please select CSV File")
        return
    CSVstatus.configure(text="Selected File: "+temp)
    dataToCsvBtn.configure(text="Store in: "+temp)

def setdefFileName():
    global filename
    filename='HandData.csv'
    CSVstatus.configure(text="Selected File: "+filename)
    dataToCsvBtn.configure(text="Store in: "+filename)

#===================== Showing DATA==================================================

dataheader = Label(dataFrame,
                   font=('Helvetica',20,'bold'),
                   text="Features",
                   bg="bisque",
                   fg = "OliveDrab4",
                   bd=10,
                   anchor="n")
dataheader.grid(columnspan=5)

  
flexheader = Label(dataFrame,
                   font=('calibri',15,'bold'),
                   text="Flex Sensor Data",
                   bg="bisque",
                   fg = "OliveDrab4",
                   bd=15,
                   anchor="w")
flexheader.grid(columnspan=3)
for fingers in range(5):
    tempLabel = Label(dataFrame,
                      font=('calibri',13),
                      padx=25,
                      text=fingerNames[fingers]+"_____",
                      bg="bisque",
                      fg = "navy",
                      bd="10",
                      )
    if fingers<=2: tempLabel.grid(row=2, column=fingers,sticky=W)
    else: tempLabel.grid(row=3, column=fingers-3,sticky=W)
    fingerLabels.append(tempLabel)

Accheader = Label(dataFrame,
                  font=('calibri',15,'bold'),
                  text="Accelerometer Data",
                  bg="bisque",
                  fg = "OliveDrab4",
                  bd=15,
                  anchor="w")
Accheader.grid(columnspan=3)
for axis in range(3):
    tempLabel = Label(dataFrame,
                      font=('calibri',13),
                      padx=25,
                      text=acceleromterNames[axis]+"_____",
                      bg="bisque",
                      fg = "navy",
                      bd="10")
    tempLabel.grid(row=5, column=axis, sticky=W)
    accelerometerLabels.append(tempLabel)

GYheader = Label(dataFrame,
                 font=('calibri',15,'bold'),
                 text="Gyroscope Data",
                 bg="bisque",
                 fg = "OliveDrab4",
                 bd=15,
                 anchor="w"
                 )
GYheader.grid(columnspan=3)
for axis in range(3):
    tempLabel = Label(dataFrame,
                      font=('calibri',13),
                      padx=25,
                      text=gyroscopeNames[axis]+"_____",
                      bg="bisque",
                      fg = "navy",
                      bd="10"
                      )
    tempLabel.grid(row=7, column=axis,sticky=W)
    gyroscopeLabels.append(tempLabel)
    
#================================Console=====================================

outputlabel = Label(consoleFrame,
                 text="Label the data: ",
                 fg="navy",
                 font=("arial",13),
                 bg='khaki',
                 pady=10,
                 )
outputlabel.grid(row=0,column=0,sticky=E)

outputEntry = Entry(consoleFrame,
                 insertwidth=1,
                 bg="bisque",
                 bd=3,
                 font=("arial",16),
                 fg="midnight blue",
                
                 )
outputEntry.grid(row=0,column=1)
outputBtn = Button(consoleFrame,
                        bg = "midnight blue",
                        bd=1,
                        fg="khaki",
                        text="Save",
                        font=("arial",10,'bold'),
                        pady=5,
                        command=setLabel
                        )
outputBtn.grid(row=0, column=3,sticky=W)

labelledlabel = Label(consoleFrame,
                        fg = "red",
                        font=('Times',13,'bold'),
                        text = "No label",
                        bg='khaki',
                        pady=5
                        )
labelledlabel.grid(row=1,column=0,columnspan=2,sticky=E)

comlabel = Label(consoleFrame,
                 text="Type PORT Number: ",
                 fg="navy",
                 font=("arial",13),
                 bg='khaki',
                 pady=10,
                 )
comlabel.grid(row=2,column=0)

comEntry = Entry(consoleFrame,
                 insertwidth=1,
                 bg="bisque",
                 bd=3,
                 font=("arial",16),
                 fg="midnight blue"
                 )
comEntry.grid(row=2,column=1)
comBtn = Button(consoleFrame,
                        bg = "midnight blue",
                        bd=1,
                        fg="khaki",
                        text="Save",
                        font=("arial",10,'bold'),
                        pady=5,
                        command=SaveCom
                        )
comBtn.grid(row=2, column=3,sticky=W)

selectedPortlabel = Label(consoleFrame,
                        fg = "red",
                        font=('Times',13,'bold'),
                        text = "No PORT selected",
                        bg='khaki',
                        pady=15
                        )
selectedPortlabel.grid(row=3,column=0,columnspan=2,sticky=E)
datacollectBtn = Button(consoleFrame2,
                        bg = "midnight blue",
                        bd=4,
                        fg="khaki",
                        text="Collect Data from arduino",
                        font=('Times',18,'bold'),
                        padx=10,
                        command=UpdateData
                        )
datacollectBtn.grid(row=0, columnspan=2,sticky=W)
dataCollectstatus = Label(consoleFrame2,
                fg = "midnight blue",
                font=('Times',10),
                text = "",
                bg='khaki',
                pady=5
                )
dataCollectstatus.grid(row=1,columnspan=2,sticky=E)
dataToCsvBtn = Button(consoleFrame2,
                    bg = "midnight blue",
                    bd=4,
                    fg="khaki",
                    text="Store in: <Select csv file>",
                    font=('Times',18,'bold'),
                    padx=20,
                    command=SaveToCSV
                    )
dataToCsvBtn.grid(row=2,rowspan=2, columnspan=2,sticky= E)
space = Label(consoleFrame2,
                fg = "midnight blue",
                font=('Times',10),
                text = "",
                bg='khaki',
                pady=5,
                padx=10,
                )
space.grid(row=2,rowspan=2,column=2,sticky=E)
FileBtn = Button(consoleFrame2,
                bg="bisque",
                bd=1,
                fg="midnight blue",
                text="Browse",
                font=("arial",10,'bold'),                        
                command=setFileName
                )
FileBtn.grid(row=2,column=3,sticky=W)

DefaultFileBtn = Button(consoleFrame2,
                    bg="bisque",
                    bd=1,
                    fg="midnight blue",
                    text="Default",
                    padx=2,
                    font=("arial",10,'bold'),
                    command=setdefFileName
                    )
DefaultFileBtn.grid(row=3,column=3,sticky=W)
CSVstatus = Label(consoleFrame2,
                fg = "midnight blue",
                font=('Times',10),
                text = "No upload file selected",
                bg='khaki',
                pady=15
                )
CSVstatus.grid(row=4,columnspan=3)

root.mainloop()


