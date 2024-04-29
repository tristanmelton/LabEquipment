# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 08:03:57 2022

@author: allen
"""
from labequipment.instruments.ssa.E5052A import E5052A
import matplotlib.pyplot as plt
import os

import fnmatch

plt.close('all')

# OSA
SSA_address = 'GPIB0::17::INSTR'

path = '230103'
with E5052A(SSA_address) as ssa:
    data = ssa.fetchData()
    fc, power = ssa.getCarrier()
    print(f'fc: {fc:.2f}GHz, power: {power:.2f}dBm')
plt.semilogx(data.Frequency,data.PN)
plt.ylim(-140,0)
fc = str(round(fc,5)).replace('.','p')
power = str(round(power,2)).replace('.','p')
count = len(fnmatch.filter(os.listdir(path), '*.*'))

data.to_csv(os.path.join(path,f'Soliton' + str(count) + '.csv'),index=False)