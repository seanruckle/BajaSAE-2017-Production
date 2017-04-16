#!/usr/bin/env python3

from tkinter import *
import threading, queue, serial, matplotlib, sys, time
from matplotlib import pyplot as plt
import numpy as np


from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

matplotlib.rcParams.update({'figure.autolayout': True})


class SerialThread(threading.Thread):
    def __init__(self, COMPort,COMBaud, RXqueue, TXqueue):
        self._stopevent = threading.Event()
        threading.Thread.__init__(self)
        self.baud = COMBaud
        self.COM = COMPort
        self.rx = RXqueue
        self.tx = TXqueue
    def run(self):
        s = serial.Serial(self.COM.get(), self.baud.get(), timeout=1)
        if(s.isOpen()):
            s.close()
        s.open()
        while not self._stopevent.isSet():
            if s.inWaiting():
                text = s.readline()
                #print(text)
                self.rx.put(text)
                print(text)
            if self.tx.qsize():
                try:
                    s.write(bytes(self.tx.get(),'UTF-8'))
                except queue.Empty:
                    pass
        s.close()
    def join(self, timeout=None):
        """ Stop the thread. """
        self._stopevent.set(  )
        threading.Thread.join(self, timeout)


class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Baja GUI")
        
        self.grid()
        cw = 1   # cell width
        ch = 2
        
        cr = self.winfo_screenwidth() / 32
        
        print(self.winfo_screenheight())
        print(self.winfo_screenwidth())
        
        # Root level frames
        self.controlFrame = Frame(self, bg='grey', borderwidth=0, width=self.winfo_screenwidth(), height=(self.winfo_screenheight()/4))
        self.displayFrame = Frame(self, bg='grey', borderwidth=0)
        # Serial Control Frame
        self.serialFrame = Frame(self.controlFrame, borderwidth=0)  
        
        self.COMPort = StringVar()
        self.COMPortTextBox = Entry(self.serialFrame, textvariable = self.COMPort)
        self.COMPort.set('/dev/ttyUSB0')
        self.COMBaud = StringVar()
        self.COMBaudTextBox = Entry(self.serialFrame, textvariable = self.COMBaud)
        self.COMBaud.set('9600')
        self.COMButton = Button(self.serialFrame, text = "Start Serial", command = self.StartSerial)
        
        self.SerialSendButton = Button(self.serialFrame, text = "Send to Board", command = self.SendToSerial)
        self.SerialSendToDriverButton = Button(self.serialFrame, text = "Send to Driver", command = self.SendToDriver)
        self.SerialSendTextBox = Entry(self.serialFrame)

        

        # Extra Buttons
        self.SerialStopButton = Button(self.serialFrame, text = "Stop Serial", command = self.StopSerial)
        self.comeBackToPitNowButton = Button(self.controlFrame, text = "Pit Now", command = self.PitNow)
        self.comeBackToPitNextLapButton = Button(self.controlFrame, text = "Pit Next Lap", command = self.PitNextLap)

        # Informative Things
        self.dataBarFrame = Frame(self.controlFrame)
        
        self.numActiveThreads = StringVar()
        self.numThreadsLabel = Label(self.dataBarFrame, textvariable = self.numActiveThreads)
        self.numActiveThreads.set('Threads\n' + str(threading.enumerate().__len__()))
        self.numThreadsLabel.grid(column = 0, row = 0)
        
        
        self.counter = StringVar()
        self.counterLabel = Label(self.dataBarFrame, textvariable = self.counter)
        self.counter.set('Counter\n' + 'N/A')
        self.counterLabel.grid(column = 1, row = 0)
        
        self.gpsDate = StringVar()
        self.gpsDateLabel = Label(self.dataBarFrame, textvariable = self.gpsDate)
        self.gpsDate.set('Date\n' + '010100')
        self.gpsDateLabel.grid(column = 2, row = 0)
        
        self.gpsTime = StringVar()
        self.gpsTimeLabel = Label(self.dataBarFrame, textvariable = self.gpsTime)
        self.gpsTime.set('Time\n' + '00000000')
        self.gpsTimeLabel.grid(column = 3, row = 0)
        
        self.numSats = StringVar()
        self.numSatsLabel = Label(self.dataBarFrame, textvariable = self.numSats)
        self.numSats.set('Sats\n' + 'NSA')
        self.numSatsLabel.grid(column = 4, row = 0)

        self.currentLatitude = StringVar()
        self.latitudeLabel = Label(self.dataBarFrame, textvariable = self.currentLatitude)
        self.currentLatitude.set("Latitude\n" + 'Unknown')
        self.latitudeLabel.grid(column = 5, row = 0)
        
        
        self.currentLongitude = StringVar()
        self.longitudeLabel = Label(self.dataBarFrame, textvariable = self.currentLongitude)
        self.currentLongitude.set("Longitude\n" + 'Unknown')
        self.longitudeLabel.grid(column = 6, row = 0)
        
        
        self.currentSpeed = StringVar()
        self.speedLabel = Label(self.dataBarFrame, textvariable=self.currentSpeed)
        self.currentSpeed.set("Speed\n" + "86")
        self.speedLabel.grid(column = 7, row = 0)
        
        self.currentDashTemp = StringVar()
        self.dashTempLabel = Label(self.dataBarFrame, textvariable=self.currentDashTemp)
        self.currentDashTemp.set("Dash Temp\n" + "N/A")
        self.dashTempLabel.grid(column = 8, row = 0)
        
        self.batteryVoltage = StringVar()
        self.batteryVoltageLabel = Label(self.dataBarFrame, textvariable = self.batteryVoltage)
        self.batteryVoltage.set("BATT\n" + "N/A")
        self.batteryVoltageLabel.grid(column = 9, row = 0)
        
        
        self.xbeeSignalStrength = StringVar()
        self.xbeeSignalStrengthLabel = Label(self.dataBarFrame, textvariable = self.xbeeSignalStrength)
        self.xbeeSignalStrength.set("XBee\n" + "N/A")
        self.xbeeSignalStrengthLabel.grid(column = 10, row = 0)
        
        self.currentFrontBrakeAvg = StringVar()
        self.frontBrakeAvgLabel = Label(self.dataBarFrame, textvariable = self.currentFrontBrakeAvg)
        self.currentFrontBrakeAvg.set("Front Brake Avg\n" + "N/A")
        self.frontBrakeAvgLabel.grid(column = 11, row = 0)
        
        self.currentFrontBrakeMax = StringVar()
        self.frontBrakeMaxLabel = Label(self.dataBarFrame, textvariable = self.currentFrontBrakeMax)
        self.currentFrontBrakeMax.set("Front Brake Max\n" + "N/A")
        self.frontBrakeMaxLabel.grid(column = 12, row = 0)
        
        self.currentRearBrakeAvg = StringVar()
        self.rearBrakeAvgLabel = Label(self.dataBarFrame, textvariable = self.currentRearBrakeAvg)
        self.currentRearBrakeAvg.set("Rear Brake Avg\n" + "N/A")
        self.rearBrakeAvgLabel.grid(column = 13, row = 0)
        
        self.currentRearBrakeMax = StringVar()
        self.rearBrakeMaxLabel = Label(self.dataBarFrame, textvariable = self.currentRearBrakeMax)
        self.currentRearBrakeMax.set("Rear Brake Max\n" + "N/A")
        self.rearBrakeMaxLabel.grid(column = 14, row = 0)
        

        self.currentSteeringAvg = StringVar()
        self.steeringAvgLabel = Label(self.dataBarFrame, textvariable = self.currentSteeringAvg)
        self.currentSteeringAvg.set("Steering\n" + "Yes")
        self.steeringAvgLabel.grid(column = 15, row = 0)
        
        self.buttonPressed = StringVar()
        self.buttonPressedLabel = Label(self.dataBarFrame, textvariable = self.buttonPressed, borderwidth = 1)
        self.buttonPressed.set("Button\n" + "No")
        self.buttonPressedLabel.grid(column = 16, row = 0)
        
        
        self.currentPrimaryRPM = StringVar()
        self.currentSecondaryRPM = StringVar()
        
        # Accelerometer
        self.accX = [0]
        self.maxX = [0]
        self.accY = [0]
        self.maxY = [0]
        self.accZ = [0]
        self.maxZ = [0]
        
        # 
        self.rearTemp = [0]

        
        

        self.listbox = Listbox(self.controlFrame)
        
        # Set to full screen
        self.attributes('-fullscreen', True)
        
        # Bind <Return> Keypress to text boxes
        self.SerialSendTextBox.bind("<Return>", self.SendOnReturn)
        self.COMBaudTextBox.bind("<Return>", self.StartSerialOnReturn)
        
        # Pack Serial Controls into Serial Frame
        self.SerialSendTextBox.grid(column = 0, row=0, sticky=EW)
        self.SerialSendButton.grid(column = 2, row=0)
        self.SerialSendToDriverButton.grid(column = 3, row = 0)
        self.COMPortTextBox.grid(column = 4, row=0, sticky = E)
        self.COMBaudTextBox.grid(column=6, row=0, sticky = E)
        self.COMButton.grid(column = 8, row=0, sticky = NE)
        self.SerialStopButton.grid(row = 0, column = 9, sticky=NE)
        
        # Pack Control Widgets into Control Frame
        self.serialFrame.grid(row = 0, column=0, columnspan=12, sticky=EW)
        
        
        self.comeBackToPitNowButton.grid(row=0, column=10, sticky=NSEW)
        self.comeBackToPitNextLapButton.grid(row=1, column=10, sticky=NSEW)

        self.dataBarFrame.grid(row = 1, column = 0, columnspan = 10, sticky = EW)
        
        self.listbox.grid(row = 2, column = 0, columnspan=10, sticky = EW)
        
        # Pack Control Frame into root
        self.controlFrame.grid(row = 0, sticky=EW)
        
        
        # Top Level Display Frames
        self.leftDisplayFrame = Frame(self.displayFrame, bg='grey', borderwidth=0, width=(self.winfo_screenwidth()/2))
        self.rightDisplayFrame = Frame(self.displayFrame, bg='grey', borderwidth=0, width=(self.winfo_screenwidth()/2))
        
        # Inside Left Display Frames
        self.topLeftDisplayFrame = Frame(self.leftDisplayFrame, bg='grey', borderwidth=0, height=(self.winfo_screenheight()/4))
        self.middleLeftDisplayFrame = Frame(self.leftDisplayFrame, bg='grey', borderwidth=0, height=(self.winfo_screenheight()/4))
        self.bottomLeftDisplayFrame = Frame(self.leftDisplayFrame, bg='grey', borderwidth=0, height=(self.winfo_screenheight()/4))
        
        # Inside Top Left Display Frames
        
        # Inside Middle Left Display Frames
        self.brakeFrame = Frame(self.middleLeftDisplayFrame, borderwidth=0)
        
        # Inside Bottom Left Display Frames
        self.driveTrainTempFrame = Frame(self.bottomLeftDisplayFrame, borderwidth=0)
        self.driveTrainRPMFrame = Frame(self.bottomLeftDisplayFrame, borderwidth=0)
        
        # Inside Rigt Display Frames
        self.shieldTempFrame = Frame(self.rightDisplayFrame, borderwidth=0, bg='grey', height=(self.winfo_screenheight()/8))
        self.shieldHealthFrame = Frame(self.rightDisplayFrame, borderwidth=0, bg='grey')
        
        # Construct Items for Display Frame
        self.gpsFigure, self.gpsAxes = plt.subplots(figsize=(2*ch,2*ch), dpi=cr*2)
        self.speedFigure, self.speedAxes = plt.subplots(figsize=(2*ch,2*ch), dpi=cr)

        
        self.rpmFigure, self.rpmAxes = plt.subplots(figsize=(ch,ch), dpi=cr)
        self.dashTempFigure, self.dashTempAxes = plt.subplots(figsize=(2*ch,ch), dpi=cr)
        self.rearTempFigure, self.rearTempAxes = plt.subplots(figsize=(2*ch,ch), dpi=cr)
        self.gearTempFigure, self.gearTempAxes = plt.subplots(figsize=(2*ch,ch), dpi=cr)
        self.cvtTempFigure, self.cvtTempAxes = plt.subplots(figsize=(2*ch,ch), dpi=cr)
        self.battFigure, self.battAxes = plt.subplots(figsize=(ch,ch), dpi=cr)
        self.frontBrakeFigure, self.frontBrakeAxes = plt.subplots(figsize=(2*ch,ch), dpi=cr)
        self.rearBrakeFigure, self.rearBrakeAxes = plt.subplots(figsize=(2*ch,ch), dpi=cr)
        self.steeringFigure, self.steeringAxes = plt.subplots(figsize=(ch,2*ch), dpi=cr)
        self.buttonFigure, self.buttonGraph = plt.subplots(figsize=(ch,ch), dpi=cr)
        self.accFigure, self.accAxes = plt.subplots(figsize=(2*ch,2*ch), dpi=cr)
        self.zFigure, self.zAxes = plt.subplots(figsize=(ch, 2*ch), dpi=cr)
        
        
        # GPS Axes Setup
        self.gpsFigure.patch.set_visible(False)
        self.gpsAxes.set_title('GPS')
        #self.gpsAxes.set_xlim(-110.953,-110.952)
        self.gpsAxes.set_xlim(-118823207 - 3000,-118823207 + 3000)
        self.gpsAxes.set_ylim(34749085 - 3000,34749085 + 3000)
        self.gpsAxes.hold(True)
        
        self.gpsCanvas = FigureCanvasTkAgg(self.gpsFigure, master=self.rightDisplayFrame)
        self.gpsCanvas.show()
        
        
        
        
        
        # speed Axes Setup
        self.speedFigure.patch.set_visible(False)
        self.speedAxes.set_title('Speed')
        self.speedAxes.set_xlim(0,100)
        self.speedAxes.set_ylim(0,50)
        self.speedAxes.hold(True)
        
        self.speedCanvas = FigureCanvasTkAgg(self.speedFigure, master=self.topLeftDisplayFrame)
        self.speedCanvas.show()

        # Speed Textbox Setup

        
        # Dash Temperature Axes Setup
        self.dashTempFigure.patch.set_visible(False)
        self.dashTempAxes.set_title('Dash Temperature')
#        self.ten_wide = [0,1,2,3,4,5,6,7,8,9]
        self.dashTempAxes.set_xlim(0,100)
#        self.dashTempAxes.autoscale(enable=True, axis='x')
        self.dashTempAxes.set_ylim(0,100)
        self.dashTempAxes.hold(True)
        
        self.dashTempCanvas = FigureCanvasTkAgg(self.dashTempFigure, master=self.shieldTempFrame)
        self.dashTempCanvas.show()
#        self.dashTempCanvas.draw()

        
        
        # Rear Temperature Axes Setup
        self.rearTempFigure.patch.set_visible(False)
        self.rearTempAxes.set_title('Rear Temperature')
        self.rearTempAxes.set_xlim(0,500)
        self.rearTempAxes.set_ylim(0,100)
        self.rearTempAxes.hold(True)
        
        self.rearTempCanvas = FigureCanvasTkAgg(self.rearTempFigure, master=self.shieldTempFrame)
        self.rearTempCanvas.show()
#        
        
        
        # Gearbox Temperature Axes Setup
        self.gearTempFigure.patch.set_visible(False)
        self.gearTempAxes.set_title('Gearbox Temperature')
        self.gearTempAxes.set_xlim(0,500)
        self.gearTempAxes.set_ylim(0,100)
        self.gearTempAxes.hold(True)
        
        self.gearTempCanvas = FigureCanvasTkAgg(self.gearTempFigure, master=self.driveTrainTempFrame)
        self.gearTempCanvas.show()
#        
        
        
        # CVT Temperature Axes Setup
        self.cvtTempAxes.set_title('CVT Temperature')
        self.cvtTempAxes.set_xlim(0,500)
        self.cvtTempAxes.set_ylim(0,100)
        self.cvtTempAxes.hold(True)
        
        self.cvtTempCanvas = FigureCanvasTkAgg(self.cvtTempFigure, master=self.driveTrainTempFrame)
        self.cvtTempCanvas.show()
#        
        
        
        # Acceleration Axes Setup
        self.accFigure.patch.set_visible(False)
        self.accAxes.set_title('Acceleration 2-D')
        self.accAxes.set_xlim(-2, 2)
        self.accAxes.set_ylim(-2, 2)
        self.accAxes.hold(True)
        
        self.accCanvas = FigureCanvasTkAgg(self.accFigure, master=self.middleLeftDisplayFrame)
        self.accCanvas.show()
        
        self.zFigure.patch.set_visible(False)
        self.zAxes.set_title('Z-Acc')
        self.zAxes.set_xlim(-2, 2)
        self.zAxes.set_ylim(-2, 2)
        self.zAxes.hold(True)
        
        self.zCanvas = FigureCanvasTkAgg(self.zFigure, master=self.topLeftDisplayFrame)
        self.zCanvas.show()
        
        
        self.steeringFigure.patch.set_visible(False)
        self.steeringAxes.set_title('Steering')
        self.steeringAxes.set_xlim(-2, 2)
        self.steeringAxes.set_ylim(-2, 2)
        self.steeringAxes.hold(True)
        
        self.steeringCanvas = FigureCanvasTkAgg(self.steeringFigure, master=self.topLeftDisplayFrame)
        self.steeringCanvas.show()
        
        # Front Brake Axes Setup
        self.frontBrakeFigure.patch.set_visible(False)
        self.frontBrakeAxes.set_title('Front Brake Pressure')
        self.frontBrakeAxes.set_xlim(0,500)
        self.frontBrakeAxes.set_ylim(0,100)
        self.frontBrakeAxes.hold(True)
        
        self.frontBrakeCanvas = FigureCanvasTkAgg(self.frontBrakeFigure, master=self.brakeFrame)
        self.frontBrakeCanvas.show()
        
        # Rear Brake Axes Setup
        self.rearBrakeFigure.patch.set_visible(False)
        self.rearBrakeAxes.set_title('Rear Brake Pressure')
        self.rearBrakeAxes.set_xlim(0,500)
        self.rearBrakeAxes.set_ylim(0,100)
        self.rearBrakeAxes.hold(True)
        
        self.rearBrakeCanvas = FigureCanvasTkAgg(self.rearBrakeFigure, master=self.brakeFrame)
        self.rearBrakeCanvas.show()
        
        # Layout
        # Pack Brake Pressure
        self.frontBrakeCanvas.get_tk_widget().grid(column = 0, row=0, sticky=N)
#        self.frontBrakeCanvas._tkcanvas.grid(column=0, row=0, sticky=N)
        self.rearBrakeCanvas.get_tk_widget().grid(column=0, row=1, sticky=S)
#        self.rearBrakeCanvas._tkcanvas.grid(column=0, row=1, sticky=S)
        
        # Pack Drive Train RPM
        
        # Pack Drive Train Temp
        self.gearTempCanvas.get_tk_widget().grid(column = 0, row=0, sticky=W)
#        self.gearTempCanvas._tkcanvas.grid(column=0, row=0, sticky=W)
        self.cvtTempCanvas.get_tk_widget().grid(column=1, row=0, sticky=E)
#        self.cvtTempCanvas._tkcanvas.grid(column=1, row=0, sticky=E)
        
        # Pack stuff into top left
#        self.speedTextBox.grid(column=1, row=0, sticky=NSEW)
        self.zCanvas.get_tk_widget().grid(column=0, row=0, sticky=NSEW)
        self.steeringCanvas.get_tk_widget().grid(column=1, row=0, sticky=NSEW)
        self.speedCanvas.get_tk_widget().grid(column=2, row=0 , sticky=NSEW)
#        self.speedCanvas._tkcanvas.grid(column=2 , row=0 , sticky=NSEW)
        
        # Pack stuff into middle left
        self.accCanvas.get_tk_widget().grid(column=0 , row=1 , sticky=W  )
#        self.accCanvas._tkcanvas.grid(column=0 , row=1 , sticky=W  )
        self.brakeFrame.grid(column=1 , row=1 , sticky=E)
        
        # Pack stuff into bottom left
        self.driveTrainTempFrame.grid(column=0 , row=5 , sticky=N  )
        self.driveTrainRPMFrame.grid(column=0 , row=6 , sticky=S  )
        
        
        # Pack Left Display
        self.topLeftDisplayFrame.grid(column=0 , row=2 , sticky=NSEW  )
        self.middleLeftDisplayFrame.grid(column=0 , row=4 , sticky=NSEW  )
        self.bottomLeftDisplayFrame.grid(column=0 , row=6 , sticky=NSEW  )
        
        
        # Pack Shield Temp
        self.dashTempCanvas.get_tk_widget().grid(column=0 , row=5   )
#        self.dashTempCanvas._tkcanvas.grid(column=0 , row=5 , sticky=W  )
        self.rearTempCanvas.get_tk_widget().grid(column=1 , row=5   )
#        self.rearTempCanvas._tkcanvas.grid(column=1 , row=5 , sticky=E  )
        
        # Pack Shield Health
        
        # Pack stuff inside right display
        self.gpsCanvas.get_tk_widget().grid(column=4 , row=2 , sticky=NSEW  )
#        self.gpsCanvas._tkcanvas.grid(column=4 , row=2 , sticky=NSEW  )
        self.shieldTempFrame.grid(column=4 , row=5 , sticky=N  )
        self.shieldHealthFrame.grid(column=4 , row=6 , sticky=N  )
            # TODO: Button Press notification goes here...
        
        
        # Pack Display Frame
        self.leftDisplayFrame.grid(column=0 , row=3 , sticky=NS  )
        self.rightDisplayFrame.grid(column=5 , row=3 , sticky=NS  )
        
        # Pack Display Into Root
        self.displayFrame.grid(column=0 , row=2 , sticky=NSEW  )
        
        
    # Initialize Data Variables
        
        # Dash Data
#        self.counter.set(0) # Commented to preserve initial text value, left here to preserve variable order/index
#        self.gpsDate = 0
#        self.gpsTime = 0
#        self.numSats = 0
        self.latitude = [32236562]
        self.longitude = [-110952322]
        self.speed = [0]*102
        self.dashTemp = [0]*102
#        self.batteryVoltage = 0
#        self.xbeeSignalStrength = 0
        self.frontBrakeAvg = [0]
        self.frontBrakeMax = [0]
        self.rearBrakeAvg = [0]
        self.rearBrakeMax = [0]
        self.steeringAvg = [0]
#        self.buttonPressed = 0
        
        # Rear Board Data
        self.primaryRPM = 0
        self.secondaryRPM = 0
        
        
        # Accelerometer
        self.accX = [0]
        self.maxX = [0]
        self.accY = [0]
        self.maxY = [0]
        self.accZ = [0]
        self.maxZ = [0]
        
        # 
        self.rearTemp = [0]

        


        
        self.hundred_array = list(range(0,102))
        
        self.gpsBackground = self.gpsCanvas.copy_from_bbox(self.gpsAxes.bbox)
        self.speedBackground = self.speedCanvas.copy_from_bbox(self.speedAxes.bbox)
        self.dashTempBackground = self.dashTempCanvas.copy_from_bbox(self.dashTempAxes.bbox)
        
        self.gpsPlot = self.gpsAxes.plot(self.longitude, self.latitude, '-')[0]
        self.speedPlot = self.speedAxes.plot(self.hundred_array,self.speed)[0]
        self.dashTempPlot = self.dashTempAxes.plot(self.hundred_array, self.dashTemp)[0]
        
        
        # Create Queues for talking to serial line asyncronously
        self.rx = queue.Queue()
        self.tx = queue.Queue()
        
        


    def StartSerial(self):
        self.listbox.insert(0, "Baud Rate: " + self.COMBaud.get())
        self.listbox.insert(0, "COM Port: " + self.COMPort.get())
        self.numActiveThreads.set('Threads\n' + str(threading.enumerate().__len__()))
        if (threading.enumerate().__len__()!=1):
            self.serialThread.join()
        #print(threading.enumerate().__len__())
        self.numActiveThreads.set('Threads\n' + str(threading.enumerate().__len__()))
        self.serialThread = SerialThread(self.COMPort, self.COMBaud, self.rx, self.tx)
        
        self.serialThread.start()
        self.numActiveThreads.set('Threads\n' + str(threading.enumerate().__len__()))
        self.process_serial()


    def StopSerial(self):
        self.listbox.insert(0, "Serial Stopped")
        if (threading.enumerate().__len__()!=1):
            self.serialThread.join()
        self.numActiveThreads.set('Threads\n' + str(threading.enumerate().__len__()))
        
    def PitNow(self):
        self.listbox.insert(0, "Pit Now")
        self.tx.put("<PIT NOW>\n")

    def PitNextLap(self):
        self.listbox.insert(0, "Pit Next Lap")
        self.tx.put("<PIT NEXT LAP>\n")


    def SendOnReturn(self, event):
        self.SendToSerial()

    def StartSerialOnReturn(self, event):
        self.StartSerial()

    def SendToSerial(self):
        text_contents = self.SerialSendTextBox.get()
        self.listbox.insert(0, text_contents)
        self.tx.put(text_contents)
        self.SerialSendTextBox.delete(0,END)

    def SendToDriver(self):
        text_contents = self.SerialSendTextBox.get()
        self.listbox.insert(0, text_contents)
        self.tx.put('<')
        self.tx.put(text_contents)
        self.tx.put('>')
        self.SerialSendTextBox.delete(0,END)


    def process_serial(self):
        text = StringVar()
        if self.rx.qsize():
#            self.listbox.delete(0,END)
            try:
                dataString = self.rx.get()
                
            except Queue.Empty:
                pass
                
            self.listbox.insert(0, dataString)
            data = dataString.split(bytes(', ','UTF-8'))
            print(data.__len__())
            if(data.__len__()==18 or data.__len__()==28):
                try:
                    i = 0
                    # Dash Data
                    self.counter.set('Counter\n' + str(int(data[0])))
                    i = 1
                    self.gpsDate.set('Date\n' + str(int(data[1])))
                    i = 2
                    self.gpsTime.set('Time\n' + str(int(data[2])))
                    i = 3
                    self.numSats.set('Sats\n' + str(int(data[3])))
                    if (float(data[4])/1000000 < 100 and float(data[5])/1000000 < 200):
                        i = 4
                        self.latitude.append(int(data[4]))
                        self.currentLatitude.set('Latitude\n' + str(int(data[4])))
                        i = 5
                        self.longitude.append(int(data[5]))
                        self.currentLongitude.set('Longitude\n' + str(int(data[5])))
                    i = 6
                    self.speed.append(float(data[6]))
                    self.currentSpeed.set('Speed\n' + str(float(data[6])))
                    self.currentSpeed.set('Speed\n' + str(float(data[6])))
                    i = 7
                    self.dashTemp.append(float(data[7]))
                    self.currentDashTemp.set('Dash Temp\n' + str(float(data[7])) + 'C')
                    i = 8
                    self.batteryVoltage.set('Batt\n' + str(int(data[8])))
                    i = 9
                    self.xbeeSignalStrength.set('XBee\n' + str(int(data[9])))
                    i = 10
                    self.frontBrakeAvg.append(float(data[10]))
                    i = 11
                    self.frontBrakeMax.append(int(data[11]))
                    i = 12
                    self.rearBrakeAvg.append(float(data[12]))
                    i = 13
                    self.rearBrakeMax.append(int(data[13]))
                    i = 14
                    self.steeringAvg.append(float(data[14]))
                    i = 15
    #                    self.buttonPressed = int(data[15])
                    i = 16
    #                    
    #                    # Rear Board Data
    #                    self.primaryRPM = 0
    #                    self.secondaryRPM = 0
    #                    
    #                    
    #                    # Accelerometer
    #                    self.accX = [0]
    #                    self.maxX = [0]
    #                    self.accY = [0]
    #                    self.maxY = [0]
    #                    self.accZ = [0]
    #                    self.maxZ = [0]
    #                    
    #                    # 
    #                    self.rearTemp = [0]
                except:
                    print('Exception Raised!' + str(i))
                    pass
                    
 

                
                self.gpsCanvas.restore_region(self.gpsBackground)
                self.gpsPlot.set_data(self.longitude[1:], self.latitude[1:])
                self.gpsAxes.draw_artist(self.gpsPlot)
                self.gpsCanvas.blit(self.gpsAxes.bbox)
                
                self.speedCanvas.restore_region(self.speedBackground)
                self.speedPlot.set_data(self.hundred_array[-101:], self.speed[-101:])
                self.speedAxes.draw_artist(self.speedPlot)
                self.speedCanvas.blit(self.speedAxes.bbox)
                
                self.dashTempCanvas.restore_region(self.dashTempBackground)
                self.dashTempPlot.set_data(self.hundred_array[-101:], self.dashTemp[-101:])
                self.dashTempAxes.draw_artist(self.dashTempPlot)
                self.dashTempCanvas.blit(self.dashTempAxes.bbox)
                

                
        self.after(100, self.process_serial)
        
    # Graceful Exit
    def destroy(e):
        sys.exit()



app = App()
app.mainloop()




