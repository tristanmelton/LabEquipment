import time as tm
import numpy
import easy_scpi as spci


class DS1104(object):
    def __init__(self):
        self.instr = spci.Instrument("USB0::0x1AB1::0x04CE::DS1ZA203514719::INSTR")

        self.instr.connect()
    def __del__(self):
        self.instr.disconnect()
    
    def single(self):
        self.instr.write(":SING")
    def continuous(self):
        self.instr.write(":RUN")
    def stop(self):
        self.instr.write("STOP")

    def fetchData(self):
        tm.sleep(0.5)
        status = self.instr.query(":TRIG:STAT?")
        if status == "WAIT\n" or status == "RUN\n" or status == 'AUTO\n':
            self.instr.write("STOP")
            self.instr.write("RUN")
            tm.sleep(2.5)
            self.instr.write("STOP")

        self.instr.write(":WAV:MODE NORM")
        
        self.instr.write(":WAV:SOURCE CHAN1")
        self.instr.write(":WAV:MODE NORM")
        self.instr.write(":WAV:FORM ASC")
        rawdata1 = self.instr.query(":WAV:DATA?")[11:]

        self.instr.write(":WAV:SOURCE CHAN2")
        self.instr.write(":WAV:MODE NORM")
        self.instr.write(":WAV:FORM ASC")
        
        rawdata2 = self.instr.query(":WAV:DATA?")[11:]
        data_size = len(rawdata1)

        sample_rate = float(self.instr.query(":ACQ:SRAT?"))
        timescale = float(self.instr.query(":TIM:SCAL?"))
        timeoffset = float(self.instr.query(":TIM:OFFS?"))
        voltscale1 = float(self.instr.query(":CHAN1:SCAL?"))
        voltoffset1 = float(self.instr.query(":CHAN1:OFFS?"))

        voltscale2 = float(self.instr.query(":CHAN2:SCAL?"))
        voltoffset2 = float(self.instr.query(":CHAN2:OFFS?"))


        
        data1 = rawdata1.split(',')
        data1 = numpy.float64(numpy.array(data1))

        data2 = rawdata2.split(',')
        data2 = numpy.float64(numpy.array(data2))

        time = numpy.linspace(timeoffset - 6*timescale,
                              timeoffset + 6*timescale,
                              num=len(data1))
        
        if(time[-1] < 1e-3):
            time = time * 1e6
            tUnit = u"\u00B5\u0053"
        elif (time[-1] < 1):
            time = time * 1e3
            tUnit = "ms"
        else:
            tUnit = "s"
        
        info = [("Data Size", data_size),
                ("Sample Rate", sample_rate),
                ("Time Scale", timescale),
                ("Voltage Offset CH1", voltoffset1),
                ("Voltage Scale CH1", voltscale1),
                ("Voltage Offset CH2", voltoffset2),
                ("Voltage Scale CH2", voltscale2),
                ("Time Unit", tUnit)]
        #self.instr.write(":RUN")
        #self.instr.write(":KEY:FORC")

        return [time, tUnit, data1, data2, info]

