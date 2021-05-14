#%%

import numpy as np
import matplotlib.pyplot as plt
import math

import Oving2
import Oving3

#%%

viscP = 30
vis = 30/1000

rho_mud = 1.8*1000
Q = 2200/1000/60
L = 3700

d_DP_inner = 4.276*0.0254
d_DP_outer = 5*0.0254
d_hole = 8.5*0.0254

n_nozzles = 5
d_nozzle = (14/32)*0.0254

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

p_SPP = deltaP_ann+deltaP_bit+deltaP_pipe
print('SPP:', p_SPP/100000, 'bar')

ECD = rho_mud + deltaP_ann/(9.81*L)
print('ECD:', ECD/1000, 'Sg')

#Pressure window minimum is the mud weight minus swab effects. Maximum is ECD plus surge pressure

