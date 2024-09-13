#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 20:17:00 2024

@author: aglaser
"""

import numpy as np

# --------------------------------------------------------------

def keff(b):
    
    """
    Retuns the value of k(eff) for a given burnup
    """
    
    return 7.703583E-05*b**2 - 1.194196E-02*b + 1.236691 # 1.235 - 0.01025 * b

# --------------------------------------------------------------

def sigma(l):
    
    """
    Returns the lithium (105) cross section as a function of loading
    """
    
    return 7.433510E-05*l**2 - 8.600433E-02*l + 7.264452E+01

# --------------------------------------------------------------

def deltak(l):
    
    """
    Returns the k(eff) penalty as a function of loading
    """
        
    return 0.000001492411 * l**2 - 0.001555564 * l 



# --------------------------------------------------------------

def fracreduction(l,deltab):
    
    """
    Returns fractional reduction of lithium concentration
    based on current lithium loading and burnup increment
    """
    
    return np.exp(-sigma(l) * 0.0008225 * deltab)


#%% 

b = 0
k0 = 1.33 # 1.235

l0 = 104  # Initial lithium loading
bi = 1e-4  # Burnup increment per cycle

k = k0 + deltak(l0)
l = l0

while k > 1.03:
    
    l *= fracreduction(sigma(l),bi)
    
    b += bi
    
    k = keff(b) + deltak(l)
    
tritium = (l0 - l) * 3526 * 3.016/6.015 / 1000

print('Initial loading ..... [mg/kg]: ', l0)
print('Residual loading .... [mg/kg]: ', round(10*l)/10)
print('Total tritium ........... [g]: ', round(10*tritium)/10)
print('Discharge burnup ... [MWd/kg]: ', round(10*b)/10)

# --------------------------------------------------------------
# THE END
# --------------------------------------------------------------
