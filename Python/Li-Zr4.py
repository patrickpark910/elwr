import numpy as np

n_zr4_dict = {" 8016":0.000296, 
                24050:0.000076*0.0434,
                24052:0.000076*0.838,
                24053:0.000076*0.0950,
                24054:0.000076*0.0237, 
                26054:0.000141*0.0585,
                26056:0.000141*0.918,
                26057:0.000141*0.0212,
                26058:0.000141*0.0028, 
                40090:0.021877, 
                40091:0.004771, 
                40092:0.007292, 
                40094:0.007390, 
                40096:0.001191, 
                50112:0.000464*.00970,
                50114:0.000464*.0066,
                50115:0.000464*.0034,
                50116:0.000464*.145,
                50117:0.000464*.0768,
                50118:0.000464*.242,
                50119:0.000464*.0859,
                50120:0.000464*.326,
                50122:0.000464*.0463,
                50124:0.000464*.0579,
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
correction = 1 # 0.7450072562255365 # 1

m_UO2 = 4000 # kg
m_U = m_UO2*(e_U*mm_U235+(1-e_U)*mm_U238)/(32+(e_U*mm_U235+(1-e_U)*mm_U238)) # kg
# print(f"kg U in core: {m_U}")

num_FAs = 21
num_pins = (17*17-25)*num_FAs

R_clad_in, R_clad_out, H_clad = 0.4177, 0.4750, 144.16
V_clad_pin = np.pi*(R_clad_out**2-R_clad_in**2)*H_clad # should be 23.1662 cc
V_clad_core = V_clad_pin*num_pins # cc of cladding in whole core
rho_clad = 6.56 # g/cc
# print(f"V_clad in core: {V_clad_core} == 128433.413 (check)")

c_list = [77.4808,100] # mgLi6/kgU
for c_i in c_list:
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
    for i in n_zr4_dict.keys():
        n_tot_pin += n_zr4_dict[i]
    
    print(f"c lithium-doped zircaloy-4 cladding | rho = {rho_clad_new:.4f} | 325 C / 600 K")
    # print(f"c suppposed to be {c_i} mg(Li-6)/kg(U) = tot {m_Li6_core*1000/correction:.0f} mg / {m_U:.0f} kg")
    # print(f"c but script applies correction: {correction:.6f}")
    print(f"c {c_i_corr:.4f} mg(Li-6)/kg(U) = tot {m_Li6_core*1000:.0f} mg / {m_U:.0f} kg")
    print(f"c tot N = {n_tot_pin:.10f} at/b-cm")
    print(f"m3101  3006.81c  {n_Li6_pin:.12f} ")
    print(f"       3007.81c  {n_Li7_pin:.12f} ")
    for i in n_zr4_dict.keys():
        i_wt_frac = n_zr4_dict[i] # (1-li6_at_dens)*
        print(f"      {i}.81c  {i_wt_frac:.8f} ")

