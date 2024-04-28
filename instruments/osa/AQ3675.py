import pyvisa

import pandas as pd

class AQ3675:
    def __init__(self, GPIB_address):
        self.address = GPIB_address
        self.rm = pyvisa.ResourceManager()
    def __enter__(self):
        self.osa = self.rm.open_resource(self.address)
        self.osa.timeout = 10e3
        
        return self
    def fetchData(self):
        x = self.osa.query(':TRAC:DATA:X? TRA')
        y = self.osa.query(':TRAC:DATA:Y? TRA')
        df = pd.DataFrame({'Wavelength':x.split(','),
                           'Intensity':y.split(',')})
        df = df.apply(pd.to_numeric,errors='coerce')
        
        return df
    def __exit__(self, exc_type, exc_value, traceback):
        self.osa.close()