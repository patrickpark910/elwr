import numpy as np

lithium = {40090:0.5145, 40091:0.1122, 40092:0.1715, 40094:0.1738, 40096:0.0280}
uo2_kg = 4000
li6_mg_per_uo2_kg = [5,10,20,30,40,50]
clad_density_gcc = 6.5
num_FAs = 17*17-25

breed_clad_cc = (np.pi*0.4750**2 - np.pi*0.4177**2)*72.08
breed_clad_cc_tot = breed_clad_cc*num_FAs
breed_clad_g_tot = breed_clad_cc_tot * clad_density_gcc

for m in li6_mg_per_uo2_kg:
    li6_mg_tot = m*uo2_kg
    li6_g_tot = li6_mg_tot/1000

    new_clad_density_gcc = (li6_g_tot+breed_clad_g_tot)/breed_clad_cc_tot

    # print(li6_g_tot,breed_clad_g_tot,li6_g_tot/breed_clad_g_tot,)
    li6_wt_frac = li6_g_tot/(li6_g_tot+breed_clad_g_tot)

    print(f"c lithium-doped ziracloy cladding | rho = {new_clad_density_gcc:.3f} ")
    print(f"c {m} mg(Li-6)/kg(UO2) = tot {li6_g_tot} g Li-6 in core ")
    print(f"m125  3006.81c {li6_wt_frac:.6f} ")
    for i in lithium.keys():
        i_mass_tot = lithium[i]*clad_density_gcc*breed_clad_cc_tot
        i_wt_frac = i_mass_tot / (li6_g_tot+breed_clad_g_tot)
        print(f"     {i}.81c {i_wt_frac:.6f} ")

        # print(new_clad_density_gcc)