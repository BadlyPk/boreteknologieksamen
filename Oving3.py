#%%

import numpy as np
import matplotlib.pyplot as plt
import math

import Oving2

#%%

g = 9.81


w_max_drilling = 3 * max(Oving2.totalBuoStringWeight)
w_max_tripping = 2 * max(Oving2.Buoyed)
w_max = max([w_max_drilling, w_max_tripping])

#EIPS min. tensile strength, search in Compendium (used 1 3/8'' here):
f_line_max = 83.2*10 #from kdaN to kN

w_line_max = f_line_max/g #tons

#Required string-up:
n_theo = math.ceil(w_max/w_line_max)

#Efficiency factor:
epsilon = round(0.99**(n_theo+1),3)

w_max_real = n_theo*w_line_max*epsilon

if __name__ == "__main__":
    print('Required string-ups:', n_theo)
    print('Efficiency factor:', epsilon)
    #Check if string up is sufficient, with efficiency factor:
    if w_max_real > w_max:
        print('A string-up of', n_theo, 'is sufficient')
    else: 
        print('A string-up of', n_theo, 'is not sufficient')
    print('-------------------')
    
SF_drilling = []    
SF_tripping = []
F_drawworks_drilling = []
F_drawworks_tripping = []

for i in range(len(Oving2.sectionNumber)):
    SF_drilling.append(
        round(w_max_real/Oving2.totalBuoStringWeight[i],2)
        )
    SF_tripping.append(
        round(w_max_real/Oving2.Buoyed[i],2)
        )
    F_drawworks_drilling.append(
        round(f_line_max/SF_drilling[i],2)
        )
    F_drawworks_tripping.append(
        round(f_line_max/SF_tripping[i],2)
        )
    
    
if __name__ == "__main__":    
    print('Safety factor drilling:', SF_drilling)
    print('Safety factor drilling:', SF_tripping)
    print('Force on DW  (drill string):', F_drawworks_drilling, 'kN')
    print('Force on DW  (casing/liner + DP):', F_drawworks_tripping, 'kN')

P_gen = 2000 * 0.7457 #hp to kW
epsilon_loss = 0.10

P_DW = P_gen - epsilon_loss*P_gen

v_b_drilling = []
v_b_tripping = []

for i in range(len(Oving2.sectionNumber)):

    v_f_drilling = P_DW/F_drawworks_drilling[i]
    v_b_drilling.append(round(v_f_drilling/n_theo,2))
    
    v_f_tripping = P_DW/F_drawworks_tripping[i]
    v_b_tripping.append(round(v_f_tripping/n_theo,2))

if __name__ == "__main__":    
    print('Pulling speed (drill string):', v_b_drilling, 'm/s')
    print('Pulling speed (casing/liner + DP):', v_b_tripping, 'm/s')





















