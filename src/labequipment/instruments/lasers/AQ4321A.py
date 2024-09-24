import pyvisa
import time

class AQ4321A:
    def __init__(self, GPIB_address='GPIB0::24::INSTR'):
        self.address = GPIB_address
        self.rm = pyvisa.ResourceManager()
    def __enter__(self):
        self.laser = self.rm.open_resource(self.address)
        return self
        
    def unlock(self):
        if self.query('LOCK?') == '1':
            self.laser.write('LOCK0/4321')
    def enable_output(self):
        self.laser.write("L1")
    def disable_output(self):
        self.laser.write("L0")
    def is_output_on(self):
        return self.laser.query("L?")
    def set_power(self, power_dbm):
        if power_dbm < -20:
            return -1
        elif power_dbm > 8:
            return -2
        self.laser.write('TPDB'+str(power_dbm))
        return 0
    def get_power(self):
        return float(self.laser.query('TPDB?'))
    
    def set_wavelength(self, wavelength):
        if wavelength < 1480:
            return -1
        elif wavelength > 1580:
            return -2
        self.laser.write('TWL'+str(wavelength))
    def get_wavelength(self):
        return float(self.laser.query('TWL?'))
    
    def set_sweep_min(self, wavelength):
        if wavelength < 1480:
            return -1
        elif wavelength > 1580:
            return -2
        self.laser.write('TSTAWL'+str(wavelength))
    def get_sweep_min(self):
        return float(self.laser.query('TSTAWL?'))

    def set_sweep_max(self, wavelength):
        if wavelength < 1480:
            return -1
        elif wavelength > 1580:
            return -2
        elif wavelength < float(self.get_sweep_min()):
            return -3
        self.laser.write('TSTPWL'+str(wavelength))
    def get_sweep_max(self):
        return float(self.laser.query('TSTPWL?'))       

    def set_sweep_time(self, time):
        if time < 1:
            return -1
        elif time > 99999:
            return -2
        self.laser.write('TSWET'+str(time))
    def get_sweep_time(self):
        return float(self.laser.query('TSWET?'))

    def start_sweep(self):
        self.laser.write('TSWM1')
        self.enable_output()
        time.sleep(2)
        sweep_time = self.get_sweep_time()
        self.laser.write('TSGL')
        time.sleep(sweep_time)

    def set_linewidth_narrow(self):
        self.laser.write("TLINEWIDTH0")
    def set_linewidth_broad(self):
        self.laser.write("TLINEWIDTH1")
    def get_linewidth_type(self):
        return float(self.laser.query("TLINEWIDTH?"))

    def query(self,command):
        return self.laser.query(command)

    def __exit__(self, exc_type, exc_value, traceback):
        self.laser.close()
