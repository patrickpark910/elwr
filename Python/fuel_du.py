from sympy import symbols, N

# Constants
NA = 6.022e23  # Avogadro's number
density_DU = 18.95 # g/cc 

# Molar masses [g/mol]
molar_mass_U235 = 235.0439299
molar_mass_U238 = 238.0507882

# Enrichment level [1%e = 0.01]
e_list = [0.0025,] # 

for enrichment_235 in e_list:
    # Calculate average molar mass of the DU
    molar_mass_DU = enrichment_235 * molar_mass_U235 + (1 - enrichment_235) * molar_mass_U238

    # Calculate volume of 1 mol DU
    volume_DU = molar_mass_DU / density_DU

    # Calculate atomic number density of U
    n_U = NA / volume_DU  

    # Calculate atomic densities for U-235 and U-238
    n_U235 = enrichment_235 * n_U 
    n_U238 = (1 - enrichment_235) * n_U #

    print(f"for {enrichment_235*100} wt%e DU at {density_DU} g/cc\n",\
        f"U25: {(n_U235*1e-24):.6e}\n",\
        f"U28: {(n_U238*1e-24):.6e}\n", \
        f"sum: {(n_U235+n_U238)*1e-24:.11f}\n",\
        f"check: sum for 0.25%e DU should be 4.794E-02 from PNNL 2021")
