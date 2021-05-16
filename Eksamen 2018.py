#%%

import numpy as np
import matplotlib.pyplot as plt
import math

from sympy.solvers import solve
from sympy import Symbol

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

possibleOD = [11+1/4,11,10,9+3/4,9+1/2,9,8+1/4,8,7+3/4,7+1/4,7,6+3/4,6+1/2,6+1/4,6,5+3/4,5+1/4,5,4+7/8,4+3/4,4+1/4,4+1/8,3+3/4,3+1/2,3+3/8,3+1/8+2+7/8]
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

maxDrillingPa = (((BuoWeightDP5-WOB)*1000)*g)/crossSectionAreaDP

maxDrillingPSI = maxDrillingPa*0.000145037738

SF = 135000/maxDrillingPSI

print('Safety factor:', round(SF,2))

#SF_max = (pipe_grade * ((OD**2)-(ID**2))) / (pipe_weight)
#We check out the highest grades drillpipes, S-135, with 38.10kg/m and 29.02 kg/m

pipe_grade = 135
OD = 5
ID = [4, 4.276]
pipe_weight = [38.10,29.02]
SF_pipes = []

for i in range(len(ID)):
    SF_max = (pipe_grade*((OD**2)-(ID[i]**2))) / (pipe_weight[i])
    SF_pipes.append(SF_max)
    print('The pipe with weight', pipe_weight[i], 'kg, has a SF of:', round(SF_max,2))
    

actualSF = SF*max(SF_pipes)/min(SF_pipes)
print('The actual SF is:', round(actualSF,2))

rho_gas = 188
new_rho_mud = 1790
rho_frac = 1800
rho_pore = 1750
h_end = 4500 #Section depth end
h_start = 2000 #Section depth start
P_frac = rho_frac*g*h_start #1800 er frac pressure, ved section start (2000)
P_pore = rho_pore*g*h_end #1750 er pore pressure, ved section end (4500)
H = h_end-h_start
A = (math.pi/4)*(((12+1/4)*0.0254)**2-(d_DP_outer)**2)

V_influx = (P_frac*A)/(P_pore) * ((P_pore-P_frac-new_rho_mud*g*H)/(g*(rho_gas-new_rho_mud)))

print('Kick tolerance:', round(V_influx,4))

V_influx_limit = 4 #m^3

#V_influx_limit = (rho_frac*x*A/P_pore)*((P_pore-rho_frac*g*x-new_rho_mud*g*(h_end-x))/(rho_gas-new_rho_mud))
#Sett inn i wolfram alpha

a = (rho_frac-new_rho_mud)*g
b = (new_rho_mud-rho_pore)*g*4500
c = (V_influx_limit*P_pore*(rho_gas-new_rho_mud))/(A*rho_frac)

x1=(-b+math.sqrt(b**2-4*a*c))/(2*a)
x2=(-b-math.sqrt(b**2-4*a*c))/(2*a)

print('X1:', x1, 'X2:', x2)


#Choose the strongest and heaviest casing: P-110, 72 lbm/ft
thickness_13_casing = 0.514
od_13_casing = 13.375
id_13_casing = 12.347
nom_weight_threads_and_coupling = 107.15
A_13_casing = (math.pi/4)*(((od_13_casing)*0.0254)**2-(id_13_casing*0.0254)**2)

dry_mass_13_casing = nom_weight_threads_and_coupling*2000

#Choose Buoyancy factor of 0.8 (just assume)
sigma_a = ((0.8*dry_mass_13_casing*g)/A_13_casing)/10**5 #Pa
print('Sigma_a:', round(sigma_a,2), 'bar')
sigma_ys = 110000/14.5 #Psi to bar

sigma_t_vs_ys = 0.5*(sigma_a/sigma_ys)+math.sqrt(1-0.75*((sigma_a/sigma_ys)**2))

print('sigma_t =', round(sigma_t_vs_ys,3),'* sigma_ys')

#Since sigma_t is higher (1.072 times sigma ys), this means the tension is more burst resistance due to axial tension. Therefore, more conservative to not consider axial tension

P_burst = 2*sigma_ys*(thickness_13_casing/od_13_casing)
print('P_burst:', round(P_burst,2), 'bar')

used_SF = 1.1

frac_gradient = (P_burst*(10**5)/(used_SF*g*h_start)+rho_gas)/1000 #Sg

print('Fracture gradient:', frac_gradient, 'Sg')

