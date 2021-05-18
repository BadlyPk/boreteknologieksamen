#%%

import numpy as np
import matplotlib.pyplot as plt
import math

from sympy.solvers import solve
from sympy import Symbol

#%%

#General values given in task or from tables:
g = 9.81
d = 8+1/2
d_hole = d*0.0254
critSpeed = 200/60
Q = 2000/1000/60
rho_mud = 1.6*1000 
rho_s = 7840 #kg/m^3
WOB = 10 #tons
l_joint = 9.144 #m
w_jointPPF = 117 #pounds per feet
w_joint_per_meter = w_jointPPF*1.48816
L = 5000


d_DCM = round(math.sqrt((d_hole**2)-((4*Q)/(critSpeed*math.pi))),4)
d_DCInches = round(d_DCM/0.02542,2)

possibleOD = [11+1/4,11,10,9+3/4,9+1/2,9,8+1/4,8,7+3/4,7+1/4,7,6+3/4,6+1/2,6+1/4,6,5+3/4,5+1/4,5,4+7/8,4+3/4,4+1/4,4+1/8,3+3/4,3+1/2,3+3/8,3+1/8+2+7/8]
usedOD = []

#Finds the closest matching standard OD:
for available_length in possibleOD:
    if d_DCInches >= available_length:
      usedOD.append(available_length)
      break
print('---Task 2a and 2b---')
print('Chosen OD:', usedOD, 'inches')

buoyancyfactor = 1-rho_mud/rho_s

DC_weight = (WOB*1000)/(0.85*buoyancyfactor)

eachDC_weight = l_joint*w_joint_per_meter

amountDC = math.ceil(DC_weight/eachDC_weight)

print('Amount of Drill Collars:', amountDC)

lengthDC = amountDC*l_joint
print('Drill collar length:', lengthDC, 'm')
weightDC = amountDC + DC_weight

print('---Task 2c---')
w_dp5_per_meter = 29.02 #kg per m
l_dp5 = 27.43 #m

l_HWDP = 27.43
w_HWDP = 81.74

amountHWDP = 9*3
weightperHWDP = w_HWDP*l_HWDP
weightHWDP = amountHWDP*weightperHWDP

amountDP5 = math.ceil((L-lengthDC-l_HWDP)/l_dp5)
weightperDP5 = w_dp5_per_meter*l_dp5
weightDP5 = amountDP5*weightperDP5

dryWeight = (weightDP5 + weightDC + weightHWDP)/1000

BuoWeightDP5 = round(dryWeight * buoyancyfactor,2)

print('Buoyed weight:', BuoWeightDP5, 'tons')

print('Buoyed weight without WOB, since we are drilling:', BuoWeightDP5-WOB, 'tons')