import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

standadult=np.load("./nparray-1.npy")
standchild=np.load("./nparray-2.npy")
walkingadult=np.load("./nparray-3.npy")
walkingchild=np.load("./nparray-4.npy")

fig=plt.figure()
ax1=fig.add_subplot(2,2,1)
ax2=fig.add_subplot(2,2,2)
ax3=fig.add_subplot(2,2,3)
ax4=fig.add_subplot(2,2,4)

ax1.set_ylabel("standadult")
ax2.set_ylabel("standchild")
ax3.set_ylabel("walkingadult")
ax4.set_ylabel("walkingchild")

#b, a = signal.butter(2, 5, btype="lowpass",fs=100)
b, a = signal.butter(6, (15,25), btype="bandpass",fs=100)
res1=signal.lfilter(b,a,standadult)
res2=signal.lfilter(b,a,standchild)
res3=signal.lfilter(b,a,walkingadult)
res4=signal.lfilter(b,a,walkingchild)

overlap=60
NFFt=64
ax1.specgram(res1, NFFT=NFFt, Fs=100, noverlap=overlap, detrend="mean")
ax2.specgram(res2, NFFT=NFFt, Fs=100, noverlap=overlap, detrend="mean")
ax3.specgram(res3, NFFT=NFFt, Fs=100, noverlap=overlap, detrend="mean")
ax4.specgram(res4, NFFT=NFFt, Fs=100, noverlap=overlap, detrend="mean")

plt.show()