import pyvisa

import pandas as pd

class E5052A:
    def __init__(self, GPIB_address):
        self.address = GPIB_address
        self.rm = pyvisa.ResourceManager()
    def __enter__(self):
        self.ssa = self.rm.open_resource(self.address)
        return self
    def fetchData(self):
        x = self.ssa.query('CALC:PN1:DATA:XDAT?').split(',')
        y = self.ssa.query('CALC:PN1:DATA:RDAT?').split(',')
        df = pd.DataFrame({'Frequency':x,
                           'PN':y})
        df = df.apply(pd.to_numeric,errors='coerce')
        return df
    def getCarrier(self):
        carrier = self.ssa.query('CALC:PN1:DATA:CARR?')
        fc = float(carrier.split(',')[0])*1e-9
        power = float(carrier.split(',')[1])
        return (fc,power)
    def query(self,command):
        msg = self.ssa.query(command)
    def send(self, command):
        self.ssa.write(command)
    def get(self, command):
        msg = self.ssa.read(command)
        return msg
    def __exit__(self, exc_type, exc_value, traceback):
        self.ssa.close()
  