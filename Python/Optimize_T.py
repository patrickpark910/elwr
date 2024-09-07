import numpy as np

# Molar masses
mm_T   = 3.016 # g/mol
mm_Li6 = 6.016 # g/mol

# Physical constants
mu = 1.66054 # b-mol/cm**2-at
avo = 6.022e23 # at/mol

# Reactor settings
e_U = 0.035
m_U = 4000*(e_U*235+(1-e_U)*238)/(32+(e_U*235+(1-e_U)*238)) # kg

def main():
    b_i = 19.9 # MWd/kgU of CLEAN core
    c_i = 70 # mgLi-6/kgU

    for c_i in [20,40,60,80,100,120,140,160,180]:

        print(f"RESULTS")
        print(f"After {b_i} MWd/kgU + initial {c_i} mgLi6/kgU:")
        print(f"T produced [g]               : {Calc_m_T(b_i,c_i)}")
        # print(f"k-eff after penalty at BU={b} : {Calc_k_c(b,c_i)}")
        print(f"k-eff penalty [Delta k]      : {0.001345*Calc_c_f(b_i,c_i)}")
        print(f"Li-6 left [mg/kgU]           : {Calc_c_f(b_i,c_i)}")
        print(f"Li-6 left [g]                : {Calc_c_f(b_i,c_i)/1000*m_U}")
        print(f"Li-6 burned [g]              : {(c_i-Calc_c_f(b_i,c_i))/1000*m_U}")
        print(f"New BU where k=1.03          : {Calc_B_penalty(b_i,c_i)}")

def Calc_m_T(b,c_i):
    return c_i/1000*m_U*(mm_T/mm_Li6)*(1-np.exp(-0.0512*b))

def Calc_k_c(b,c_i):
    return Calc_k_0(b)-0.001345*Calc_c_f(b,c_i)

def Calc_k_0(b):
    return -0.0103057*b+1.23164

def Calc_B_penalty(b,c_i):
    return (1.03-1.23164+0.001345*Calc_c_f(b,c_i))/(-0.0103057)

def Calc_c_f(b,c_i):
    return c_i*(np.exp(-0.0512*b))

if __name__ == '__main__':
    main()