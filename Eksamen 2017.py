#%%

import numpy as np
import matplotlib.pyplot as plt
import math

from sympy.solvers import solve
from sympy import Symbol

import Oving2
import Oving3

#%%

#For section 1 and 2, use sea water, right above pore pressure
#For section 3, gradually increase to around 1.55 Sg
#For section 4, greadually increase from 1.55 Sg to around 1.7 Sg
#For section 5, reservoar depleted, so decrease mud weight to 1.1 Sg


g = 9.81
d = 8+1/2
d_hole = d*0.0254
critSpeed = 100/60
Q = 2000/1000/60
L = 4844

rho_mud = 1.1*1000 
rho_s = 7840 #kg/m^3

l_dp5 = 27.43 #m, assumed
w_dp5_per_meter = 29.02 #kg per m, from table

sigma_ys = 135000 #psi, from table (grade name) 

WOB = 9 #tons, from task

l_joint = 9.144 #m, assumed
w_jointPPF = 60 #pounds per feet
w_joint_per_meter = w_jointPPF*1.48816

d_DP_outer = 5*0.0254 #from task
d_DP_inner = 4.276*0.0254 #from table



d_DCM = round(math.sqrt((d_hole**2)-((4*Q)/(critSpeed*math.pi))),4)
d_DCInches = round(d_DCM/0.02542,2)

possibleOD = [11+1/4,11,10,9+3/4,9+1/2,9,8+1/4,8,7+3/4,7+1/4,7,6+3/4,6+1/2,6+1/4,6,5+3/4,5+1/4,5,4+7/8,4+3/4,4+1/4,4+1/8,3+3/4,3+1/2,3+3/8,3+1/8+2+7/8]
usedOD = []

for available_length in possibleOD:
    if d_DCInches >= available_length:
      usedOD.append(available_length)
      break
print('Chosen OD:', usedOD, 'inches')

buoyancyfactor = 1-rho_mud/rho_s

DC_weight = (WOB*1000)/(0.85*buoyancyfactor)

print(DC_weight)

eachDC_weight = l_joint*w_joint_per_meter

amountDC = math.ceil(DC_weight/eachDC_weight)

print('Amount of Drill Collars:', amountDC)

lengthDC = amountDC*l_joint
print('Drill collar length:', lengthDC, 'm')

#Need to find the most load while tripping and during drilling. For each of these, we multiply with the safety factors 2 and 3, respectively. When calculating the drilling phase, we can ignore the WOB. We can then find the tensions with the cross section area and buoyed weight.
#Generally, and intuitively, its the load when drilling (multiplied with SF=3), that decides the grade of drill pipe.

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

SF = sigma_ys/maxDrillingPSI

print('Tension on drill pipe:', round(maxDrillingPSI,3), 'psi')
print('Safety factor:', round(SF,2))

#Task torque:


tau_max = (math.sqrt(((sigma_ys**2)-(maxDrillingPSI))/3))/14.5*100000 #psi to bar to pascal

torque_max = (tau_max*((d_DP_outer**2)-(d_DP_inner**2))*(d_DP_outer+d_DP_inner)*math.pi)/16

print('Max torque:', round(torque_max,3), 'Nm')

#Task twist

G = 79.3*(10**9) #GPa to Pa

#We use the relation: twist_DP_max = (j_torsion*G*twist_ang)/L

j_torsion = (math.pi*((d_DP_outer**4)-(d_DP_inner**4)))/(32)
twist_ang = (L*torque_max)/(j_torsion*G)

print('The pipe is turned:', math.ceil(twist_ang/(math.pi*2)), 'turns')




