# GlovedataCollector
This personal project is a GUI to collect data from a glove through an arduino from 5 flex sensors on each fingers and a MPU-6050 for detecting orientation and movement of hand. The data will be used to train models for various purposes.

The whole code is in HandDataCollector.py -- download this to read the code
Used modules- 
#Tkinter   [For building GUI]
#serial    [For communicating with arduino]
#numpy     [For collecting and manipulating arrays]
#pandas    [To store the data in a csv file]

If you want to just try out the GUI, download the executable file HandDataCollector.exe from the dist folder.
The script was converted into exe file using pyinstaller module.
