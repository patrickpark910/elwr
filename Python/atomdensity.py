from sympy import symbols, N

# Constants
NA = 6.022e23  # Avogadro's number, atoms/mol
density_UO2 = 9.5 # 10.96 # g/cm^3, density of UO2 / 10.96 pNNL test 

# Molar masses in g/mol
molar_mass_U235 = 235.0439299
molar_mass_U238 = 238.0507882
molar_mass_O = 16

# Enrichment level
e_list = [0.04,0.022] # 0.03 PNNL test

for enrichment_235 in e_list:
	# Calculate average molar mass of enriched uranium
	average_molar_mass_U = enrichment_235 * molar_mass_U235 + (1 - enrichment_235) * molar_mass_U238

	# Calculate molar mass of UO2
	molar_mass_UO2 = average_molar_mass_U + 2 * molar_mass_O

	# Calculate volume of one mole of UO2 using density
	volume_mole_UO2 = molar_mass_UO2 / density_UO2

	# Calculate atomic number density of Uranium and Oxygen in UO2
	n_U = NA / volume_mole_UO2  # number density of Uranium atoms
	n_O = 2 * n_U  # number density of Oxygen atoms, twice that of Uranium

	# Calculate atomic densities for U-235 and U-238
	n_U235 = enrichment_235 * n_U 
	n_U238 = (1 - enrichment_235) * n_U #

	print(f"for {enrichment_235*100} wt%e at {density_UO2} g/cc\n",\
		f"  O: {n_O*1e-24}\n", \
		f"U25: {n_U235*1e-24}\n",\
		f"U28: {n_U238*1e-24}\n", \
		f"sum: {(n_O*1e-24+n_U235*1e-24+n_U238*1e-24)}\n")
