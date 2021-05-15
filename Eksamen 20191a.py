#%%

import numpy as np
import matplotlib.pyplot as plt
import math

import Oving2
import Oving3

#%%

viscP = 30
vis = 30/1000
g = 9.81

rho_mud = 1.8*1000
rho_s = 7840 #kg/m^3
Q = 2200/1000/60
critSpeed = 125/60
L = 3700

WOB = 15 #tons

d = 8.5 #inches

d_DP_inner = 4.276*0.0254
d_DP_outer = 5*0.0254
d_hole = d*0.0254

n_nozzles = 5
d_nozzle = (14/32)*0.0254

l_joint = 9.144
w_joint_per_meter = 111.6

w_dp5_per_meter = 29.02 #kg per m
l_dp5 = 27.43 #m

A_pipe = (math.pi*((d_DP_inner/2)**2))

v_pipe = Q/A_pipe

Re_pipe = (rho_mud*v_pipe*d_DP_inner)/vis

#print(Re_pipe)

A_hole = (math.pi*((d_hole)/2)**2)
A_pipe_outer = (math.pi*((d_DP_outer/2)**2))
A_ann = A_hole-A_pipe_outer

v_ann = Q/A_ann

Re_ann = (rho_mud*v_ann*(d_hole-d_DP_outer))/vis

#print(Re_ann)

A_nozzle = (math.pi*((d_nozzle)/2)**2)
v_bit = Q/(A_nozzle*n_nozzles)

if Re_pipe > 4000 and Re_ann > 4000:
    deltaP_pipe = (0.092*(rho_mud**0.8)*(vis**0.2)*(v_pipe**1.8)*L)/(d_DP_inner**1.2)
    deltaP_ann = (0.092*(rho_mud**0.8)*(vis**0.2)*(v_ann**1.8)*L)/((d_hole-d_DP_outer)**1.2)
    #print(deltaP_pipe/100000)
    #print(deltaP_ann/100000)

    deltaP_bit = 0.55*rho_mud*(v_bit**2)
    #print(deltaP_bit/100000)

p_SPP = round(deltaP_ann+deltaP_bit+deltaP_pipe,1)
print('SPP:', p_SPP/100000, 'bar')

ECD = round(rho_mud + deltaP_ann/(g*L),2)
print('ECD:', ECD/1000, 'Sg')

#Pressure window minimum is the mud weight minus swab effects. Maximum is ECD plus surge pressure

d_DCM = round(math.sqrt((d_hole**2)-((4*Q)/(critSpeed*math.pi))),4)
d_DCInches = round(d_DCM/0.02542,2)

print(d_DCInches)

possibleOD = [11+1/4,11,10,9+1/2,9,8+1/4,8,7+3/4,7+1/4,7,6+3/4,6+1/2,6+1/4,6,5+3/4,5,4+7/8,4+3/4,4+1/4,4+1/8,3+3/4,3+1/2,3+3/8,3+1/8+2+7/8]
usedOD = []

for available_length in possibleOD:
    if d_DCInches >= available_length:
      usedOD.append(available_length)
      break
print('Chosen OD:', usedOD, 'inches')

buoyancyfactor = 1-rho_mud/rho_s

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

maxTrippingPa = ((BuoWeightDP5*1000)*g)/crossSectionAreaDP
maxDrillingPa = (((BuoWeightDP5-WOB)*1000)*g)/crossSectionAreaDP
print(maxTrippingPa, maxDrillingPa)

maxTrippingPSI = maxTrippingPa*0.000145037738
maxDrillingPSI = maxDrillingPa*0.000145037738

maxTrippingPSI = maxTrippingPSI * 2
maxDrillingPSI = maxDrillingPSI * 3

print('The grade has to be at least:', math.ceil(maxDrillingPSI/1000))

rho_g = 0.188 #Sg

#Look in table for right OD size, for section 4. Look for closest grade to DP, which in this case is C-95. Then look for correct ID. 
casing_size = 9.625
casing_collapse = 7340
casing_wall_thickness = 0.545

P_burst = 2*casing_collapse*(casing_wall_thickness*0.0254)/(casing_size*0.0254)

print(P_burst)


