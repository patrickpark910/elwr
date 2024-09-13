import numpy as np

n_ss304_dict = {" 6000":0.000322,      # -----------------CHANGE
                 14028:0.001722*0.922,
                 14029:0.001722*0.047, 
                 14030:0.001722*0.031,                 
                 15031:0.000070, 
                 16032:0.000045*0.948, 
                 16033:0.000045*0.0076,
                 16034:0.000045*0.0437,
                 16036:0.000045*0.002,
                 24050:0.017671*0.0434,
                 24052:0.017671*0.838,
                 24053:0.017671*0.095,
                 24054:0.017671*0.0237,
                 25055:0.001760,
                 26054:0.059182*0.0585,
                 26056:0.059182*0.918,
                 26057:0.059182*0.0212, 
                 26058:0.059182*0.0028, 
                 28058:0.007827*0.681,
                 28060:0.007827*0.262,
                 28061:0.007827*0.0114,
                 28062:0.007827*0.0363,
                 28064:0.007827*0.00926, 
                 }

# Molar masses
mm_T   = 3.016 # g/mol
mm_Li6 = 6.015 # g/mol
mm_Li7 = 7.016 # g/mol
mm_U235 = 235.044 # g/mol
mm_U238 = 238.051 # g/mol

# Physical constants
mu = 1.660539 # b-mol/cm**2-at
avo = 6.022e23 # at/mol

# Reactor settings
e_U = 0.035
e_Li = 0.9
correction = 1 # 0.7450072562255365 # 1 # -----------------CHANGE

m_UO2 = 4000 # kg
m_U = m_UO2*(e_U*mm_U235+(1-e_U)*mm_U238)/(32+(e_U*mm_U235+(1-e_U)*mm_U238)) # kg
# print(f"kg U in core: {m_U}")

num_FAs = 21
num_pins = (17*17-25)*num_FAs

R_clad_in, R_clad_out, H_clad = 0.4177, 0.4577, 144.16 # -----------------CHANGE
V_clad_pin = np.pi*(R_clad_out**2-R_clad_in**2)*H_clad # should be 23.1662 cc
V_clad_core = V_clad_pin*num_pins # cc of cladding in whole core
rho_clad = 8.03 # g/cc -----------------CHANGE

c_i = [67,54.36,43.35] # mgLi6/kgU
for c_i in c_i:
    c_i_corr   = c_i*correction
    m_Li6_core = c_i_corr*m_U/1000 # g = mg/kgU*kgU/1000
    m_Li6_pin  = m_Li6_core/num_pins # g
    m_Li7_pin  = ((1-e_Li)/e_Li)*m_Li6_pin

    n_Li6_pin = m_Li6_pin/mu/mm_Li6/V_clad_pin # b-mol/cm**2-at = g*(b-mol/cm**2-at)
    n_Li7_pin = m_Li7_pin/mu/mm_Li7/V_clad_pin
    n_Li_pin  = n_Li6_pin + n_Li7_pin

    m_clad_new = m_Li6_pin + m_Li7_pin + (V_clad_pin*rho_clad)
    rho_clad_new = m_clad_new/V_clad_pin

    n_tot_pin = n_Li6_pin + n_Li7_pin
    for i in n_ss304_dict.keys():
        n_tot_pin += n_ss304_dict[i]
    
    print(f"c lithium-doped stainless steel 304 cladding | rho = {rho_clad_new:.4f}")
    # print(f"c suppposed to be {c_i} mg(Li-6)/kg(U) = tot {m_Li6_core*1000/correction:.0f} mg / {m_U:.0f} kg")
    # print(f"c but script applies correction: {correction:.6f}")
    print(f"c = {c_i_corr:.4f} mg(Li-6)/kg(U) = tot {m_Li6_core*1000:.0f} mg / {m_U:.0f} kg")
    print(f"c tot at dens = {n_tot_pin:.10f} [at/b-cm]")
    print(f"m3201  3006.81c  {n_Li6_pin:.12f} ")
    print(f"       3007.81c  {n_Li7_pin:.12f} ")
    for i in n_ss304_dict.keys():
        i_wt_frac = n_ss304_dict[i] # (1-li6_at_dens)*
        print(f"      {i}.81c  {i_wt_frac:.8f} ")

