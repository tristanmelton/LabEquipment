import pyvisa

import numpy as np
import pandas as pd

from struct import unpack


class TDS7404:
    def __init__(self, GPIB_address):
        self.address = GPIB_address
        self.rm = pyvisa.ResourceManager()
    def __enter__(self):
        self.scope = self.rm.open_resource(self.address)
        return self
    def fetchData(self, channel):
        self.scope.write(f"DATA:SOU CH{channel}")
        self.scope.write('DATA:WIDTH 1')
        self.scope.write('DATA:ENC RPB')
        ymult = float(self.scope.query('WFMPRE:YMULT?'))
        yzero = float(self.scope.query('WFMPRE:YZERO?'))
        yoff = float(self.scope.query('WFMPRE:YOFF?'))
        xincr = float(self.scope.query('WFMPRE:XINCR?'))
        xdelay = float(self.scope.query('HORizontal:POSition?'))
        self.scope.write('CURVE?')
        data = self.scope.read_raw()
        headerlen = 2 + int(data[1])
        header = data[:headerlen]
        ADC_wave = data[headerlen:-1]
        ADC_wave = np.array(unpack('%sB' % len(ADC_wave),ADC_wave))
        Volts = (ADC_wave - yoff) * ymult  + yzero
        Time = np.arange(0, (xincr * len(Volts)), xincr)-((xincr * len(Volts))/2-xdelay)
        df = pd.DataFrame({'Time':Time-np.min(Time),
                           'Volts':Volts})
        return df
    def send(self, command):
        self.scope.write(command)
    def get(self, command):
        msg = self.scope.read(command)
        return msg
    def __exit__(self, exc_type, exc_value, traceback):
        self.scope.close()

