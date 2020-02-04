import numpy as np
import matplotlib.pyplot as plt
import math
import statistics
import weatherapi
import time
#tempdata is a list of the avaerage daily temperature in degrees celsius
#wolpercentage is the percentage of wolbachia infected mosquitoes to add every time the average weekly temperature is between 29 and 32.5
class MosquitoWithWolbachia:
    def __init__(self, tempdata, wolpercentage):
        self.tempdata = tempdata
        self.wolpercentage = wolpercentage/100
        self.days = len(self.tempdata)
        self.dayslist = np.linspace(0,len(self.tempdata)-1,len(self.tempdata))
        self.Sh = [None]*self.days   #susceptible humans
        self.Eh = [None]*self.days   #exposed humans
        self.Ih = [None]*self.days   #infected humans
        self.Rh = [None]*self.days   #recovered humans
        self.An = [None]*self.days   #aquatic mosquitoes
        self.Sn = [None]*self.days   #susceptible mosquitoes
        self.En = [None]*self.days   #exposed mosquitoes
        self.In = [None]*self.days   #infected mosquitoes
        self.Aw = [None]*self.days   #aquatic mosquitoes infected with wolbachia
        self.Sw = [None]*self.days   #susceptible mosquitoes infected with wolbachia
        self.Ew = [None]*self.days   #exposed mosquitoes infected with wolbachia
        self.Iw = [None]*self.days   #infected mosquitoes infected with wolbachia
        self.Sh[0] = 100000.0        #initial population values:
        self.Eh[0] = 0.0
        self.Ih[0] = 0.0
        self.Rh[0] = 0.0
        self.An[0] = 10000.0
        self.Sn[0] = 10000.0
        self.En[0] = 0.0
        self.In[0] = 1.0
        self.Aw[0] = 0.0
        self.Sw[0] = 100.0
        self.Ew[0] = 0.0
        self.Iw[0] = 0.0
        self.carrycapacr = 3.0
        self.reinfectr = 0.08
        self.recoveryr = 0.2
        self.sigma = 0.02
        self.reproductiver = 1.25
        self.tranmaternal = 0.9
        self.maturationr = 0.1
        self.th = self.Sh[0]+self.Eh[0]+self.Ih[0]+self.Rh[0]   #total human population
        self.tn = self.th*self.carrycapacr                      #total mosquito population=humanpopulation*carryingcapacity
        self.tnw = self.th*self.carrycapacr                     #total wol-mosquito population=humanpopulation*carryingcapacity      
        self.bn, self.bw, self.tmh, self.thm, self.tauN, self.c, self.muNA, self.muN = self.tempDependentVariables()

    def getDaysList(self):
        return self.days, self.dayslist

    def getHumanPopulation(self):
        return self.Sh, self.Eh, self.Ih, self.Rh

    def getMosquitoNonWol(self):
        return self.An, self.Sn, self.En, self.In

    def getMosquitoWithWol(self):
        return self.Aw, self.Sw, self.Ew, self.Iw

    def getQuickModel(self):
        return self.Ih,self.In,self.Aw,self.Sw,self.tempdata

    def tempDependentVariables(self):
        bn = [None]*self.days    #biting rate
        bw = [None]*self.days    #biting rate for wolbachia mosquito
        tmh = [None]*self.days   #transmission chance mosquito to human
        thm = [None]*self.days   #transmission chance human to mosquito
        tauN = [None]*self.days  #mosquito maturation rate
        c = [None]*self.days     #extrinsic incubation period
        muNA = [None]*self.days  #aquatic mosquito death rate
        muN = [None]*self.days   #adult mosquito death rate
        for i in range(self.days):  
            if self.tempdata[i]>=21.00 and self.tempdata[i]<=32.00:
                bn[i]=0.0943+0.0043*self.tempdata[i]
                bw[i]=0.95*(0.0943+0.0043*self.tempdata[i])
            else:
                bn[i]=0.0
                bw[i]=0.0
            if self.tempdata[i]>=12.4 and self.tempdata[i]<=32.5:
                tmh[i]=0.001044*self.tempdata[i]*(self.tempdata[i]-12.286)*math.sqrt(abs(32.461-self.tempdata[i]))
            else:
                tmh[i]=0.0
            if self.tempdata[i]>=12.4 and self.tempdata[i]<=26.1:
                thm[i]=-0.9037+0.0729*self.tempdata[i]
            elif self.tempdata[i]<12.4 or self.tempdata[i]>32.5:
                thm[i]=0
            else:
                thm[i]=1
            heavis=0.57-0.43*math.cos((2*math.pi*self.dayslist[i])/365+(math.pi/4))
            if heavis<0:
                tauN[i]=0.0
            else:
                tauN[i]=(0.00483*self.tempdata[i]-0.00796)*(0.57-0.43*math.cos((2*math.pi*self.dayslist[i]/365+(math.pi/4))))
            c[i]=-0.1393+0.008*self.tempdata[i]
            muNA[i]=0.8692-0.159*self.tempdata[i]+0.01116*self.tempdata[i]**2-0.0003408*self.tempdata[i]**3+0.000003809*self.tempdata[i]**4
            muN[i]=(1/14)*(1-(0.6228)*(math.cos((2*math.pi)*(i+(20.61))/365)))
        return bn, bw, tmh, thm, tauN, c, muNA, muN
    
    def plotGraph(self):
        plt.subplot(3, 1, 1)
        plt.plot(self.dayslist,self.Sh, '-b', label="Susceptible Humans")
        plt.plot(self.dayslist,self.Ih, '-r', label="Infected Humans")
        plt.plot(self.dayslist,self.Eh, '-y', label="Exposed Humans")
        plt.plot(self.dayslist,self.Rh, '-g', label="Recovered Humans")
        plt.title("Mosquito Disease Model with Wolbachia")
        plt.legend(loc="lower right")

        plt.subplot(3,1,2)
        plt.plot(self.dayslist,self.An, 'c', label="Aquatic Mosquitoes")
        plt.plot(self.dayslist,self.Sn, 'm', label="Susceptible Mosquitoes")
        plt.plot(self.dayslist,self.En, 'r', label="Exposed Mosquitoes")
        plt.plot(self.dayslist,self.In, 'k', label="Infected Mosquitoes")
        plt.legend(loc="lower right")

        plt.subplot(3,1,3)
        plt.plot(self.dayslist,self.Aw, 'c', label="Aquatic Mosquitoes with W")
        plt.plot(self.dayslist,self.Sw, 'm', label="Susceptible Mosquitoes with W")
        plt.plot(self.dayslist,self.Ew, 'r', label="Exposed Mosquitoes with W")
        plt.plot(self.dayslist,self.Iw, 'k', label="Infected Mosquitoes with W")
        plt.xlabel("Days")
        plt.legend(loc="lower right")
        plt.show() 

    def runModel(self):
        for i in range(self.days):
            if i==0:
                #normalizing the populations
                self.Sh[0]=100000.0/self.th    
                self.Eh[0]=0/self.th
                self.Ih[0]=0/self.th
                self.Rh[0]=0/self.th
                self.An[0]=10000.0/self.tn
                self.Sn[0]=10000.0/self.tn
                self.En[0]=0.0/self.tn
                self.In[0]=1/self.tn
                self.Aw[0]=0/self.tnw
                self.Sw[0]=100/self.tnw
                self.Ew[0]=0/self.tnw
                self.Iw[0]=0/self.tnw
            else:
                fn=self.Sn[i-1]+self.En[i-1]+self.In[i-1]  #total non-wolbachia mosquito population
                fw=self.Sw[i-1]+self.Ew[i-1]+self.Iw[i-1]  #total wolbachia mosquito population
                #human compartmental differential equations:
                self.Sh[i]=self.Sh[i-1]+(-self.bn[i-1]*self.tmh[i-1]*self.carrycapacr*self.In[i-1]*self.Sh[i-1])-(self.bw[i-1]*0.5*self.tmh[i-1]*self.carrycapacr*self.Iw[i-1]*self.Sh[i-1])+self.reinfectr*self.Rh[i-1]
                self.Eh[i]=self.Eh[i-1]+((self.bn[i-1]*self.tmh[i-1]*self.carrycapacr*self.In[i-1]*self.Sh[i-1])+(self.bw[i-1]*0.5*self.tmh[i-1]*self.carrycapacr*self.Iw[i-1]*self.Sh[i-1])-self.recoveryr*self.Eh[i-1])
                self.Ih[i]=self.Ih[i-1]+(self.recoveryr*self.Eh[i-1]-self.sigma*self.Ih[i-1])
                self.Rh[i]=self.Rh[i-1]+(self.sigma*self.Ih[i-1])-self.reinfectr*self.Rh[i-1]
                #mosquito compartmental differential equations:
                self.An[i]=self.An[i-1]+(self.reproductiver*(fn**2)/(2*(fn+fw))*(1-(self.An[i-1]+self.Aw[i-1]))-(self.maturationr+(self.muNA[i-1]))*self.An[i-1])
                self.Sn[i]=self.Sn[i-1]+((self.maturationr*self.An[i-1]/2)+(1-self.tranmaternal)*self.maturationr*self.Aw[i-1]/2-(self.bn[i-1]*fn*self.Ih[i-1]+self.muN[i-1])*self.Sn[i-1])
                self.En[i]=self.En[i-1]+((self.bn[i-1]*self.thm[i-1]*self.Ih[i-1]*self.Sn[i-1])-((self.c[i-1])+self.muN[i-1])*self.En[i-1])
                self.In[i]=self.In[i-1]+((self.c[i-1])*self.En[i-1]-self.muN[i-1]*self.In[i-1])
                #mosquito infected with wolbachia compartmental differential equations:
                self.Aw[i]=self.Aw[i-1]+(0.95*self.reproductiver*(fn/2)*(1-(self.An[i-1]+self.Aw[i-1]))-(self.maturationr+self.muN[i-1])*self.Aw[i-1])
                if i>=7:  #adding wolpercentage% wolbachia if the average temperature for the past week is between 29 and 32.5 degrees celsius
                    lastweektemps=[]
                    for j in range(7):
                        k=i-j
                        lastweektemps.append(self.tempdata[k])
                        weekavg=statistics.mean(lastweektemps)
                        if weekavg >=29 and weekavg<=32.5:
                            self.Sw[i]=self.Sw[i-1]+(self.maturationr*self.tranmaternal*(self.Aw[i-1]/2)-(self.bw[i-1]*self.thm[i-1]*self.Ih[i-1]+1.1*self.muN[i-1])*self.Sw[i-1])+self.wolpercentage
                        else:
                            self.Sw[i]=self.Sw[i-1]+(self.maturationr*self.tranmaternal*(self.Aw[i-1]/2)-(self.bw[i-1]*self.thm[i-1]*self.Ih[i-1]+1.1*self.muN[i-1])*self.Sw[i-1])
                else:
                    self.Sw[i]=self.Sw[i-1]+(self.maturationr*self.tranmaternal*(self.Aw[i-1]/2)-(self.bw[i-1]*self.thm[i-1]*self.Ih[i-1]+1.1*self.muN[i-1])*self.Sw[i-1])
                self.Ew[i]=self.Ew[i-1]+((self.bw[i-1]*self.thm[i-1]*self.Ih[i-1]*self.Sw[i-1])-(self.maturationr+1.1*self.muN[i-1]))*self.Ew[i-1]
                self.Iw[i]=self.Iw[i-1]+(self.maturationr*self.Ew[i-1]-1.1*self.muN[i-1]*self.Iw[i-1])
                
