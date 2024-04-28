import pyvisa
import numpy as np
import pandas as pd

class E4440A:
    def __init__(self, GPIB_address='GPIB0::18::INSTR'):
        self.address = GPIB_address
        self.rm = pyvisa.ResourceManager()
    def __enter__(self):
        self.esa = self.rm.open_resource(self.address)
        return self
        
    def fetchData(self,startFreq=-1,stopFreq=-1):
        if startFreq != -1:
            self.esa.write(f'SENS:FREQ:STAR {float(startFreq) / float(1e9)} GHz')
        if stopFreq != -1:
            self.esa.write(f'SENS:FREQ:STOP {float(stopFreq) / float(1e9)} GHz')

        data=self.esa.query('TRAC:DATA? TRACE1')
        freqStart=float(self.esa.query('SENS:FREQ:STAR?'))
        freqStop=float(self.esa.query('SENS:FREQ:STOP?'))
        step=float(self.esa.query('SENS:FREQ:CENT:STEP:INCR?'))

        intensity=np.array([float(i) for i in data.split(',')])
        freq=np.linspace(freqStart,freqStop,len(intensity))
                
        df = pd.DataFrame({'Frequency':freq,
                           'Intensity':intensity})

        return df

    def __exit__(self, exc_type, exc_value, traceback):
        self.esa.close()