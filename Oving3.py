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

if __name__ == "__main__":
    print('Required string-ups:', n_theo)
    print('Efficiency factor:', epsilon)
    #Check if string up is sufficient, with efficiency factor:
    if n_theo*w_line_max*epsilon > w_max:
        print('A string-up of', n_theo, 'is sufficient')
    else: 
        print('A string-up of', n_theo, 'is not sufficient')


