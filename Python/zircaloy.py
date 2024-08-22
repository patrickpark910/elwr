import numpy as np

zr4_wt_fracs = {" 8016":0.001193, 24052:0.000997, 26056:0.001993, 40090:0.497860, 40091:0.109780, 40092:0.169646, 40094:0.175665, 40096:0.028904, 50120:0.013955}
uo2_kg = 4000
u_kg = uo2_kg * 238/(32+238)
# print(u_kg)

li6_mg_per_u_kg = [0.1,1,5,10,15,20,25,30,35]#20,25]
clad_density_gcc = 6.56
num_pins = 17*17-25
num_FAs = 21

# breed_clad_cc_tot = num_FAs*num_pins*(np.pi*0.4750**2 - np.pi*0.4177**2)*72.08
# breed_clad_g_tot = breed_clad_cc_tot * clad_density_gcc

breed_clad_cc = (np.pi*0.4750**2 - np.pi*0.4177**2)*72.08
breed_clad_g  = breed_clad_cc*clad_density_gcc

# print(breed_clad_cc_tot, breed_clad_g_tot)

for li6_mg_per_u_kg in li6_mg_per_u_kg:
    li6_g_core = li6_mg_per_u_kg*u_kg/1000
    li6_g = li6_g_core/num_FAs/num_pins
    print(f"check {li6_g*1000} matches {u_kg/(num_FAs*num_pins)*li6_mg_per_u_kg}")

    li6_wt_frac = li6_g/(li6_g+breed_clad_g)
    # print(li6_wt_frac)

    new_clad_density_gcc = (li6_g+breed_clad_g)/breed_clad_cc

    print(f"c lithium-doped zircaloy cladding | rho = {new_clad_density_gcc:.3f} ")
    print(f"c {li6_mg_per_u_kg} mg(Li-6)/kg(U) = tot {li6_g_core*1000:.0f} mg Li-6 / {u_kg:.0f} kg U")
    print(f"m125  3006.81c  -{li6_wt_frac:.8f} ")
    for i in zr4_wt_fracs.keys():
        # i_mass_tot = zr4_wt_fracs[i]*clad_density_gcc*breed_clad_cc_tot
        i_wt_frac = (1-li6_wt_frac)*zr4_wt_fracs[i]
        print(f"     {i}.81c  -{i_wt_frac:.8f} ")

