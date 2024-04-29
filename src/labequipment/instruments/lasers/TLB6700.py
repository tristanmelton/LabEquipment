import sys
import os

from time import sleep, time

from clr import * #pip install pythonnet
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import clr
from System.Text import StringBuilder


clr.AddReference('UsbDllWrap')
import clr
import Newport

class TLB6700:
    def refresh(self):
        """Connect to the laser; currently only supports a single laser"""
        self.npusb = Newport.USBComm.USB()
        self.npusb.OpenDevices(4106, True) #Product id = 4106 (dec) = 0x100a (hex)
        self.ndevices,self.keystrings = self.npusb.GetDeviceKeys('')
        if self.ndevices == 1:
            self.devicekey = self.keystrings[0] #Should be u'TLB-6700-LN SN1008'
            print(self.devicekey+' connected.')
            self.write('syst:mcon rem')
        else:
            print('{} laser devices detected.'.format(self.ndevices))
    
    def __init__(self):
        self.b = StringBuilder(64)
        self.refresh()

    #Basic I/O
    def query(self,text):
        """Query command used for everything"""
        self.b.Clear()
        self.npusb.Query(self.devicekey,text,self.b)
        return self.b.ToString()

    def write(self,text):
        """Returns error if command fails"""
        if text[-1] == '?':
            raise Exception('Query command sent.')
        if self.query(text) != u'OK':
            raise Exception('Command {} failed with response {}.'.format(text,self.b.ToString()))

    def msg(self,text):
        """Interprets communication type"""
        if text[-1] == '?':
            return self.query(text)
        else:
            self.write(text)

    #Set and read things
    def set_power(self,mW=''):
        """Set power in mW"""
        
        if self.query('sour:cpow?') != '1':
            self.query('sour:cpow 1')
            print('Switched to power control.')
            self.on()

        if isinstance(mW,float) or isinstance(mW,int):
            self.write('sour:pow:diod {}'.format(mW))
        else:
            return self.query('sour:pow:diod?')
    
    def read_power(self):
        """Return instantaneous power in mW"""
        return self.query('sens:pow:diod?')

    def set_current(self,mA=''):
        """Set current in mA"""

        if self.query('sour:cpow?') != '0':
            self.query('sour:cpow 0')
            print('Switched to current control.')
            self.on()

        if isinstance(mA,float) or isinstance(mA,int):
            self.write('sour:curr:diod {}'.format(mA))
        else:
            return self.query('sour:curr:diod?')

    def read_current(self):
        """Return instantaneous current in mA"""
        return self.query('sens:curr:diod?')

    def set_piezo(self,pc=''):
        """Set piezo as percentage"""
        if isinstance(pc,float) or isinstance(pc,int):
            self.write('sour:volt:piez {}'.format(pc))
        else:
            return self.query('sour:volt:piez?')

    def set_wavelength(self,wavelength='',waitstep=1,closeenough=0.01,timeout=60,wait=True):
        """Set wavelength in nm and track to it, if wait=True program will wait"""

        if isinstance(wavelength,float) or isinstance(wavelength,int):
            if wavelength < 1550 or wavelength > 1630: raise Exception('Wavelength out of range.')

            self.write('outp:scan:stop')
            sleep(waitstep)
            self.write('outp:trac 1') #needs wavelength tracking activated
            sleep(waitstep)
            if float(self.query('sour:wave?')) != wavelength:
                self.write('sour:wave {}'.format(wavelength))

            if wait:
                time0 = time()
                goodtime = time()
                flag = False
                while (time() - goodtime < 3) or (abs(float(self.query('sens:wave?'))-wavelength) > closeenough):
                    if flag == False:
                        goodtime = time()
                    if abs(float(self.query('sens:wave?'))-wavelength) < closeenough and flag == False:
                        flag = True
                        goodtime = time()
                    if time() - time0 > timeout:
                        raise Exception('{} sec timeout reached whilst waiting for wavelength {}.'.format(timeout,wavelength))
                    sleep(waitstep)
            self.write('outp:trac 0')
        else:
            return self.query('sour:wave?')

    def read_wavelength(self):
        """Return instantaneous wavelength in nm"""
        return self.query('sens:wave?')

    def tracking(self,trac=''):
        """Set tracking"""
        if isinstance(trac,bool) or isinstance(trac,int):
            self.write('outp:trac {}'.format(int(trac)))
        else:
            return self.query('outp:trac?')

    #Sweeps
    def setup_sweep(self,startwave=1520,stopwave=1570,speed=20,returnspeed='auto',scans=1):
        """Set up a sweep, wavelength in nm, speed in nm/s"""
        self.write('outp:scan:stop') #stop
        self.write('sour:wave:scancfg 0') #keep laser on during reverse sweep
        self.write('sour:wave:desscans {}'.format(scans))
        self.write('sour:wave:start {}'.format(startwave))
        self.write('sour:wave:stop {}'.format(stopwave))

        if speed > 20: raise Exception('Laser speed {} too fast.'.format(speed))
        self.write('sour:wave:slew:forw {}'.format(speed))

        if isinstance(returnspeed,int) or isinstance(returnspeed,float):
            if returnspeed > 20: raise Exception('Laser return speed {} too fast.'.format(returnspeed))
            self.write('sour:wave:slew:ret {}'.format(returnspeed))
        else:
            self.write('sour:wave:slew:ret {}'.format(speed))

    def cont_sweep(self,startwave=1520,stopwave=1570,speed=20,returnspeed='auto',scans=1):
        """Continuously sweep laser, wavelength in nm, speed in nm/s"""
        self.setup_sweep(startwave=startwave,stopwave=stopwave,speed=speed,returnspeed=returnspeed,scans=scans)
        sleep(1)
        self.write('outp:scan:start')

    def start_sweep(self,check=True):
        """Start sweep"""
        if check and (self.query('*OPC?') == '0'):
            raise Exception('Laser not ready.')
        self.write('outp:scan:start')

    #Laser on/off
    def on_delay(self):
        """Time delay between sending on command and laser starting, converted to seconds"""
        return float(self.query('ondelay?'))/1000
    
    def on(self,wait=True):
        """Turn laser on"""
        if self.query('outp:stat?') == '0':
            self.write('outp:stat 1')
            if wait:
                sleep(self.on_delay())
            print('Laser on')
   
    def off(self):
        """Turn laser off"""
        if self.query('outp:stat?') == '1':
            self.write('outp:stat 0')
            print('Laser off')

    def close(self):
        """Disconnect communication"""
        self.write('syst:mcon loc')
        self.npusb.CloseDevices()

    #Wavelength monitoring functions
    def volt_to_nm(self,voltage):
        """Convert wavelength voltage V to nm"""
        return (1570-1520)*voltage/10+1520

    def nm_to_volt(self,wave):
        """Convert wavelength nm to V"""
        return 10*(wave-1520)/(1570-1520)