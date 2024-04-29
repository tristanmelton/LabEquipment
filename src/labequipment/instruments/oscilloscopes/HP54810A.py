import pyvisa

import numpy as np
import pandas as pd

class HP54810A:
    def __init__(self, GPIB_address):
        self.address = GPIB_address
        self.rm = pyvisa.ResourceManager()
    def __enter__(self):
        self.scope = self.rm.open_resource(self.address)
        self.scope.timeout = 2000
        self.scope.write(':WAVEFORM:SOURCE CHAN1') 
        self.scope.write(':TIMEBASE:MODE MAIN')
        self.scope.write(':ACQUIRE:TYPE NORMAL')
        self.scope.write(':ACQUIRE:COUNT 1')
        self.scope.write(':ACQUIRE:POINTS 5000')
        self.scope.write(':WAV:POINTS:MODE RAW')
        self.scope.write(':WAV:POINTS 5000')
        self.scope.write(':WAVEFORM:FORMAT ASCii')
        return self
    def fetchData(self):
        preambleBlock = self.scope.query(':WAVEFORM:PREAMBLE?')
        RawData = self.scope.query(':WAV:DATA?')
        RawData = RawData.replace('\r\n\x00','')
        RawData = RawData.split('\n')[0]
        RawData = [float(i) for i in RawData.split(',')]
        RawData = np.array(RawData)
        preambleBlock = preambleBlock.split(',')
        XIncrement = float(preambleBlock[4]) # in seconds
        XData = (XIncrement*(np.arange(len(RawData)))) - XIncrement
        YData = RawData

        df = pd.DataFrame({'Time':XData,
                           'Volts':YData})
        return df
    def send(self, command):
        self.scope.write(command)
    def get(self):
        msg = self.scope.read()
        return msg
    def __exit__(self, exc_type, exc_value, traceback):
        self.scope.close()
