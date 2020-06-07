import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import math

standadult=np.load("./nparray-1.npy")
standchild=np.load("./nparray-2.npy")
walkingadult=np.load("./nparray-3.npy")
walkingchild=np.load("./nparray-4.npy")

fig=plt.figure()
ax1=fig.add_subplot(4,1,1)
ax2=fig.add_subplot(4,1,2)
ax3=fig.add_subplot(4,1,3)
ax4=fig.add_subplot(4,1,4)

b, a = signal.butter(6, (15,25), btype="bandpass",fs=100)

res1=abs(signal.lfilter(b,a,standadult))
res2=abs(signal.lfilter(b,a,standchild))
res3=abs(signal.lfilter(b,a,walkingadult))
res4=abs(signal.lfilter(b,a,walkingchild))

b, a = signal.butter(2, 2, btype="low",fs=100)

res1=signal.lfilter(b,a,res1)
res2=signal.lfilter(b,a,res2)
res3=signal.lfilter(b,a,res3)
res4=signal.lfilter(b,a,res4)

ax1.plot(standadult, alpha=0.2)
ax1.plot(res1)
ax2.plot(standchild, alpha=0.2)
ax2.plot(res2)
ax3.plot(walkingadult, alpha=0.2)
ax3.plot(res3)
ax4.plot(walkingchild, alpha=0.2)
ax4.plot(res4)
ax1.legend(('standAdult', 'lfilter'), loc='best')
ax2.legend(('standChild', 'lfilter'), loc='best')
ax3.legend(('walkAdult', 'lfilter'), loc='best')
ax4.legend(('walkChild', 'lfilter'), loc='best')

plt.show()