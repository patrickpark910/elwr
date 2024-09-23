import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.interpolate import make_interp_spline
from matplotlib.ticker import MultipleLocator

# Molar masses
mm_T   = 3.016 # g/mol
mm_Li6 = 6.015 # g/mol
mm_U235 = 235.044 # g/mol
mm_U238 = 238.051 # g/mol

# Physical constants
mu = 1.660539 # b-mol/cm**2-at
avo = 6.022e23 # at/mol
lambda_T = 1.78287158e-9 # 1/s

# Reactor materials
e_U   = 0.035
m_UO2 = 4000 # kg
m_U   = m_UO2*(e_U*mm_U235+(1-e_U)*mm_U238)/(32+(e_U*mm_U235+(1-e_U)*mm_U238)) # kg

# Reactor volumes
num_FAs = 21
num_pins = (17*17-25)*num_FAs
R_clad_in, R_clad_out, H_clad = 0.4177, 0.4577, 144.16
V_clad_pin = np.pi*(R_clad_out**2-R_clad_in**2)*H_clad
V_clad_core = V_clad_pin*num_pins # cc of cladding in whole core

def main():
    b_max  = 15.0 # MWd/kgU of CLEAN core at k=1.03
    b_step = 1e-4 # MWd/kgU

    c_list = [70,90] # list(range(60, 141, 5))
    Tnd_solutions, Td_solutions, b_solutions = [], [], []

    for c_0 in c_list: # mgLi6/kgU
        print(f"===============")
        print(f"Initial [Li6]   : {c_0:.4f} MWd/kgU")
        
        b, m_T, m_T_nodecay, c_i = 0, 0, 0, c_0  # initial burnup, mass_T
        k = K_c(b,c_0) # initial k-eff (only to initialize k for while loop--not a real value, k-regression only true for b > 1)
        n_Li6_i = c_i/mu/mm_Li6/V_clad_core/1000*m_U # at/b-cm
        
        # print(f"Initial Li6 numdens : {n_Li6_i} (to check with MCNP mat gen script)")

        b_list, k_list, cf_list, cffrac_list, dmT_list, mT_list, mTd_list = [], [], [], [], [], [], []
        while k >= 1.030001 and b < b_max:
            b  += b_step
            t_step = 3.046317691790e+06*b_step # s/MWd/kgU * MWd/kgU
            b_list.append(b)
            
            # Calculate remaining Li6 after burnstep using Midpoint Rule
            c_m = C_b(b_step/2,c_i,c_i) # use to APPROX midpoint c_m:   c_m = c_i exp(-sigma(c_i)*phi(c_i)*3e6*b_step/2) <-- /2
            c_f = C_b(b_step,c_i,c_m)   # use c_m to compute final c_f: c_f = c_i exp(-sigma(c_m)*phi(c_m)*3e6*b_step)
            cf_list.append(c_f)
            cffrac_list.append(c_f/c_0)
            
            # Calculate incremental dmass_T made and add to cumulative mass_T
            dm_T = M_T(c_i,c_f)
            m_T  += dm_T
            m_T_nodecay += dm_T
            dmT_list.append(dm_T)
            mT_list.append(m_T_nodecay)

            m_T *= np.exp(-1*lambda_T*t_step) # <----------- DECAY STEP *****
            mTd_list.append(m_T)

            # Predict k-eff after this burnstep (with c_f mgLi6/kgU)
            k = K_c(b,c_f)
            k_list.append(k)        

            # Set c_f as the next burnstep's initial mgLi6/kgU
            c_i = c_f

        c_avg = calc_avg_Li(b_list,cf_list)
        # print(f"Predicted k-eff :  {k:.6f}")
        print(f"EOC burnup      : {b:.6f} MWd/kgU")
        print(f"Remaining [Li6] : {c_f:.6f} mg/kgU")
        print(f"Eff avg [Li6]   : {c_avg:.6f} mg/kgU")
        print(f"Tritium made    : {m_T:.6f} g")

        # Save this iteration's data to plot later
        df = pd.DataFrame({'MWd/kgU': b_list,'k-eff':k_list, 'Left mgLi6/kgU': cf_list,'Left %': cffrac_list,'g T made': dmT_list,'g T tot': mT_list, 'g T net': mTd_list})
        df.set_index('MWd/kgU', inplace=True)
        # df.to_csv(f'Predicted-SS-Li{str(c_0).zfill(3)}.csv')

        # Append this iteration's solutions to list of ALL solutions to be plotted by plot_results()
        Tnd_solutions.append(m_T_nodecay)
        Td_solutions.append(m_T)
        b_solutions.append(b)

    # print(T_solutions)
    # print(b_solutions)
    # plot_results(c_list, Tnd_solutions, Td_solutions, b_solutions)

def Sigma(c):
    return (6.920061E-05*c**2 - 7.745592E-02*c + 7.055463E+01)*1e-24

def Phi(c):
    return 4.243187E+07*c**2 - 4.875460E+10*c + 2.647080E+14

def M_T(c_i,c_f):
    return (c_i-c_f)*mm_T/mm_Li6*m_U/1000

def K_c(b,c):
    return K_0(b) + K_p(c)

def K_p(c):
    ''' k-eff penalty
     0 MWd/kgU: 1.255923E-06*c**2 - 1.273313E-03*c
     1 MWd/kgU: 1.086425E-06*c**2 - 1.154473E-03*c
     5 MWd/kgU: 1.574698E-06*c**2 - 1.107087E-03*c
    10 MWd/kgU: 1.294948E-06*c**2 - 9.991347E-04*c
    '''
    b00 = 1.255923E-06*c**2 - 1.273313E-03*c
    b01 = 1.086425E-06*c**2 - 1.154473E-03*c
    b05 = 1.574698E-06*c**2 - 1.107087E-03*c
    b10 = 1.294948E-06*c**2 - 9.991347E-04*c
    return b00 # 3/2*b01-1/2*b00

def K_0(b):
    return 3.158977E-05*b**2 - 8.960167E-03*b + 1.156364

def C_b(b,c_i,c):
    # print(f"sigma: {Sigma(c_b)*1e24:.2f} [b]")
    # print(f"phi  : {Phi(c_b):.2e}")
    return c_i*np.exp(-Sigma(c)*Phi(c) * 86400 * 35.26 * b)

def calc_avg_Li(b_list,c_list):
    ''' Given list of burnups (x) and [Li6] (y), calculates effective average Li-6 concentration
    '''
    # Initial guess for parameters a and b
    initial_guess = [70, -0.05]

    # Perform the curve fit
    params, covariance = curve_fit(exp, b_list, c_list, p0=initial_guess)

    # Extract parameters
    a, m = params
    a = max(c_list)
    # print(f"Estimated parameters: a = {a:.4f}, m = {m:.4f}")
    # print(f"Exponential model: y = {a:.4f} * e^({m:.4f} * x)")
    
    # m   = slope
    i,f = max(b_list), min(b_list)
    avg = (a/(f-i)/m)*(np.exp(m*f)-np.exp(m*i))
    # print(i,f,m,avg)
    
    # print(f"a, m: {a}, {m}")
    c_fit = exp(b_list,a,m) # a * np.exp(m * b_list)
    r_sq = r_sq_func(c_list, c_fit)
    # print(f"Coefficient of determination (R^2): {r_sq:.4f}")

    return avg

def exp(x, a, b):
    return a * np.exp(b * np.array(x))

def r_sq_func(y_true, y_pred):
    residuals = y_true - y_pred
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y_true - np.mean(y_true))**2)
    r_sq = 1 - (ss_res / ss_tot)
    return r_sq

def plot_results(c, Tnd, Td, b):
    fig, ax1 = plt.subplots()

    # Li-6 concentration vs. T produced
    c, Tnd, Td = np.array(c), np.array(Tnd), np.array(Td)
    c_Tnd_Spline = make_interp_spline(c, Tnd)
    c_Td_Spline = make_interp_spline(c, Td)
    c_ = np.linspace(c.min(), c.max(), 500)
    Tnd_ = c_Tnd_Spline(c_)
    Td_ = c_Td_Spline(c_)
    ax1.plot(c_, Tnd_, color='blue') # marker='o'
    ax1.plot(c, Tnd, '.', color='blue') # marker='o'
    ax1.plot(c_, Td_, color='blue') # marker='o'
    ax1.plot(c, Td, '.', color='blue') # marker='o'
    plt.fill_between(c_, Td_, Tnd_, where=(Tnd_ > Td_), facecolor='blue', alpha=0.25, interpolate=True, label='Area where cos(x) > sin(x)')
    ax1.set_xlabel('Initial Li-6 concentration [mg/kgU]')
    ax1.set_ylabel('T produced [g]', color='b')
    ax1.xaxis.set_minor_locator(MultipleLocator(5))
    ax1.tick_params(axis='y', labelcolor='b')

    # Li-6 concentration vs. Discharge burnup
    ax2 = ax1.twinx()
    b = np.array(b)
    c_b_Spline = make_interp_spline(c, b)
    b_ = c_b_Spline(c_)
    ax2.plot(c_, b_, color='red')
    ax2.plot(c, b, '.', color='red')
    ax2.set_ylabel('Cycle burnup [MWd/kgU]', color='r')
    ax2.tick_params(axis='y', labelcolor='r')

    # plt.grid(True)
    # plt.show()
    plt.savefig('Optimize_Tdc_SS.svg',format='svg',transparent=True) # ,bbox_inches=0,transparent=True)

if __name__ == '__main__':
    main()