import numpy as np

zr4_wt_fracs = {" 8016":0.000296, 
                  24050:0.000076*0.0434,
                  24052:0.000076*0.838,
                  24053:0.000076*0.0950,
                  24054:0.000076*0.0237, 
                  26054:0.000141*0.0585,
                  26056:0.000141*0.918,
                  26057:0.000141*0.0212, 
                  40090:0.021877, 
                  40091:0.004771, 
                  40092:0.007292, 
                  40094:0.007390, 
                  40096:0.001191, 
                  50116:0.000464*.145,
                  50117:0.000464*.0768,
                  50118:0.000464*.242,
                  50119:0.000464*.0859,
                  50120:0.000464*.326,
                  50122:0.000464*.0463,
                  50124:0.000464*.0579,
                  }


li6_amu = 6.015
li7_amu = 7.016
avo = 6.022e23
uo2_kg = 4000
u_kg = uo2_kg*(0.035*235+0.965*238)/(32+(0.035*235+0.965*238))
print(u_kg)

li6_e = 0.9
correction = 1 # 0.605887557 # 0.605887557
li6_mg_per_u_kg = [200,180,160,140,120] # ,34,36,39.425,40]

clad_density_gcc = 6.56
num_FAs = 21
num_pins = (17*17-25)*num_FAs

breed_clad_cc = np.pi*(0.4750**2-0.4177**2)*144.16
print(f"clad = {breed_clad_cc} cc")
breed_clad_g  = breed_clad_cc*clad_density_gcc

# print(breed_clad_cc_tot, breed_clad_g_tot)

for li6_mg_per_u_kg in li6_mg_per_u_kg:
    li6_mg_per_u_kg_corr = li6_mg_per_u_kg*correction
    li6_g_core = li6_mg_per_u_kg_corr*u_kg/1000
    li6_g = li6_g_core/num_pins

    li6_at = li6_g*(avo/li6_amu)

    li6_at_dens = li6_at/breed_clad_cc*1e-24
    li7_at_dens = li6_at_dens*(1-li6_e)*li6_amu/li6_e/li7_amu

    new_clad_density_gcc = (li6_g+breed_clad_g)/breed_clad_cc

    tot_at_dens = li6_at_dens + li7_at_dens
    for i in zr4_wt_fracs.keys():
        tot_at_dens += zr4_wt_fracs[i]

    print(f"c lithium-doped zircaloy-4 cladding | rho = {new_clad_density_gcc:.4f}")
    print(f"c suppposed to be {li6_mg_per_u_kg} mg(Li-6)/kg(U) = tot {li6_g_core*1000/correction:.0f} mg / {u_kg:.0f} kg")
    print(f"c but script applies correction: {correction:.6f}")
    print(f"c   = {li6_mg_per_u_kg_corr:.4f} mg(Li-6)/kg(U) = tot {li6_g_core*1000:.0f} mg / {u_kg:.0f} kg")
    print(f"c   to manually account for Li-6 depletion over 0 to 10 MWd/kgU")
    print(f"c   tot at dens = {tot_at_dens:.10f}")
    print(f"m3101  3006.81c  {li6_at_dens:.10f} ")
    print(f"       3007.81c  {li7_at_dens:.10f} ")
    for i in zr4_wt_fracs.keys():
        i_wt_frac = zr4_wt_fracs[i] # (1-li6_at_dens)*
        # print(f"      {i}.81c  {i_wt_frac:.8f} ")

