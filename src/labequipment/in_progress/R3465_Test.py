# -*- coding: utf-8 -*-
"""
Created on Sat May 21 14:30:57 2022

@author: allen
"""

from instruments.esa.R3465 import R3465
import matplotlib.pyplot as plt
import os
plt.close('all')

# ESA
ESA_address = 'GPIB0::18::INSTR'

path = '230119'
with R3465(ESA_address) as esa:
    data = esa.fetchData(startFreq=10e6,stopFreq=1e9,Navg=1)
    
    
plt.plot(data.Frequency,data.Intensity)
data.to_csv(os.path.join(path,'Soli1.csv'),index=False)