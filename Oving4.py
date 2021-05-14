#%%

import numpy as np
import matplotlib.pyplot as plt
import math

import Oving2
import Oving3

#%%

viscP = [1,1,30,30,30,30]
vis = [i/1000 for i in viscP]

n_nozzles = 5
d_nozzle = (14/32)*0.0254


Re_pipe = []

for i in range(len(Oving2.sectionNumber)):
    rho_mud = Oving2.mudWeightkgm3[i]
    Q = Oving2.expectedFlowRate[i]/1000/60
    d_DP_inner = 4.276*0.0254
    A_pipe = (math.pi*((d_DP_inner/2)**2))
    v_pipe = Q/A_pipe
    Re_pipe.append(round(
        (rho_mud*v_pipe*d_DP_inner)/vis[i]
        ,2))
print('RePipe:', Re_pipe)


Re_ann = []

for i in range(len(Oving2.sectionNumber)):
    rho_mud = Oving2.mudWeightkgm3[i]
    Q = Oving2.expectedFlowRate[i]/1000/60
    d_hole = Oving2.holeSizeInch[i]*0.0254
    d_ann_DP_outer = 5*0.0254
    A_hole = (math.pi*((d_hole)/2)**2)
    A_pipe_outer = (math.pi*((d_ann_DP_outer/2)**2))
    A_ann = A_hole-A_pipe_outer
    v_ann = Q/A_ann
    Re_ann.append(round(
        (rho_mud*v_ann*(d_hole-d_ann_DP_outer))/vis[i]
        ,2))
print('ReAnn:', Re_ann)    

deltaP_pipe = []
deltaP_ann = []
deltaP_bit = []
p_SPP = []

for i in range(len(Oving2.sectionNumber)):
    rho_mud = Oving2.mudWeightkgm3[i]
    Q = Oving2.expectedFlowRate[i]/1000/60
    A_nozzle = (math.pi*((d_nozzle)/2)**2)
    v_bit = Q/(A_nozzle*n_nozzles)
    d_hole = Oving2.holeSizeInch[i]*0.0254
    
    d_DP_inner = 4.276*0.0254
    A_pipe = (math.pi*((d_DP_inner/2)**2))
    v_pipe = Q/A_pipe
    
    d_ann_DP_outer = 5*0.0254
    A_hole = (math.pi*((d_hole)/2)**2)
    A_pipe_outer = (math.pi*((d_ann_DP_outer/2)**2))
    A_ann = A_hole-A_pipe_outer
    v_ann = Q/A_ann
    
    if Re_pipe[i] > 2300 and Re_ann[i] > 2300:
        deltaP_pipe.append(
            ((0.092*(rho_mud**0.8)*(vis[i]**0.2)*(v_pipe**1.8)*Oving2.endDepth[i])/(d_DP_inner**1.2))/100000
            )
        deltaP_ann.append(
            ((0.092*(rho_mud**0.8)*(vis[i]**0.2)*(v_ann**1.8)*Oving2.endDepth[i])/((d_hole-d_ann_DP_outer)**1.2))/100000
            )
        deltaP_bit.append(
            (0.55*rho_mud*(v_bit**2))/100000
            )
        
    p_SPP.append(round(
        deltaP_pipe[i] + deltaP_ann[i] + deltaP_bit[i]
        ,2))
    
print('SPP:', p_SPP)

ECD = []

for i in range(len(Oving2.sectionNumber)):
    ECD.append(round(
        Oving2.mudWeightkgm3[i] + (deltaP_ann[i]/(9.81*Oving2.endDepth[i]))
        ,2))

print('ECD:', ECD)





