#!/usr/bin/env python
# coding: utf-8

"""
The units for this script is mm, N, tonne, s, MPa.
The final results include a true stress-plastic strain curve and its corresponding data that can be imported to ABAQUS directly.
"""
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

e_stress0 = 900 # yield strength
e_stressu = 1000 # ultimate strength
elo = 0.09 # Elongation
E = 200000 # Young's modulus

e_strainu = 100*(elo-e_stressu/E) # uniform strain, plastic strain at the end of uniform elongation
n = np.log(e_stressu/e_stress0)/np.log(e_strainu/0.2)# strain hardening exponent, better obtain with the fitting of experimental curves

e_stress = np.linspace(e_stress0, e_stressu, 20)
e_strain = e_stress/E + 0.002*(e_stress/e_stress0)**(1/n) # Ramberg_Osgood_relationship

t_strain = np.log(1+e_strain)
t_stress = e_stress*(1+e_strain)
p_strain = t_strain-t_stress/E

stress_strain_df = pd.DataFrame({'true stress': t_stress, 'plastic strain': p_strain})
print(stress_strain_df)
stress_strain_df.to_excel("M12_trueStress_plasticStrain.xls")

stress_strain_df.plot(x='plastic strain', y='true stress', kind='line')
plt.show()


