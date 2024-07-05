import numpy as np

# Dimensions of the cylinder
radius = 0.4095  # cm
height = 372.8690  # cm
density_UO2 = 9.5  # g/cm^3, density of UO2

NA = 6.022e23
molar_mass_U235 = 235.0439299
molar_mass_U238 = 238.0507882
molar_mass_O = 16

enrichment = 0.7204 / 100

# Calculate the volume of the cylinder
volume_cylinder = np.pi * radius**2 * height

# Calculate the total mass of UO2 in the cylinder
mass_UO2 = density_UO2 * volume_cylinder

# Calculate the mass fraction of Uranium in UO2
mass_fraction_U = (enrichment*molar_mass_U235 + (1-enrichment)*molar_mass_U238) / (enrichment*molar_mass_U235 + (1-enrichment)*molar_mass_U238 + 2*molar_mass_O)

# Calculate the mass of Uranium in the cylinder
mass_U = mass_UO2 * mass_fraction_U

print(volume_cylinder, mass_U)
