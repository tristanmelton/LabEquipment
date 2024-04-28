import pyvisa

class SG384:
    def __init__(self, GPIB_address):
        self.address = GPIB_address
        self.rm = pyvisa.ResourceManager()
    def __enter__(self):
        self.sg = self.rm.open_resource(self.address)
        self.sg.write('ENBR 1')
        self.sg.write('AMPR 1 vpp')
        return self
    def tuneFreq(self,freq):
        self.sg.write(f'FREQ {freq}')
    def tuneAmp(self,amp):
        self.sg.write(f'AMPR {amp}')
    def query(self,command):
        msg = self.sg.query(command)
        return msg
    def send(self,command):
        self.sg.write(command)
    def __exit__(self, exc_type, exc_value, traceback):
        self.sg.write('ENBR 0')
        self.sg.close()