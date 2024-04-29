# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 00:18:42 2022

@author: allen
"""
from labequipment.instruments.ssa.N9010A import N9010A
import matplotlib.pyplot as plt
import os
plt.close('all')

# EXA
EXA_address = 'GPIB0::18::INSTR'

path = '220725'
with N9010A(EXA_address) as exa:
    data = exa.fetchData()
    
    
plt.plot(data.Frequency,data.Intensity)
data.to_csv(os.path.join(path,'ESA_IQphaseShifter_source_I0_Q0.csv'),index=False)
