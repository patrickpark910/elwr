import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

# Molar masses
mm_T   = 3.016 # g/mol
mm_Li6 = 6.015 # g/mol
mm_U235 = 235.044 # g/mol
mm_U238 = 238.051 # g/mol

# Physical constants
mu = 1.660539 # b-mol/cm**2-at
avo = 6.022e23 # at/mol

# Reactor materials
e_U   = 0.035
m_UO2 = 4000 # kg
m_U   = m_UO2*(e_U*mm_U235+(1-e_U)*mm_U238)/(32+(e_U*mm_U235+(1-e_U)*mm_U238)) # kg

# Reactor volumes
num_FAs = 21
num_pins = (17*17-25)*num_FAs
R_clad_in, R_clad_out, H_clad = 0.4177, 0.4750, 144.16
V_clad_pin = np.pi*(R_clad_out**2-R_clad_in**2)*H_clad
V_clad_core = V_clad_pin*num_pins # cc of cladding in whole core

def main():
    b_max  = 19.9 # MWd/kgU of CLEAN core at k=1.03
    b_step = 1e-1 # MWd/kgU

    c_list = [50,90,100,110,120,130] # list(range(60, 141, 5))
    T_solutions, b_solutions = [], []

    for c_0 in c_list: # mgLi6/kgU
        print(f"===============")
        print(f"Starting mgLi6/kgU   : {c_0:.4f}")
        
        b, m_T, c_i = 0, 0, c_0  # initial burnup, mass_T
        k = K_c(b,c_0) # initial k-eff (only to initialize k for while loop--not a real value, k-regression only true for b > 1)
        # print(k)

        n_Li6_i = c_i/mu/mm_Li6/V_clad_core/1000*m_U # at/b-cm
        
        print(f"Starting Li6 numdens : {n_Li6_i} (to check with MCNP mat gen script)")

        b_list, k_list, cf_list, cffrac_list, dmT_list, mT_list = [], [], [], [], [], []

        while k >= 1.030001 and b < b_max:
            b  += b_step
            b_list.append(b)
            
            # Calculate remaining Li6 after burnstep using Midpoint Rule
            # c_m = C_b(b_step/2,c_i,c_i) # use to APPROX midpoint c_m:   c_m = c_i exp(-sigma(c_i)*phi(c_i)*3e6*b_step/2) <-- /2
            c_f = C_b(b_step,c_i,c_i)   # use c_m to compute final c_f: c_f = c_i exp(-sigma(c_m)*phi(c_m)*3e6*b_step)
            cf_list.append(c_f)
            cffrac_list.append(c_f/c_0)
            # print(f"b, c_i, c_m, c_f: {b:.4f}, {c_i:.4f}, {c_m:.4f}, {c_f:.4f}") # useful to observe
            
            # Calculate incremental dmass_T made and add to cumulative mass_T
            dm_T = M_T(c_i,c_f)
            m_T += dm_T
            dmT_list.append(dm_T)
            mT_list.append(m_T)

            # Predict k-eff after this burnstep (with c_f mgLi6/kgU)
            k = K_c(b,c_f)
            k_list.append(k)        

            # Set c_f as the next burnstep's initial mgLi6/kgU
            c_i = c_f

        print(f"Predicted k-eff      :  {k:.6f}")
        print(f"...at MWd/kgU        : {b:.6f} ")
        print(f"Remaining mgLi6/kgU  : {c_f:.6f}")
        print(f"Tritium made [g]     : {m_T:.6f}")

        # Save this iteration's data to plot later
        df = pd.DataFrame({'MWd/kgU': b_list,'k-eff':k_list, 'Left mgLi6/kgU': cf_list,'Left %': cffrac_list,'g T made': dmT_list,'g T tot': mT_list})
        df.set_index('MWd/kgU', inplace=True)
        # df.to_csv(f'output-Li{str(c_0).zfill(3)}.csv')

        # Append this iteration's solutions to list of ALL solutions to be plotted by plot_results()
        T_solutions.append(m_T)
        b_solutions.append(b)

    # print(T_solutions)
    # print(b_solutions)
    # plot_results(c_list, T_solutions, b_solutions)

def Sigma(c):
    return (7.433510e-5*c**2 - 8.600433E-02*c + 7.264452E+01)*1e-24

def Phi(c):
    return 4.716128E+07*c**2 - 5.629420E+10*c + 2.783984e14

def M_T(c_i,c_f):
    return (c_i-c_f)*mm_T/mm_Li6*m_U/1000

def K_c(b,c):
    return K_0(b) - 0.905*0.03564/20*c # + 1.49241096E-06*c**2 - 1.55556423E-03*c

def K_0(b):
    return 7.703583E-05*b**2 - 1.194196E-02*b + 1.236691

def C_b(b,c_i,c):
    # print(f"sigma: {Sigma(c_b)*1e24:.2f} [b]")
    # print(f"phi  : {Phi(c_b):.2e}")
    return c_i*np.exp(-Sigma(c)*Phi(c) * 86400 * 35.26 * b)

def plot_results(c, T, b):
    fig, ax1 = plt.subplots()

    # Li-6 concentration vs. T produced
    c, T = np.array(c), np.array(T)
    c_T_Spline = make_interp_spline(c, T)
    c_ = np.linspace(c.min(), c.max(), 500)
    T_ = c_T_Spline(c_)
    ax1.plot(c_, T_, color='blue') # marker='o'
    ax1.plot(c, T, '.', color='blue') # marker='o'
    ax1.set_xlabel('Initial Li-6 concentration [mg/kgU]')
    ax1.set_ylabel('T produced [g]', color='b')
    ax1.tick_params(axis='y', labelcolor='b')

    # Li-6 concentration vs. Discharge burnup
    ax2 = ax1.twinx()
    b = np.array(b)
    c_b_Spline = make_interp_spline(c, b)
    b_ = c_b_Spline(c_)
    ax2.plot(c_, b_, color='red')
    ax2.plot(c, b, '.', color='red')
    ax2.set_ylabel('Discharge burnup [MWd/kgU]', color='r')
    ax2.tick_params(axis='y', labelcolor='r')

    # plt.grid(True)
    # plt.show()
    plt.savefig('Optimize_T.svg',format='svg',transparent=True)

if __name__ == '__main__':
    main()