import numpy as np

c = (17**2-25)*21 #  # (17**2-25)*21
h = 144.16
breed_clad_cc = (np.pi*0.4577**2 - np.pi*0.4177**2)*h*c # (np.pi*0.4750**2 - np.pi*0.4177**2)*h*c 
gap_cc = (np.pi*0.4177**2 - np.pi*0.4095**2)*h*c
pellet_cc = np.pi*(0.4095**2)*h*c
water_cc = (2*0.625)**2*h*c - breed_clad_cc - gap_cc - pellet_cc

print(f"uo2 : {pellet_cc}")
print(f"gap : {gap_cc}")
print(f"clad: {breed_clad_cc}")
print(f"lwtr: {water_cc}")


for c in [(17**2-15**2)*8, (15**2-25)*8, (17**2-15**2)*4, (15**2-25)*4, (17**2-15**2)*1, (15**2-25)*1]:
	# c = (15**2-25)*21 #  # (17**2-25)*21
	h = 144.16
	breed_clad_cc = (np.pi*0.4750**2 - np.pi*0.4177**2)*h*c
	gap_cc = (np.pi*0.4177**2 - np.pi*0.4095**2)*h*c
	pellet_cc = (np.pi*0.4095**2)*h*c
	water_cc = 0.625**2*h*c

	p = 100e6/1.602e-13/197.7*2.442
	T = 3.01604928/6.022e23
	# print(p)
	fm = -1*breed_clad_cc*T*p
	# print(f'{fm:.6f}')