#%%

import numpy as np
import matplotlib.pyplot as plt
import math


#%%

sectionNumber = [1,2,3,4,5,6]
endDepth = [75,650,1350,2275,3700,4370] #m
holeSizeInch = [36,26,17+1/2,12+1/4,8+1/2,6] #inch
holeSizeM = [i*0.0254 for i in holeSizeInch] #cm
casingODInch = [30,20,13+3/8,9+5/8,7,4+1/2] #inch
casingODM = [i*0.0254 for i in casingODInch] #cm
casingIDInch = [28,18.7,12.35,8.53,6.09,3.92] #inch
casingIDM = [i*0.0254 for i in casingIDInch] #cm
mudWeightSpecific = [1.06,1.06,1.26,1.48,1.8,1.1] #Sg
mudWeightkgm3 = 1000*np.array(mudWeightSpecific)
porePressureSpecific = [1.035,1.035,1.160,1.459,1.745,1.045] #Sg
porePressurekgm3 = 1000*np.array(porePressureSpecific)
criticalSpeed = [125,125,125,125,125,125] #m/min
criticalSpeedms = np.array(criticalSpeed)/60; #ms
expectedFlowRate = [4000,4000,3500,3000,2200,1000] #l/min
flowRatem3s = np.array(expectedFlowRate)/1.666*10**-5
maximumWOB = [8,15,17,20,15,6] #tons
maximumWOBkg = 1000*np.array(maximumWOB)
g = 9.81

rho_s = 7840 #kg/m^3
l_joint = 9.1140 #m (30 feet)
dp5_weight = 29.02
dp3_weight = 23.07 
maxw_DC = [310,310,310,243,83,32] #lbs/ft
maxw_DCkg = 1.488*np.array(maxw_DC) #kg/m
maxw_CS = [309.7,133,72,53.5,32,13.5] #lbm/ft
maxw_CSkg = 1.488*np.array(maxw_CS) #kg/m

h_rathole = 5 #m
D_wh = 10 # m

DP_OD = 5 * 0.0254
DP_ID = 4.276 * 0.0254

if __name__ == "__main__":
    print('---Task 1---')
#Mud pressure:
p_mud = []

for i in range(len(sectionNumber)):
    p_mud.append(
        mudWeightkgm3[i]*g*endDepth[i]
        )


if __name__ == "__main__":
    print('Mud pressure:', np.round(np.array(p_mud)/100000,2), "MPa")

if __name__ == "__main__":
    print('---Task 2---')
#Overbalance:
overbalance = []        

for i in range(len(sectionNumber)):
    overbalance.append(
        p_mud[i]-(porePressurekgm3[i]*g*endDepth[i])
        )
if __name__ == "__main__":    
    print('Overbalance:', np.round(np.array(overbalance)/100000,2), "MPa")

if __name__ == "__main__":
    print('---Task 4---')
#Required OD and length of drill collars
OD = []

for i in range(len(sectionNumber)):
    OD.append(
        math.sqrt((holeSizeInch[i]**2)-((4*flowRatem3s[i])/(criticalSpeedms[i]*math.pi)))
        )
if __name__ == "__main__":    
    print('OD:', np.round(np.array(OD),2),'m')

clearedOD = [i - 2 for i in OD]
if __name__ == "__main__":
    print('Maximum DC OD:', np.round(np.array(clearedOD),3), 'inches')
possibleOD = [11+1/4,11,10,9+1/2,9,8+1/4,8,7+3/4,7+1/4,7,6+3/4,6+1/2,6+1/4,6,5+3/4,5+1/4,5,4+7/8,4+3/4,4+1/4,4+1/8,3+3/4,3+1/2,3+3/8,3+1/8+2+7/8]
usedOD = []

for wanted_length in clearedOD:
  for available_length in possibleOD:
    if wanted_length >= available_length:
      usedOD.append(available_length)
      break

if __name__ == "__main__":
    print('Chosen OD:', usedOD, 'inches')

#Buoyancy factor
buoyancyfactor = []
for i in range(len(sectionNumber)):
    buoyancyfactor.append(
        1-mudWeightkgm3[i]/rho_s
        )

#Drill collar weight
weightDC = []
for i in range(len(sectionNumber)):
    weightDC.append(
        maximumWOBkg[i]/(0.85*buoyancyfactor[i])
        )
if __name__ == "__main__":
    print('Drill collar weight:', weightDC, 'tons')
     
#Amount of collars
amountDC = []
for i in range(len(sectionNumber)):
    amountDC.append(
        round(math.ceil((weightDC[i]/maxw_DCkg[i])/l_joint))
        )
if __name__ == "__main__":
    print('Amount of drill collars:', amountDC)

lengthDC = []
for i in range(len(sectionNumber)):
    lengthDC.append(
        round((amountDC[i]*l_joint),2)
        )
if __name__ == "__main__":
    print('Length of the drill collars:', lengthDC, 'm')

#

if __name__ == "__main__":
    print('---Task 5---')
BuoWeightDC = []
for i in range(len(sectionNumber)):
    BuoWeightDC.append(
        round(buoyancyfactor[i]*lengthDC[i]*(maxw_DCkg[i]/1000),1)
        )
if __name__ == "__main__":
    print('Buoyed weight of drill collars:',BuoWeightDC, ' tons')

theoreticalLengthDP5 = []
theoreticalLengthDP3 = []

for i in range(len(endDepth)):
    if endDepth[i] > 3800:
        theoreticalLengthDP3.append(round(endDepth[i]-2275+105-lengthDC[i],2))
    else:
        theoreticalLengthDP3.append(0)
    theoreticalLengthDP5.append(round(endDepth[i]-lengthDC[i]-theoreticalLengthDP3[i],2))

if __name__ == "__main__":
    print('Theoretical length of DP5:', theoreticalLengthDP5, 'm')
    print('Theoretical length of DP3:', theoreticalLengthDP3, 'm')

amountDP5 = []
for i in range(len(sectionNumber)):
    amountDP5.append(
        math.ceil((theoreticalLengthDP5[i]/l_joint))
        )
if __name__ == "__main__":
    print('Amount of DP5:', amountDP5)

amountDP3 = []
for i in range(len(sectionNumber)):
    amountDP3.append(
        math.ceil((theoreticalLengthDP3[i]/l_joint))
        )
if __name__ == "__main__":
    print('Amount of DP5:', amountDP3)

lengthDP5 = []
for i in range(len(sectionNumber)):
    lengthDP5.append(
        round(amountDP5[i]*l_joint,2)
        )
if __name__ == "__main__":
    print('Length of DP5:', lengthDP5, 'm')

lengthDP3 = []
for i in range(len(sectionNumber)):
    lengthDP3.append(
        round(amountDP3[i]*l_joint,2)
        )
if __name__ == "__main__":
    print('Length of DP3:', lengthDP3, 'm')

BuoWeightDP5 = []
for i in range(len(sectionNumber)):
    BuoWeightDP5.append(
        round(buoyancyfactor[i]*lengthDP5[i]*(dp5_weight/1000),1)
        )
if __name__ == "__main__":
    print('Buoyed weight of DP5:', BuoWeightDP5, ' tons')

BuoWeightDP3 = []
for i in range(len(sectionNumber)):
    BuoWeightDP3.append(
        round(buoyancyfactor[i]*lengthDP3[i]*(dp3_weight/1000),1)
        )
if __name__ == "__main__":
    print('Buoyed weight of DP5:', BuoWeightDP3, ' tons')

totalBuoStringWeight = []
for i in range(len(sectionNumber)):
    totalBuoStringWeight.append(
        round(BuoWeightDC[i]+BuoWeightDP5[i]+BuoWeightDP3[i],1)
        )
if __name__ == "__main__":
    print('Total buoyed string weight:', totalBuoStringWeight)

if __name__ == "__main__":
    print('---Task 6---')

lengthCS = []*len(sectionNumber)
for i in range(0,4):
    lengthCS.append(
        round(endDepth[i] - h_rathole - D_wh,2)
        )
for i in range(4,6):
    lengthCS.append(
        round(endDepth[i]-endDepth[i-1]+100)
        )
if __name__ == "__main__":
    print('The length of the casing and liner:', lengthCS, 'm')

BuoWeightCS = []
for i in range(len(sectionNumber)):
    BuoWeightCS.append(
        round(buoyancyfactor[i]*lengthCS[i]*(maxw_CSkg[i]/1000),1)
        )
if __name__ == "__main__":
    print('Buoyed weight of the casing/liner:', BuoWeightCS, 'tons')

Buoyed = []
for i in range(len(sectionNumber)):
    if i == 4:
        Weight = 0
        B = 1 - mudWeightkgm3[i] / rho_s
        Lenght_liner = endDepth[i] - endDepth[i - 1] + 100
        Weight += Lenght_liner * B * maxw_CSkg[i]
        Length = math.ceil((endDepth[i - 1] - 100 - 5) / l_joint) * l_joint
        Weight += Length * dp5_weight * B
        Buoyed.append(round(Weight * 10 ** (-3), 2))
    elif i == 5:
        Weight = 0
        B = 1 - mudWeightkgm3[i] / rho_s
        Lenght_liner = endDepth[i] - endDepth[i - 1] + 100
        Weight += Lenght_liner * B * maxw_CSkg[i]
        Length = (
            math.ceil(((endDepth[i - 1] - 100) - (endDepth[i - 2] - 100) - 5) / l_joint) * l_joint
        )
        Weight += Length * 15.5 * 1.48816394 * B
        Length = math.ceil((endDepth[i - 2] - 100 - 5) / l_joint) * l_joint
        Weight += Length * dp5_weight * B
        Buoyed.append(round(Weight * 10 ** (-3), 2))
    else:
        Weight = 0
        B = 1 - mudWeightkgm3[i] / rho_s
        Length = endDepth[i] - h_rathole - D_wh
        Weight += maxw_CSkg[i] * Length * B
        Buoyed.append(round(Weight * 10 ** (-3), 2))

if __name__ == "__main__":
    print('Buoyed weight of casing/liner + DP:', Buoyed)

if __name__ == "__main__":
    print('---Task 7---')

tensionString = []
for i in range(len(sectionNumber)):
    Tension = totalBuoStringWeight[i] * g / (np.pi / 4 * (DP_OD ** 2 - DP_ID ** 2))
    tensionString.append(round(Tension * 10 ** (-3), 2))

if __name__ == "__main__":
    print('Drill string tension:', tensionString)

tensionCasing = []
for i in range(len(sectionNumber)):
    if i == 4:
        Tension = Buoyed[i] * g / (np.pi / 4 * (DP_OD ** 2 - DP_ID ** 2))
        tensionCasing.append(round(Tension * 10 ** (-3), 2))
    elif i == 5:
        Tension = Buoyed[i] * g / (np.pi / 4 * (DP_OD ** 2 - DP_ID ** 2))
        tensionCasing.append(round(Tension * 10 ** (-3), 2))
    else:
        Tension = Buoyed[i] * g/ (np.pi / 4 * (casingODM[i] ** 2 - casingIDM[i] ** 2))
        tensionCasing.append(round(Tension * 10 ** (-3), 2))

if __name__ == "__main__":
    print('Casing tension:', tensionCasing)