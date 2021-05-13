# %%
import math
import numpy as np

# %%

sections = 6
g = 9.81
Mw = [1060, 1060, 1260, 1480, 1800, 1100]
Depth = [75, 650, 1350, 2275, 3700, 4370]
Hole_size = [
    36 * 0.0254,
    26 * 0.0254,
    17.5 * 0.0254,
    12.25 * 0.0254,
    8.5 * 0.0254,
    6 * 0.0254,
]
OD = [
    30 * 0.0254,
    20 * 0.0254,
    13.375 * 0.0254,
    9.625 * 0.0254,
    7 * 0.0254,
    4.5 * 0.0254,
]
ID = [
    28 * 0.0254,
    18.7 * 0.0254,
    12.35 * 0.0254,
    8.53 * 0.0254,
    6.09 * 0.0254,
    3.92 * 0.0254,
]
PP = [1035, 1035, 1160, 1459, 1745, 1045]
DC_OD = [
    11.25 * 0.0254,
    11.25 * 0.0254,
    11.25 * 0.0254,
    10 * 0.0254,
    6 * 0.0254,
    3.75 * 0.0254,
]
DC_ID = [
    3.25 * 0.0254,
    3.25 * 0.0254,
    3.25 * 0.0254,
    3 * 0.0254,
    2.25 * 0.0254,
    1.5 * 0.0254,
]
DP_OD = 5 * 0.0254
DP_ID = 4.276 * 0.0254
WOB = [8 * 10 ** 3, 15 * 10 ** 3, 17 * 10 ** 3, 20 * 10 ** 3, 15 * 10 ** 3, 6 * 10 ** 3]
DC_weight = [
    310 * 1.48816394,
    310 * 1.48816394,
    310 * 1.48816394,
    243 * 1.48816394,
    83 * 1.48816394,
    32 * 1.48816394,
]
DP_weight = 19.5 * 1.48816394
Critical_speed = 125 / 60
Flow_rate = [
    4000 / (1000 * 60),
    4000 / (1000 * 60),
    3500 / (1000 * 60),
    3000 / (1000 * 60),
    2200 / (1000 * 60),
    1000 / (1000 * 60),
]
Rho_steel = 7840
Cs_weight = [
    309.7 * 1.48816394,
    133 * 1.48816394,
    72 * 1.48816394,
    53.5 * 1.48816394,
    32 * 1.48816394,
    13.5 * 1.48816394,
]

# %%


def P_mud():
    P_from_mud = []
    for i in range(sections):
        P_from_mud.append(round(Mw[i] * g * Depth[i] / (10 ** 5), 2))
    return P_from_mud


mud_pressure = P_mud()

# %%


def Overbalance():
    overbalance = []
    for i in range(sections):
        overbalance.append(round((Mw[i] - PP[i]) * g * Depth[i] * 10 ** (-5), 2))
    return overbalance


overbalance = Overbalance()
# %%


def OD_dc():
    dc_OD = []
    for i in range(sections):
        OD_max = np.sqrt(
            (np.pi / 4 * Critical_speed * Hole_size[i] ** 2 - Flow_rate[i])
            / (np.pi / 4 * Critical_speed)
        )
        dc_OD.append(round(OD_max / 0.0254, 2))
    return dc_OD


# OD_dc()
# 2 inches klaring fra hullstrørrelse og max OD gir:
# Seksjon 1, 2 og 3: 11 1/4 inches
# seksjon 4: 10 inches
# seksjon 5: 6 inches
# seksjon 6: 3 3/4 inches
# %%


def DC_length():
    length = []
    joint = 9.144
    for i in range(sections):
        B = 1 - (Mw[i]) / (Rho_steel)
        weight = WOB[i] / (0.85 * B)
        Length = weight / DC_weight[i]
        number = math.ceil(Length / joint)
        length.append(round(number * joint, 2))
    return length


DC_l = DC_length()

# %%


def buoyed_weight():
    Buoyed_weight = []
    joint = 9.144
    for i in range(sections):
        B = 1 - Mw[i] / Rho_steel
        if i == 5:
            Weight = 0
            Weight += DC_l[i] * DC_weight[i] * B
            Length_dp = math.ceil((Depth[i] - DC_l[i] - 2170) / joint) * joint
            Weight += B * 2170 * 15.5 * 1.48816394
            Weight += B * Length_dp * DP_weight
            Buoyed_weight.append(round(Weight * 10 ** (-3), 2))
        else:
            Weight = 0
            Weight += DC_l[i] * DC_weight[i] * B
            Length_dp = math.ceil((Depth[i] - DC_l[i]) / joint) * joint
            Weight += B * Length_dp * DP_weight
            Buoyed_weight.append(round(Weight * 10 ** (-3), 2))
    return Buoyed_weight


DS_w = buoyed_weight()
print(DS_w)
# %%

Rat_hole = 5
RKB_WH = 10


def casing_weight():
    Buoyed = []
    joint = 9.144
    for i in range(sections):
        if i == 4:
            Weight = 0
            B = 1 - Mw[i] / Rho_steel
            Lenght_liner = Depth[i] - Depth[i - 1] + 100
            Weight += Lenght_liner * B * Cs_weight[i]
            Length = math.ceil((Depth[i - 1] - 100 - 5) / joint) * joint
            Weight += Length * DP_weight * B
            Buoyed.append(round(Weight * 10 ** (-3), 2))
        elif i == 5:
            Weight = 0
            B = 1 - Mw[i] / Rho_steel
            Lenght_liner = Depth[i] - Depth[i - 1] + 100
            Weight += Lenght_liner * B * Cs_weight[i]
            Length = (
                math.ceil(((Depth[i - 1] - 100) - (Depth[i - 2] - 100) - 5) / joint)
                * joint
            )
            Weight += Length * 15.5 * 1.48816394 * B
            Length = math.ceil((Depth[i - 2] - 100 - 5) / joint) * joint
            Weight += Length * DP_weight * B
            Buoyed.append(round(Weight * 10 ** (-3), 2))
        else:
            Weight = 0
            B = 1 - Mw[i] / Rho_steel
            Length = Depth[i] - Rat_hole - RKB_WH
            Weight += Cs_weight[i] * Length * B
            Buoyed.append(round(Weight * 10 ** (-3), 2))
    return Buoyed


print(casing_weight())
Casing_w = casing_weight()
# %%


def Max_stress_string():
    tension = []
    for i in range(sections):
        Tension = DS_w[i] * g / (np.pi / 4 * (DP_OD ** 2 - DP_ID ** 2))
        tension.append(round(Tension * 10 ** (-3), 2))
    return tension


MAX = Max_stress_string()
# %%


def Max_stress_casing():
    tension = []
    for i in range(sections):
        if i == 4:
            Tension = Casing_w[i] * g / (np.pi / 4 * (DP_OD ** 2 - DP_ID ** 2))
            tension.append(round(Tension * 10 ** (-3), 2))
        elif i == 5:
            Tension = Casing_w[i] * g / (np.pi / 4 * (DP_OD ** 2 - DP_ID ** 2))
            tension.append(round(Tension * 10 ** (-3), 2))
        else:
            Tension = g * Casing_w[i] / (np.pi / 4 * (OD[i] ** 2 - ID[i] ** 2))
            tension.append(round(Tension * 10 ** (-3), 2))
    return tension


Max_stress_casing()

print(Max_stress_string())
print(Max_stress_casing())

# %%
