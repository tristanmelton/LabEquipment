# -*- coding: utf-8 -*-
"""
Created on Sat May 21 14:30:57 2022

@author: allen
"""

from instruments.osa.AQ3675 import AQ3675
import matplotlib.pyplot as plt
import os
plt.close('all')

# OSA
OSA_address = 'GPIB0::1::INSTR'

path = '220912_LLNL'
with AQ3675(OSA_address) as osa:
    data = osa.fetchData()
    
    
plt.plot(data.Wavelength,data.Intensity)
# plt.yscale('log')
data.to_csv(os.path.join(path,'ELMA.csv'),index=False)