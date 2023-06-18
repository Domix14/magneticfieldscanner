import logging

import pyvisa
import time

class Scanner:
    def __init__(self):
        self.connected = False
        self.ip = ""
        self.freq = 0
        self.window = 0
        self.instr = None
        self.ref_level_offset = 0
        self.RBW=0

    def connect(self, ip, freq, window, ref_level_offset, RBW):
        try:
            self.rm = pyvisa.ResourceManager()
            # replace with your instrument's VISA address
            self.window = window
            self.freq = freq
            self.ip = ip
            self.ref_level_offset=ref_level_offset
            self.RBW=RBW
            self.instr = self.rm.open_resource(f"TCPIP0::{self.ip}::INSTR")

            self.instr.write("*RST")
            # # Select the measurement parameters you want to measure
            self.instr.write(
                f"SENS:FREQ:START {self.freq - self.window}MHz"
            )  # set the start frequency
            self.instr.write(
                f"SENS:FREQ:STOP {self.freq + self.window}MHz"
            )  # set the stop frequency
            # define an S21 measurement named "MyMeasurement"
            self.instr.write(f"SENS:BWID {self.RBW} Hz")
            self.instr.write('CALC:PAR:DEF:EXT "MyMeasurement",s12')
            self.instr.write("CALC:MARK:AOFF")
            self.instr.write("CALC:MARK1:STAT ON")
            # # Set the analyzer to continuous measurement mode
            self.instr.write("INITiate:CONTinuous ON")  # turn on continuous measurement

            self.instr.write(f"DISP:WIND:TRAC:Y:RLEV:OFFS {self.ref_level_offset}")
            
            self.connected = True
        except Exception as err:
            logging.error(f"Error while initializing PyVisa: {err}")
            self.connected = False

        return self.connected

    def disconnect(self):
        try:
            self.rm.close()
        except Exception as err:
            logging.error(f"Error while closing PyVisa connection: {err}")

        self.connected = False

    def measure(self):
        self.instr.write("CALC:TRAC1:CLE")
        self.instr.write("DISP:WIND1:TRAC1:Y:AUTO ON")
        
        #self.instr.write("INITiate:CONTinuous OFF")  # wyłącz ciągły pomiar
        self.instr.write("CALC:MARK1:MAX")
        self.instr.write("DISP:TRAC:MODE MAXH")
        self.instr.write("SENSE:AVERAGE ON")
        
        time.sleep(0.1)
        value = self.instr.query_ascii_values("CALC:MARK1:Y?")[0]
        freq = self.instr.query_ascii_values("CALC:MARK1:X?")[0]
        #time.sleep(0.1)
        #self.instr.write("INITiate:CONTinuous ON")
        return freq, value