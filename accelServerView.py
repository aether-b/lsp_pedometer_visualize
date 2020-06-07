#!/usr/bin/env python
import numpy as np
import socket
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import _thread
import math


RATE = 100 #sampling freq
TIMEBUFFER = 30 #seconds
BUFFERSAMPLES = RATE*TIMEBUFFER

accel=[np.zeros(BUFFERSAMPLES),np.zeros(BUFFERSAMPLES),np.zeros(BUFFERSAMPLES),np.zeros(BUFFERSAMPLES)]

fig=plt.figure()
axx=fig.add_subplot(4,1,1)
axy=fig.add_subplot(4,1,2)
axz=fig.add_subplot(4,1,3)
axr=fig.add_subplot(4,1,4)

linex, = axx.plot(accel[0],'r-')
axx.set_ylabel("X-axis")
liney, = axy.plot(accel[1],'y-')
axy.set_ylabel("Y-axis")
linez, = axz.plot(accel[2],'g-')
axz.set_ylabel("Z-axis")
#liner, = axr.plot(accel[3])
axr.set_ylabel("Specgram")
Pxx, freqs, bins, im = axr.specgram(accel[3], NFFT=16, Fs=100, noverlap=8)
#ax.set_ylim(0, 1)

def getAccel(xmlst):
    r=[np.zeros(1),np.zeros(1),np.zeros(1)]
    if xmlst.find("<Accelerometer")>0:
        findStr="Accelerometer"
        leng=16
    elif xmlst.find("<LinearAcceleration")>0:
        findStr="LinearAcceleration"
        leng=21
    else:
        return r
    for num in range(0,3):
        r[num]=float(xmlst[xmlst.find("<"+findStr+str(num+1)+">")+leng:xmlst.find("</"+ findStr + str(num+1) +">")])
    return r
def parser(xmlst):
    #global accel,BUFFERSAMPLES
    acc=getAccel(xmlst)
    sumSqrs=0
    for n in range(0,3):
        accel[n]=np.append(accel[n],acc[n])
        #print("len(accel[" + str(n) + "]) =" + str(len(accel[n])), np.append(accel[n],acc[n]))
        accel[n]=accel[n][-BUFFERSAMPLES:]
        sumSqrs+=math.pow(acc[n],2)
    accel[3]=np.append(accel[3],math.sqrt(sumSqrs))
    accel[3]=accel[3][-BUFFERSAMPLES:]

def update(data):
    global accel
    if np.std(accel[0])>0:
        axx.set_ylim(np.min(accel[0]),np.max(accel[0]))
    linex.set_ydata(accel[0])
    if np.std(accel[1])>0:
        axy.set_ylim(np.min(accel[1]),np.max(accel[1]))
    liney.set_ydata(accel[1])
    if np.std(accel[2])>0:
        axz.set_ylim(np.min(accel[2]),np.max(accel[2]))
    linez.set_ydata(accel[2])
    # if np.std(accel[3])>0:
    #    axr.set_ylim(np.min(accel[3]),np.max(accel[3]))
    # liner.set_ydata(accel[3])
    arr = axr.specgram(accel[3], NFFT=16, Fs=100, noverlap=8)[0]
    im.set_array(arr)
    #return line,

def udpServer():
    global accel
    port = 5555
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("192.168.0.4", port))
    print ("waiting on port 5555")
    while 1:
        data, addr = s.recvfrom(1024)
        if len(str(data))>40:
            #print(data)
            parser(str(data))
            #print(len(accel[0]))

try:
   _thread.start_new_thread( udpServer )
except:
   print ("Error: unable to start server.")

ani = animation.FuncAnimation(fig, update, interval=100)
plt.show()