#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 09:15:44 2021

@author: jamiejohnston
"""

#%%%
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats




def IDcheck(ID):
    if len(ID) != 9:
        print("you have not entered your student number correctly, ensure it has only 9 characters, then run this again")
        return
    IDcode = np.zeros(len(ID))
    for i in range(len(ID)):
        IDcode[i]=ID[i]
    return IDcode



## make a spike waveform in a 60 point window
def lor(x,a,x0,b):
    return a/(((x-x0)**2)+b)

def decay(x,x0,a,tau1,tau2):
    return a*(-np.exp((-(x-x0))/tau1)+np.exp((-(x-x0))/tau2))

def gaus(x,a,b,c):
    return a*np.exp(-((x-b)**2/2*c**2))

def spikeWave(ahp):
    sampleRate = 10000
    xs = np.arange(0,0.006,1/sampleRate)
    spike=np.zeros(60)
    spike=lor(xs,0.00000008,0.002,0)
    spike[23:59]=decay(xs[23:59],0.0023,-(ahp), 0.00022,0.0004)
    spike[20]=11
    return spike

def getNoisey():
    sampleRate = 100000
    xs = np.arange(0,0.006,1/sampleRate)
    spike=np.zeros(600)
    spike[230:590]=decay(xs[230:590],0.0023,-(1), 0.00022,0.0004)
    xs=np.arange(0,600,1)
    spike2=np.zeros(600)
    spike2=gaus(xs,1,206,0.1)
    spike+=spike2
    spike*=80
    spike-=70
    nn=np.random.normal(0,9,600)
    spike+=nn
    out=spike[100:350]
    return out

def getNoisey1():
#    IDcode=IDcheck(ID)
    spike = spikeWave2(5)*7.5

    # data=np.zeros(600)
    # data[70:130]+=spike
    spike-=70
    nn = np.random.normal(0,10,600)

    return spike+nn


#%%



def getSpike(ID):

    if len(ID) != 9:
        print("you have not entered your student number correctly, ensure it has only 9 characters, then run this again")
        return

    IDcode=IDcheck(ID)
    spike = spikeWave(15)
    sampleRate = 10000
    sponRate = IDcode[-2]+IDcode[-3]+2
    contra = sponRate+(IDcode[-4]+IDcode[-1]+30)
    
    duration = 5
    start = 0
    data = np.random.normal(0,0.5,150000)
    SponRateinSP = 1/(sponRate/sampleRate)
    contraSP = 1/(contra/sampleRate)
    
    durationinSP = duration*sampleRate
    
    numberOfStim = int(round(durationinSP/SponRateinSP))
    numberOfContra = int(round(durationinSP/contraSP))
    
    poiss = np.random.exponential(SponRateinSP,numberOfStim)
    poissContra = np.random.exponential(contraSP,numberOfContra)
    
    timeList =np.cumsum(poiss)
    timeList = [i for i in timeList if i<duration*sampleRate-60]
    timeList= np.asarray(timeList)
    timeList = timeList[np.insert(np.diff(timeList),0,60)>20]
    for t in timeList:
        t=int(round(t))
        data[t:t+60]+=spike
    timeListCon =np.cumsum(poissContra)
    timeListCon = [i for i in timeListCon if i<duration*sampleRate-60]
    timeListCon= np.asarray(timeListCon)
    timeListCon = timeListCon[np.insert(np.diff(timeListCon),0,60)>20]
    for t in timeListCon:
        t=int(round(t))+50000
        data[t:t+60]+=spike
    for t in timeList:
        t=int(round(t))+100000
        data[t:t+60]+=spike
        
    return data

def getfibres(ID):
    IDcode=IDcheck(ID)
    for i in range(40):
        np.savetxt('Fibre data/CV_'+str(i)+'.csv',fibredata(IDcode))
    
def fibredata(IDcode):
    if IDcode[-2] < 4:
        a = np.concatenate([np.random.normal(1.25,0.5,1), 
                        np.random.normal(100,10,1), np.random.normal(60,10,1)])
    elif 3<IDcode[-2]<7:
        a = np.concatenate([np.random.normal(100,10,1), np.random.normal(60,10,1),
                       np.random.normal(1.25,0.5,1),])
    elif IDcode[-2]>6:
        a = np.concatenate([np.random.normal(60,10,1),np.random.normal(1.25,0.5,1),
                       np.random.normal(100,10,1),])        
    return a


def getCircadian(ID):
    if len(ID) != 9:
        print("you have not entered your student number correctly, ensure it has only 9 characters, then run this again")
        return
    IDcode=IDcheck(ID)


    for i in range(35):

        if i<(10+IDcode[-1]+IDcode[-2]):
            sponRate = 100
            duration = 720
            numberOfStim = int(duration/sponRate)
            poiss = np.random.exponential(sponRate,numberOfStim)
            timeList1 =np.cumsum(poiss)
            timeList1 = np.asarray([i for i in timeList1 if i<duration])
            timeList1/=60

            sponRate = 5
            duration = 720
            numberOfStim = int(duration/sponRate)
            poiss = np.random.exponential(sponRate,numberOfStim)
            timeList2 =np.cumsum(poiss)
            timeList2 = np.asarray([i for i in timeList2 if i<duration])
            timeList2/=60
            timeList2+=12
            timeList=np.concatenate((timeList1,timeList2),axis=0)
        else:
            sponRate = 100
            duration = 900
            numberOfStim = int(duration/sponRate)
            poiss = np.random.exponential(sponRate,numberOfStim)
            timeList1 =np.cumsum(poiss)
            timeList1 = np.asarray([i for i in timeList1 if i<duration])
            timeList1/=60

            sponRate = 5
            duration = 540
            numberOfStim = int(duration/sponRate)
            poiss = np.random.exponential(sponRate,numberOfStim)
            timeList2 =np.cumsum(poiss)
            timeList2 = np.asarray([i for i in timeList2 if i<duration])
            timeList2/=60
            timeList2+=12
            timeList2+=3
            timeList=np.concatenate((timeList1,timeList2),axis=0)

        out=str(i)
        if len(out)==1:
            out="0"+str(i)

        np.savetxt('Circadian data/Day_'+out+'.csv',timeList)

def getExercise(ID):
    if len(ID) != 9:
        print("you have not entered your student number correctly, ensure it has only 9 characters, then run this again")
        return
    IDcode=IDcheck(ID)


    for i in range(35):

        if i<(8+IDcode[-1]+IDcode[-2]):
            sponRate = 100
            duration = 720
            numberOfStim = int(duration/sponRate)
            poiss = np.random.exponential(sponRate,numberOfStim)
            timeList1 =np.cumsum(poiss)
            timeList1 = np.asarray([i for i in timeList1 if i<duration])
            timeList1/=60

            sponRate = 5
            duration = 720
            numberOfStim = int(duration/sponRate)
            poiss = np.random.exponential(sponRate,numberOfStim)
            timeList2 =np.cumsum(poiss)
            timeList2 = np.asarray([i for i in timeList2 if i<duration])
            timeList2/=60
            timeList2+=12
            timeList=np.concatenate((timeList1,timeList2),axis=0)
        else:
            sponRate = 98
            duration = 720
            numberOfStim = int(duration/sponRate)
            poiss = np.random.exponential(sponRate,numberOfStim)
            timeList1 =np.cumsum(poiss)
            timeList1 = np.asarray([i for i in timeList1 if i<duration])
            timeList1/=60

            sponRate = 3.6
            duration = 720
            numberOfStim = int(duration/sponRate)
            poiss = np.random.exponential(sponRate,numberOfStim)
            timeList2 =np.cumsum(poiss)
            timeList2 = np.asarray([i for i in timeList2 if i<duration])
            timeList2/=60
            timeList2+=12
            timeList=np.concatenate((timeList1,timeList2),axis=0)

        out=str(i)
        if len(out)==1:
            out="0"+str(i)

        np.savetxt('Exercise data/Day_'+out+'.csv',timeList)



#%%
def getDrug(ID):
    if len(ID) != 9:
        print("you have not entered your student number correctly, ensure it has only 9 characters, then run this again")
        return
    IDcode=IDcheck(ID)
    tt = np.arange(0,100,1)
    data = ((IDcode[-4]+9)*30)*np.exp(1)**-(tt/((IDcode[-1]+2)*3))
    nn = np.random.normal(0,(IDcode[-6]+8),100)
    data+=nn

    return data


#%%

def getCellSize(ID):
    if len(ID) != 9:
        print("you have not entered your student number correctly, ensure it has only 9 characters, then run this again")
        return
    IDcode=IDcheck(ID)
    data1 = np.random.lognormal(IDcode[-3]+1,0.55, size=int(900+IDcode[-4]**2))
    return data1


def getmRNAs(ID):
    if len(ID) != 9:
        print("you have not entered your student number correctly, ensure it has only 9 characters, then run this again")
        return
    IDcode=IDcheck(ID)
    centre = (IDcode[-1]+55+IDcode[-2]*3)*10
    scale = 1+(IDcode[-3]/10) # IDcode[-1]
    data1 = np.random.lognormal(centre,scale,int(900+IDcode[-4]**2))
    data2 = np.zeros((len(data1),2))
    data2[:,0]=data1[:]
    data2[:,1]= np.random.lognormal(centre+scale*1.5,scale,int(900+IDcode[-4]**2))
    
    return data2

def getPlatelets(ID):
    if len(ID) != 9:
        print("you have not entered your student number correctly, ensure it has only 9 characters, then run this again")
        return
    IDcode=IDcheck(ID)
    count = 140000 - (5+IDcode[-2]/2)*1000
    h = stats.skewnorm.rvs(-2, count, scale=10000, size=900)
    f = stats.skewnorm.rvs(-9, count+(5+IDcode[-2]/2)*1000, scale=10000, size=900)
    scale = 1+(IDcode[-3]/10) # IDcode[-1]
    centre = IDcode[-3]
    data1 = np.random.lognormal(centre,scale,int(900+IDcode[-4]**2))
    data2 = np.zeros((len(data1),2))
    data2[:,0]=data1[:]
    data2[:,1]= np.random.lognormal(centre+scale*1.5,scale,int(900+IDcode[-4]**2))
    data2 = np.vstack((h,f))
    return data2

def dataFolder(ID):
    if len(ID) != 9:
        print("you have not entered your student number correctly, ensure it has only 9 characters, then run this again")
        return
    IDcode = np.zeros(len(ID))
    saveContents = ID[::-1]
    for i in range(len(ID)):
        IDcode[i]=saveContents[i]
    saveList=[3,2,4,1,8,0,6,7,5]
    saveName='ABCDEFGHI'
    for i in saveList:
        a= np.array([saveContents[i]],dtype='int')
        np.savetxt('Data sets/Data_'+saveName[i]+'.csv',a)
    a=np.array([12])
    b=np.array([24])
    np.savetxt('Data sets/Data_J.txt',a)
    np.savetxt('Data sets/Data_K.txt',b)

#%%
