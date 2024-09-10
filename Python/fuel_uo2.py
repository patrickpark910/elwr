from sympy import symbols, N

# Constants
NA = 6.022e23  # Avogadro's number, atoms/mol
# density_UO2 = 10.78 # 10.96 # g/cm^3, density of UO2 / 10.96 pNNL test 
eff_dens_U = 9.5

# Molar masses in g/mol
mm_U235 = 235.0439299
mm_U238 = 238.0507882
mm_O = 15.999

# Enrichment level
e_list = [0.035, 0.043] #0.035,0.0025,] #,0.022] # 0.03 PNNL test

for e in e_list:
	# Calculate molar mass of enriched uranium
	mm_U = e*mm_U235 + (1-e)*mm_U238

	# Calculate molar mass of UO2
	mm_UO2 = mm_U + 2 * mm_O

	m_U235 = e*eff_dens_U
	m_U238 = (1-e)*eff_dens_U

	n_U    = eff_dens_U*NA/mm_U
	n_U235 = m_U235*NA/mm_U235
	n_U238 = m_U238*NA/mm_U238
	print(f"check: n_U = {n_U*1e-24} == n_U235+n_U238 = {(n_U235+n_U238)*1e-24} ")
	n_O    = 2 * n_U  # number density of Oxygen atoms, twice that of Uranium

	dens_UO2 = (n_U)*mm_UO2/NA # just n_U bc each n_UO2 = n_U

	print(f"for {e*100:.2f} wt%e at {eff_dens_U} gU/cc (= {dens_UO2:.2f} gUO2/cc)\n",\
		f"  O: {n_O*1e-24:.10f}\n", \
		f"U25: {n_U235*1e-24:.10f} $  {e*100:.2f} wt% U-235 \n",\
		f"U28: {n_U238*1e-24:.10f} $ {(1-e)*100:.2f} wt% U-238 \n", \
		f"sum: {(n_O*1e-24+n_U235*1e-24+n_U238*1e-24):.10f}\n")
