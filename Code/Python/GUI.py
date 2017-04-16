#!/usr/bin/env python3

from tkinter import *
import threading, queue, serial, matplotlib, sys, time
from matplotlib import pyplot as plt
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class SerialThread(threading.Thread):
    def __init__(self, COMPort,COMBaud, RXqueue, TXqueue):
        self._stopevent = threading.Event()
        threading.Thread.__init__(self)
        self.baud = COMBaud
        self.COM = COMPort
        self.rx = RXqueue
        self.tx = TXqueue
    def run(self):
        s = serial.Serial(self.COM.get(), self.baud.get())
        if(s.isOpen()):
            s.close()
        s.open()
        while not self._stopevent.isSet():
            if s.inWaiting():
                text = s.readline(s.inWaiting())
                self.rx.put(text)
            if self.tx.qsize():
                try:
                    s.write(bytes(self.tx.get(),'UTF-8'))
                except queue.Empty:
                    pass
    def join(self, timeout=None):
        """ Stop the thread. """
        self._stopevent.set(  )
        threading.Thread.join(self, timeout)


class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Baja GUI")
        
        # Root level frames
        self.controlFrame = Frame(self, bg='blue', borderwidth=5)
        self.displayFrame = Frame(self, bg='red', borderwidth=5)
        # Serial Control Frame
        self.serialFrame = Frame(self.controlFrame, borderwidth=5)
        
        self.COMPort = StringVar()
        self.COMPortTextBox = Entry(self.serialFrame, textvariable = self.COMPort)
        self.COMPort.set('/dev/ttyUSB0')
        self.COMBaud = StringVar()
        self.COMBaudTextBox = Entry(self.serialFrame, textvariable = self.COMBaud)
        self.COMBaud.set('112500')
        self.COMButton = Button(self.serialFrame, text = "Start Serial", command = self.StartSerial)
        
        self.SerialSendButton = Button(self.serialFrame, text = "Send", command = self.SendToSerial)
        self.SerialSendTextBox = Entry(self.serialFrame)

        # Extra Button
        self.button2 = Button(self.controlFrame, text = "button2", command = self.Button2)


        
        self.NumThreadsTextBox = Entry(self.displayFrame)

        self.scrollbar = Scrollbar(self.controlFrame, orient=VERTICAL)
        self.listbox = Listbox(self.controlFrame, yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.listbox.yview)
        
        # Set to full screen
        self.attributes('-fullscreen', True)
        
        # Bind <Return> Keypress to text boxes
        self.SerialSendTextBox.bind("<Return>", self.SendOnReturn)
        self.COMBaudTextBox.bind("<Return>", self.StartSerialOnReturn)
        
        # Pack Serial Controls into Serial Frame
        self.SerialSendTextBox.pack(side = LEFT)
        self.SerialSendButton.pack(side = LEFT)
        self.COMPortTextBox.pack(side = LEFT)
        self.COMBaudTextBox.pack(side = LEFT)
        self.COMButton.pack(side = LEFT)
        
        # Pack Control Widgets into Control Frame
        self.serialFrame.pack(side = TOP)
        
        self.button2.pack(side = LEFT)


        self.scrollbar.pack(side = RIGHT, fill = Y)
        self.listbox.pack(side = RIGHT, fill = X, expand=1)
        
        # Pack Control Frame into root
        self.controlFrame.pack(side = TOP, fill=X, expand = 1)
        
        
        # Top Level Display Frames
        self.leftDisplayFrame = Frame(self.displayFrame, borderwidth=5)
        self.rightDisplayFrame = Frame(self.displayFrame, borderwidth=5)
        
        # Inside Left Display Frames
        self.topLeftDisplayFrame = Frame(self.leftDisplayFrame, bg='red', borderwidth=5)
        self.middleLeftDisplayFrame = Frame(self.leftDisplayFrame, bg='green', borderwidth=5)
        self.bottomLeftDisplayFrame = Frame(self.leftDisplayFrame, bg='blue', borderwidth=5)
        
        # Inside Top Left Display Frames
        
        # Inside Middle Left Display Frames
        self.brakeFrame = Frame(self.middleLeftDisplayFrame, borderwidth=5)
        
        # Inside Bottom Left Display Frames
        self.driveTrainTempFrame = Frame(self.bottomLeftDisplayFrame, borderwidth=5)
        self.driveTrainRPMFrame = Frame(self.bottomLeftDisplayFrame, borderwidth=5)
        
        # Inside Rigt Display Frames
        self.shieldTempFrame = Frame(self.rightDisplayFrame, borderwidth=5, bg='cyan')
        self.shieldHealthFrame = Frame(self.rightDisplayFrame, borderwidth=5, bg='magenta')
        
        # Construct Items for Display Frame
        self.gpsFigure, self.gpsAxes = plt.subplots()
        self.speedFigure, self.speedAxes = plt.subplots()
        self.rpmFigure, self.rpmAxes = plt.subplots()
        self.dashTempFigure, self.dashTempAxes = plt.subplots()
        self.rearTempFigure, self.rearTempAxes = plt.subplots()
        self.gearTempFigure, self.gearTempAxes = plt.subplots()
        self.cvtTempFigure, self.cvtTempAxes = plt.subplots()
        self.battFigure, self.battAxes = plt.subplots()
        self.frontBrakeFigure, self.frontBrakeAxes = plt.subplots()
        self.rearBrakeFigure, self.rearBrakeAxes = plt.subplots()
        self.steeringFigure, self.steeringAxes = plt.subplots()
        self.buttonFigure, self.buttonGraph = plt.subplots()
        self.accFigure, self.accAxes = plt.subplots()
        
        
        # GPS Axes Setup
        self.gpsAxes.set_title('GPS')
        self.gpsAxes.set_xlim(0,500)
        self.gpsAxes.set_ylim(0,100)
        self.gpsAxes.hold(True)
        
        self.gpsCanvas = FigureCanvasTkAgg(self.gpsFigure, master=self.rightDisplayFrame)
        self.gpsCanvas.show()
#        
        
        
        # speed Axes Setup
        self.speedAxes.set_title('Speed')
        self.speedAxes.set_xlim(0,500)
        self.speedAxes.set_ylim(0,100)
        self.speedAxes.hold(True)
        
        self.speedCanvas = FigureCanvasTkAgg(self.speedFigure, master=self.topLeftDisplayFrame)
        self.speedCanvas.show()
#        

        
        
        # Dash Temperature Axes Setup
        self.dashTempAxes.set_title('Dash Temperature')
        self.dashTempAxes.set_xlim(0,500)
        self.dashTempAxes.set_ylim(0,100)
        self.dashTempAxes.hold(True)
        
        self.dashTempCanvas = FigureCanvasTkAgg(self.dashTempFigure, master=self.shieldTempFrame)
        self.dashTempCanvas.show()
#        
        
        
        # Rear Temperature Axes Setup
        self.rearTempAxes.set_title('Rear Temperature')
        self.rearTempAxes.set_xlim(0,500)
        self.rearTempAxes.set_ylim(0,100)
        self.rearTempAxes.hold(True)
        
        self.rearTempCanvas = FigureCanvasTkAgg(self.rearTempFigure, master=self.shieldTempFrame)
        self.rearTempCanvas.show()
#        
        
        
        # Gearbox Temperature Axes Setup
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
        self.accAxes.set_title('Acceleration 2-D')
        self.accAxes.set_xlim(-10000000, 10000000)
        self.accAxes.set_ylim(-10000000, 10000000)
        self.accAxes.hold(True)
        
        self.accCanvas = FigureCanvasTkAgg(self.accFigure, master=self.middleLeftDisplayFrame)
        self.accCanvas.show()
#        
        
        
        
        # Layout
        # Pack Brake Pressure
        
        # Pack Drive Train RPM
        
        # Pack Drive Train Temp
        self.gearTempCanvas.get_tk_widget().pack(side=LEFT, fill=Y, expand=1)
        self.gearTempCanvas._tkcanvas.pack(side=LEFT, fill=Y, expand=1)
        self.cvtTempCanvas.get_tk_widget().pack(side=LEFT, fill=Y, expand=1)
        self.cvtTempCanvas._tkcanvas.pack(side=LEFT, fill=Y, expand=1)
        
        # Pack stuff into top left
        self.speedCanvas.get_tk_widget().pack(side=LEFT, fill=Y, expand=1)
        self.speedCanvas._tkcanvas.pack(side=LEFT, fill=Y, expand=1)
        
        # Pack stuff into middle left
        self.accCanvas.get_tk_widget().pack(side=LEFT, fill=Y, expand=1)
        self.accCanvas._tkcanvas.pack(side=LEFT, fill=Y, expand=1)
        self.brakeFrame.pack(side=LEFT, fill=Y, expand=1)
        
        # Pack stuff into bottom left
        self.driveTrainTempFrame.pack(side=TOP, fill=X, expand=1)
        self.driveTrainRPMFrame.pack(side=TOP, fill=X, expand=1)
        
        
        # Pack Left Display
        self.topLeftDisplayFrame.pack(side=TOP, fill=X, expand=1)
        self.middleLeftDisplayFrame.pack(side=TOP, fill=X, expand=1)
        self.bottomLeftDisplayFrame.pack(side=TOP, fill=X, expand=1)
        
        
        # Pack Shield Temp
        self.dashTempCanvas.get_tk_widget().pack(side=LEFT, fill=Y, expand=0)
        self.dashTempCanvas._tkcanvas.pack(side=LEFT, fill=Y, expand=0)
        self.rearTempCanvas.get_tk_widget().pack(side=LEFT, fill=Y, expand=0)
        self.rearTempCanvas._tkcanvas.pack(side=LEFT, fill=Y, expand=0)
        
        # Pack Shield Health
        
        # Pack stuff inside right display
        self.gpsCanvas.get_tk_widget().pack(side=TOP, fill=X, expand=1)
        self.gpsCanvas._tkcanvas.pack(side=TOP, fill=X, expand=1)
        self.shieldTempFrame.pack(side=TOP, fill=X, expand=1)
        self.shieldHealthFrame.pack(side=TOP, fill=X, expand=1)
        
        
        
        # Pack Display Frame
        self.leftDisplayFrame.pack(side=LEFT, fill=Y, expand=1)
        self.rightDisplayFrame.pack(side=LEFT, fill=Y, expand=1)
        
        # Pack Display Into Root
        self.displayFrame.pack(side=TOP, fill=X, expand=1)
        
        
        # Initialize Data Variables
        self.x = [0]
        self.y = [0]
        self.z = [0]
        self.counter = [0]
        self.temperature = [0]
        self.latitude = [0]
        self.longitude = [0]
        
        
        
        
        
        
        
        
        
        # Pack Display Frame into root
        self.displayFrame.pack(side = BOTTOM, fill=BOTH, expand = 1)
        
        
        # Create Queues for talking to serial line asyncronously
        self.rx = queue.Queue()
        self.tx = queue.Queue()
        


    def StartSerial(self):
        self.listbox.insert(END, self.COMBaud.get())
        self.listbox.insert(END, self.COMPort.get())
        print(threading.enumerate().__len__())
        if (threading.enumerate().__len__()!=1):
            self.serialThread.join()
        print(threading.enumerate().__len__())
        self.serialThread = SerialThread(self.COMPort, self.COMBaud, self.rx, self.tx)
        
        self.serialThread.start()
        print(threading.enumerate().__len__())
        self.process_serial()


    def Button2(self):
        self.listbox.insert(END, "button2 pressed")


    def SendOnReturn(self, event):
        self.SendToSerial()

    def StartSerialOnReturn(self, event):
        self.StartSerial()

    def SendToSerial(self):
        text_contents = self.SerialSendTextBox.get()
        self.listbox.insert(END, text_contents)
        self.tx.put(text_contents)
        self.SerialSendTextBox.delete(0,END)

    def process_serial(self):
        while self.rx.qsize():
            try:
                #self.text.delete(1.0, 'end')
                self.listbox.insert('end', self.rx.get())
            except Queue.Empty:
                pass
        self.after(100, self.process_serial)
        
    # Graceful Exit
    def destroy(e):
        sys.exit()



app = App()
app.mainloop()




