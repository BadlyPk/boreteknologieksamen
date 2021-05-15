#%%

import numpy as np
import matplotlib.pyplot as plt
import math

import Oving2
import Oving3

#%%

#For section 1 and 2, start at around 1.2 Sg, right above pore pressure
#For section 3, gradually increase from 1.2 Sg to around 1.55 Sg
#For section 4, greadually increase from 1.55 Sg to around 1.8 Sg
#For section 5 keep it about 1.8-1.9 Sg

g = 9.81
d = 8+1/2
d_hole = d*0.0254
critSpeed = 120/60
Q = 2500/1000/60
L = 5000

l_dp5 = 27.43 #m
w_dp5_per_meter = 38.1 #kg per m

rho_mud = 1.8*1000 
rho_s = 7840 #kg/m^3

WOB = 10 #tons

l_joint = 9.144
w_jointPPF = 60 #pounds per feet
w_joint_per_meter = w_jointPPF*1.48816

d_DP_outer = 5*0.0254
d_DP_inner = 4*0.0254



d_DCM = round(math.sqrt((d_hole**2)-((4*Q)/(critSpeed*math.pi))),4)
d_DCInches = round(d_DCM/0.02542,2)

print(d_DCInches)

possibleOD = [11+1/4,11,10,9+3/4,9+1/2,9,8+1/4,8,7+3/4,7+1/4,7,6+3/4,6+1/2,6+1/4,6,5+3/4,5+1/4,5,4+7/8,4+3/4,4+1/4,4+1/8,3+3/4,3+1/2,3+3/8,3+1/8+2+7/8]
usedOD = []

for available_length in possibleOD:
    if d_DCInches >= available_length:
      usedOD.append(available_length)
      break
print('Chosen OD:', usedOD, 'inches')

buoyancyfactor = 1-rho_mud/rho_s
print(buoyancyfactor)

DC_weight = (WOB*1000)/(0.85*buoyancyfactor)

eachDC_weight = l_joint*w_joint_per_meter

amountDC = math.ceil(DC_weight/eachDC_weight)

print('Amount of Drill Collars:', amountDC)

lengthDC = amountDC*l_joint
print('Drill collar length:', lengthDC, 'm')

weightDC = amountDC + DC_weight

amountDP5 = math.ceil((L-lengthDC)/l_dp5)
weightperDP5 = w_dp5_per_meter*l_dp5
weightDP5 = amountDP5*weightperDP5

dryWeight = (weightDP5 + weightDC)/1000

BuoWeightDP5 = round(dryWeight * buoyancyfactor,2)

print('Buoyed weight:', BuoWeightDP5, 'tons')

crossSectionAreaDP = (math.pi/4)*(d_DP_outer**2-d_DP_inner**2)

maxDrillingPa = (((BuoWeightDP5-WOB)*1000)*g)/crossSectionAreaDP

maxDrillingPSI = maxDrillingPa*0.000145037738

SF = 135000/maxDrillingPSI

print('Safety factor:', round(SF,2))

#SF_max = (pipe_grade * ((OD**2)-(ID**2))) / (pipe_weight)
#We check out the highest grades drillpipes, S-135, with 38.10kg/m and 29.02 kg/m

pipe_grade = 135
OD = 5
ID = [4, 4.216,]
pipe_weight = [38.10,29.02]

for i in range(len(ID)):
    SF_max = (pipe_grade*((OD**2)-(ID[i]**2))) / (pipe_weight[i])
    print('The pipe with weight', pipe_weight[i], 'has a SF of:', round(SF_max,2))



