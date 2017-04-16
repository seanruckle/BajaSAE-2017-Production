#!/usr/bin/env python3

import numpy as np
import time
import matplotlib
matplotlib.use('TKAgg')
#matplotlib.use('GTKAgg')
from matplotlib import pyplot as plt

import serial
import sys




def run(niter=10000):
    """
    Display the simulation using matplotlib, using blit() for speed
    """
    # serial settings
    # TODO: Automate detection of arduino / allow user to choose
    ser = serial.Serial('/dev/ttyUSB1', 115200)
    if(ser.isOpen()):
        ser.close()
    ser.open()



    fig, (ax, ax1) = plt.subplots(1, 2)
    #ax.set_aspect('equal')
    ax.set_xlim(0, 500)
    ax.set_ylim(0, 100)
    ax.hold(True)
    
    ax1.set_xlim(-10000000, 10000000)
    ax1.set_ylim(-10000000, 10000000)
    ax1.hold(True)
    
    
    #rw = randomwalk()
    #x, y = next(rw)
    x = [0]
    y = [0]
    z = [0]
    counter = [0]
    temperature = [0]
    latitude = [0]
    longitude = [0]
    
    # maximize
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    
    plt.show(False)
    plt.draw()

    # cache the background
    background1 = fig.canvas.copy_from_bbox(ax.bbox)
    background2 = fig.canvas.copy_from_bbox(ax1.bbox)
    tempPlot = ax.plot(counter, temperature, '-')[0]
    accPlot = ax1.plot(x,y, 'o')[0]
    tic = time.time()

    for ii in range(niter):
        
        # update the xy data
        data = ser.readline().split(bytes(', ','UTF-8'))
        print(data)
        if(data.__len__()==17):
            counter.append(int(data[0]))
            temperature.append(float(data[1]))
            x.append(float(data[9]))
            y.append(float(data[10]))
            z.append(float(data[11]))
            

        tempPlot.set_data(counter, temperature)
        accPlot.set_data(x,y)
        

        # restore background
        fig.canvas.restore_region(background1)
        fig.canvas.restore_region(background2)

        # redraw just the points
        ax.draw_artist(tempPlot)
        ax1.draw_artist(accPlot)

        # fill in the axes rectangle
        fig.canvas.blit(ax.bbox)
        
        fig.canvas.blit(ax1.bbox)

    #plt.close(fig)
    print("Average FPS: {:.2f}".format(niter / (time.time() - tic)))

if __name__ == '__main__':
    run()
