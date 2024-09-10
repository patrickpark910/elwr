import numpy as np

# Constants
avogadro_number = 6.022e23  # atoms/mol

# Isotopic abundances for 4.3% enrichment
abundance_u235 = 0.043  # 4.3% U-235
abundance_u238 = 0.957  # 95.7% U-238

# Atomic masses (g/mol)
mass_u235 = 235.04393  # g/mol
mass_u238 = 238.05078  # g/mol
mass_o16 = 15.999  # g/mol

# Molar mass of uranium in enriched composition
molar_mass_uranium = abundance_u235 * mass_u235 + abundance_u238 * mass_u238

# Molar mass of UO2
molar_mass_uo2 = molar_mass_uranium + 2 * mass_o16

# Effective uranium density (g/cc)
uranium_density = 9.5  # g/cm^3

# Atom density of uranium in UO2 (U atoms per cm³)
atom_density_uranium = (uranium_density / molar_mass_uranium) * avogadro_number
print(atom_density_uranium*1e-24)
# Atom densities of U-235 and U-238
atom_density_u235 = atom_density_uranium * abundance_u235
atom_density_u238 = atom_density_uranium * abundance_u238

# Atom density of oxygen in UO2 (2 oxygen atoms per UO2 molecule)
atom_density_o16 = atom_density_uranium * 2  # Two oxygen atoms for each U atom

# Display results
print(f"Atom density of U-235: {atom_density_u235*1e-24:.12f} atoms/cm³")
print(f"Atom density of U-238: {atom_density_u238*1e-24:.12f} atoms/cm³")
print(f"Atom density of O-16:  {atom_density_o16*1e-24:.12f} atoms/cm³")
