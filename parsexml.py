import numpy as np

xmlstring="<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><NodeId>1</NodeId><Accelerometer><Accelerometer1>-0.1764984130859375</Accelerometer1><Accelerometer2>0.618194580078125</Accelerometer2><Accelerometer3>9.617721557617188</Accelerometer3></Accelerometer><TimeStamp>1591434002544</TimeStamp>"
accel=[np.empty(0),np.empty(0),np.empty(0)]

def getAccel(xmlst):
    r=[0.0,0.0,0.0]
    for num in range(0,3):
        r[num]=float(xmlst[xmlst.find("<Accelerometer"+str(num+1)+">")+16:xmlstring.find("</Accelerometer"+ str(num+1) +">")])
    return r
def parser(xmlst):
    acc=getAccel(xmlst)
    for n in range(0,3):
        accel[n]=np.append(accel[n],acc[n])
parser(xmlstring)    
print(accel)