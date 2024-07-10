import numpy as np

def atom_densities_uranium_oxide(mass_density, enrichment):
    # Constants
    molar_mass_U235 = 235.0439299  # g/mol
    molar_mass_U238 = 238.0507882  # g/mol
    molar_mass_O16 = 15.999  # g/mol
    avogadro_number = 6.02214076e23  # atoms/mol
    
    # Calculate the molar mass of uranium in UO2 based on enrichment
    molar_mass_U = enrichment * molar_mass_U235 + (1 - enrichment) * molar_mass_U238
    molar_mass_UO2 = molar_mass_U + 2 * molar_mass_O16
    
    # Calculate the number of moles of UO2 per cm^3
    moles_UO2_per_cm3 = mass_density / molar_mass_UO2
    
    # Calculate the atom densities
    atom_density_UO2 = moles_UO2_per_cm3 * avogadro_number
    atom_density_U235 = enrichment * atom_density_UO2
    atom_density_U238 = (1 - enrichment) * atom_density_UO2
    atom_density_O16 = 2 * atom_density_UO2
    
    return {
        "U-235": atom_density_U235/1e24,
        "U-238": atom_density_U238/1e24,
        "O-16": atom_density_O16/1e24
    }

UO2_density = 18.9  # g/cm^3
UO2_enrich = 0.0296  # decimal enrichment: 5 wt% = 0.05
densities = atom_densities_uranium_oxide(UO2_density, UO2_enrich)

print("Atom densities (atoms/cm^3):")
for isotope, density in densities.items():
    print(f"{isotope}: {density:.8f}")
