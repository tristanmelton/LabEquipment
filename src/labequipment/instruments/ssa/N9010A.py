import pyvisa

import numpy as np
import pandas as pd


class N9010A:
    def __init__(self, GPIB_address):
        self.address = GPIB_address
        self.rm = pyvisa.ResourceManager()
    def __enter__(self):
        self.exa = self.rm.open_resource(self.address)
        return self
    def fetchData(self):
        data = self.exa.query('CALC:DATA?').split(',')
        data = np.array(data)
        data = data.reshape((-1,2))
        df = pd.DataFrame(data,columns=['Frequency','Intensity'])
        df = df.apply(pd.to_numeric,errors='coerce')
        return df
    def send(self, command):
        self.exa.write(command)
    def get(self, command):
        msg = self.exa.read(command)
        return msg
    def __exit__(self, exc_type, exc_value, traceback):
        self.exa.close()
      