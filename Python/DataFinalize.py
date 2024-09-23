import numpy as np
import pandas as pd
from DataConstants import *
import os 


def main():

    Zr_Clean  = A_Zr_000
    Zr_Clean['Batches'] = 3
    Zr_MaxT   = A_Zr_091 # A_Zr_077 (Results 5-2)
    Zr_MaxT['Batches'] = 3
    Zr_MixTPu = A_Zr_139 # A_Zr_139 (gives 90% WGPu) # A_Zr_154 (gives 93% WGPu)
    Zr_MixTPu['Batches'] = 1
    SS_Clean  = A_SS_000
    SS_Clean['Batches'] = 3
    SS_MaxT   = A_SS_057 # A_SS_054 (Results 5-2)
    SS_MaxT['Batches'] = 3
    SS_MixTPu = A_SS_079
    SS_MixTPu['Batches'] = 1

    for dataset in [Zr_Clean,Zr_MaxT,Zr_MixTPu]: # Zr_Clean,Zr_MaxT,Zr_MixTPu, SS_Clean,SS_MaxT,SS_MixTPu]: 
        batches    = dataset['Batches']
        cladding   = dataset['Cladding']
        bu_MWdkgU  = dataset['EOC burnup']
        bu_efpd    = bu_MWdkgU*MWdkgU_to_efpd # cycle length in full-power days
        cy_per_yr  = 365 / (bu_efpd + refuel_d)
        cf         = bu_efpd / (bu_efpd + refuel_d) * 100

        conc_Li6_i = dataset['Li6 initial'] 
        m_Li6_i    = conc_Li6_i * m_U / 1000
        conc_Li6_f = dataset['Li6 final'] 
        m_Li6_f    = conc_Li6_f * m_U / 1000
        m_Li6_d_c  = m_Li6_i - m_Li6_f       # g Li-6 depleted per cycle
        m_Li6_d_yr = m_Li6_d_c * cy_per_yr
        conc_Li6_e = dataset['Li6 eff avg'] 
        conc_Li6_d = conc_Li6_i - conc_Li6_e

        demand_U   = m_U * cy_per_yr / batches
        demand_SWU = demand_U * SWU_per_kgU
        m_Pu_c     = dataset['Pu produced']
        m_Pu_yr    = m_Pu_c * cy_per_yr
        m_T_c      = dataset['T produced']
        m_T_yr     = m_T_c * cy_per_yr
        f_Pu239    = dataset['Pu-239 frac'] # %

        print(f"=====================================")
        print(f"Cladding    : {cladding}")
        print(f"Li-6 initial: {conc_Li6_i:.4f} mg/kgU")
        print(f"Li initial  : {m_Li6_i/e_Li:.4f} g")
        print(f"Li-6 eff avg: {conc_Li6_e:.4f} mg/kgU")
        print(f"Li-6 final  : {conc_Li6_f:.4f} mg/kgU")
        print(f"Li depleted : {m_Li6_d_c/e_Li:.4f} g/cy")
        print(f"...         : {m_Li6_d_yr/e_Li:.4f} g/yr")
        print(f"-------------")
        print(f"Outage      : {refuel_d} days")
        print(f"Burnup      : {bu_MWdkgU:.4f} MWd/kgU")
        print(f"...         : {bu_efpd:.4f} EFPD")
        print(f"Cycles/yr   : {cy_per_yr:.4f} ")
        print(f"Capacity %  : {cf:.4f} %")
        print(f"U demand    : {m_U:.4f} kg/cy")
        print(f"...         : {demand_U:.4f} kg/yr")
        print(f"SWU demand  : {demand_SWU:.4f} SWU/yr")
        print(f"T produce   : {m_T_c:.4f} g/cy")
        print(f"...         : {m_T_yr:.4f} g/yr")
        print(f"Pu produce  : {m_Pu_c:.4f} kg/cy")
        print(f"...         : {m_Pu_yr:.4f} kg/yr")
        print(f"Pu-239 frac : {f_Pu239:.4f} %")
        print(f"\n")


if __name__ == "__main__":
    main()
