import numpy as np

ss_wt_fracs = {" 6000":0.0008, 
                 14028:0.01*0.922,
                 14029:0.01*0.047, 
                 14030:0.01*0.031,                 
                 15031:0.00045, 
                 16032:0.0003*0.948, 
                 16033:0.0003*0.0076,
                 16034:0.0003*0.0437,
                 16036:0.0003*0.002,
                 24050:0.19*0.0434,
                 24052:0.19*0.838,
                 24053:0.19*0.095,
                 24054:0.19*0.0237,
                 25055:0.02,
                 26054:0.683450*0.0585,
                 26056:0.683450*0.918,
                 26057:0.683450*0.0212, 
                 26058:0.683450*0.0028, 
                 28058:0.095*0.681,
                 28060:0.095*0.262,
                 28061:0.095*0.0114,
                 28062:0.095*0.0363,
                 28064:0.095*0.00926, 
                 }
uo2_kg = 4000
u_kg = uo2_kg * 238/(32+238)
# print(u_kg)

li6_mg_per_u_kg = [14] #,16,18,20,22,24,26,28,30] #,0.1,1,5,10,15,20]#20,25]
clad_density_gcc = 7.92
num_pins = 17*17-25
num_FAs = 21

breed_clad_cc = (np.pi*0.4577**2 - np.pi*0.4177**2)*144.16
breed_clad_g  = breed_clad_cc*clad_density_gcc

# print(breed_clad_cc_tot, breed_clad_g_tot)

for li6_mg_per_u_kg in li6_mg_per_u_kg:
    li6_g_core = li6_mg_per_u_kg*u_kg/1000
    li6_g = li6_g_core/num_FAs/num_pins
    print(f"check {li6_g*1000} matches {u_kg/(num_FAs*num_pins)*li6_mg_per_u_kg}")

    li6_wt_frac = li6_g/(li6_g+breed_clad_g)
    # print(li6_wt_frac)

    new_clad_density_gcc = (li6_g+breed_clad_g)/breed_clad_cc

    print(f"check density: {new_clad_density_gcc:.6f}")

    print(f"c lithium-doped stainless cladding | rho = {new_clad_density_gcc:.3f} ")
    print(f"c {li6_mg_per_u_kg} mg(Li-6)/kg(U) = tot {li6_g_core*1000:.0f} mg Li-6 / {u_kg:.0f} kg U")
    print(f"m3201  3006.81c  -{li6_wt_frac:.8f} ")
    for i in ss_wt_fracs.keys():
        # i_mass_tot = ss_wt_fracs[i]*clad_density_gcc*breed_clad_cc_tot
        i_wt_frac = (1-li6_wt_frac)*ss_wt_fracs[i]
        print(f"      {i}.81c  -{i_wt_frac:.8f} ")
    print(f"mt3201 fe56.24t $ (.23t 400 K, .25t 800 K)  ")