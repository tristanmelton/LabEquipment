# -*- coding: utf-8 -*-
"""
Created on Sat Jul  9 15:09:59 2022

@author: allen
"""
from instruments.oscilloscopes.TDS7404 import TDS7404
import matplotlib.pyplot as plt
import os
plt.close('all')

# OSC
OSC_address = 'GPIB0::3::INSTR'

path = '220709'
with TDS7404(OSC_address) as osc:
    data = osc.fetchData(channel=2)
    
plt.plot(data.Time,data.Volts)
data.to_csv(os.path.join(path,'Osc_ch2.csv'),index=False)


