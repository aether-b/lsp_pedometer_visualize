#!/usr/bin/env python
import numpy as np
from scipy import signal
import socket
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import _thread
import math


RATE = 100 #sampling freq
TIMEBUFFER = 30 #seconds
BUFFERSAMPLES = RATE*TIMEBUFFER
MINSTEPINTERVAL = 0.2 #seconds between steps. Detect
BUFFMININTERVAL = int(MINSTEPINTERVAL * RATE) 
nochange=False

steps=0
prevSample=0.0
dire="UP"
downVal=0
MINPEAKHEIGHT=0.07
def stepCount(currSample):
    global rfiltered, steps, prevSample, dire, downVal, MINPEAKHEIGHT
    if currSample>prevSample:
        if dire=="DOWN": #signal going UP (inflection)
            dire="UP"
            downVal=prevSample
    elif currSample<prevSample:
        if dire=="UP": #signal going down (inflection) <- peak
            dire="DOWN"
            print(prevSample-downVal)
            if (prevSample-downVal)>MINPEAKHEIGHT:
                steps+=2
    prevSample=currSample

def bandpassf(inputt):
    global nochange
    if nochange:
        return rfiltered
    b, a = signal.butter(6, (15,25), btype="bandpass",fs=100)
    resp=abs(signal.lfilter(b,a,inputt))
    stepCount(resp[-1:])
    nochange=True
    return resp

def lowpassf(inputt):
    b, a = signal.butter(2, 2, btype="low",fs=100)
    return signal.lfilter(b,a,inputt)

accel=[np.zeros(BUFFERSAMPLES),np.zeros(BUFFERSAMPLES),np.zeros(BUFFERSAMPLES),np.zeros(BUFFERSAMPLES)]
rfiltered=rfiltered=lowpassf(bandpassf(accel[3]))

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
liner, = axr.plot(rfiltered)
charttextr=axr.text(3000,0, '0 steps', fontsize=12)
#axr.set_ylabel("Specgram")
#Pxx, freqs, bins, im = axr.specgram(accel[3], NFFT=16, Fs=100, noverlap=8)
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
    global accel,BUFFERSAMPLES, rfiltered, nochange
    acc=getAccel(xmlst)
    sumSqrs=0
    for n in range(0,3):
        accel[n]=np.append(accel[n],acc[n])
        #print("len(accel[" + str(n) + "]) =" + str(len(accel[n])), np.append(accel[n],acc[n]))
        accel[n]=accel[n][-BUFFERSAMPLES:]
        sumSqrs+=math.pow(acc[n],2)
    accel[3]=np.append(accel[3],math.sqrt(sumSqrs))
    accel[3]=accel[3][-BUFFERSAMPLES:]
    nochange=False

def update(data):
    global accel, steps
    rfiltered=lowpassf(bandpassf(accel[3]))
    if np.std(accel[0])>0:
        axx.set_ylim(np.min(accel[0]),np.max(accel[0]))
    linex.set_ydata(accel[0])
    if np.std(accel[1])>0:
        axy.set_ylim(np.min(accel[1]),np.max(accel[1]))
    liney.set_ydata(accel[1])
    if np.std(accel[2])>0:
        axz.set_ylim(np.min(accel[2]),np.max(accel[2]))
    linez.set_ydata(accel[2])
    if np.std(accel[3])>0:
        axr.set_ylim(np.min(rfiltered),np.max(rfiltered))
    liner.set_ydata(rfiltered)
    charttextr.set_text(str(steps) + " steps")
    #arr = axr.specgram(accel[3], NFFT=16, Fs=100, noverlap=8)[0]
    #im.set_array(arr)
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

ani = animation.FuncAnimation(fig, update, interval=500)
plt.show()