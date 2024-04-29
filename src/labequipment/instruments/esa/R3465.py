import pyvisa

import numpy as np
import pandas as pd

class R3465:
    def __init__(self, GPIB_address, samples=1001):
        self.address = GPIB_address
        self.rm = pyvisa.ResourceManager()
        self.samples = samples
        self.maxLevel = 14592
        self.minLevel = 1792
    def __enter__(self):
        self.esa = self.rm.open_resource(self.address)
        return self
    def fetchData(self,startFreq=0,stopFreq=3e9,dbpdiv=10,reflevel=10,Navg=3):
        self.esa.write(f'FA {startFreq}')
        self.esa.write(f'FB {stopFreq}')
        self.esa.write(f'DD {dbpdiv}')
        self.esa.write(f'RL {reflevel}')
        freq = np.linspace(startFreq,stopFreq,self.samples)
        DivOut = int(self.esa.query('DD?'))
        if DivOut == 0:
            Div = 10
        elif DivOut == 1:
            Div = 5
        elif DivOut == 2:
            Div = 2
        elif DivOut == 3:
            Div = 1
        elif DivOut == 4:
            Div = 0.5
        Ref = float(self.esa.query('RL?'))
        
        data = list()
        for N in range(Navg):
            self.esa.write('TAA?')
            dataTmp = list()
            for i in range(1001):
                tmp = self.esa.read()
                tmp = ((float(tmp)-self.minLevel)/(self.maxLevel-self.minLevel)-1)*10*Div+Ref
                dataTmp.append(10**(tmp*0.1))
            data.append(dataTmp)
        data = 10*np.log10(np.mean(np.array(data),axis=0))
        df = pd.DataFrame({'Frequency':freq,
                           'Intensity':data})
        
        
        return df
    def __exit__(self, exc_type, exc_value, traceback):
        self.esa.close()
