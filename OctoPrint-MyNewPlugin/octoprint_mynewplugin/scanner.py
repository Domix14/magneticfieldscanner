import logging

import pyvisa


class Scanner():
    
    def __init__(self, freq, window):
        try:
            self.rm = pyvisa.ResourceManager()
            # replace with your instrument's VISA address
            self.instr = self.rm.open_resource('TCPIP0::192.168.1.169::INSTR')
            self.window = window
            self.freq = freq

            # # Select the measurement parameters you want to measure
            self.instr.write('SENS:FREQ:START ' + str(self.freq - self.window) + 'MHz')  # set the start frequency
            self.instr.write('SENS:FREQ:STOP ' + str(self.freq + self.window) + 'MHz')  # set the stop frequency
            # define an S21 measurement named "MyMeasurement"
            self.instr.write('CALC:PAR:DEF:EXT "MyMeasurement",Z21')
            self.instr.write('CALC:MARK:AOFF')
            self.instr.write('CALC:MARK1:STAT ON')
            # # Set the analyzer to continuous measurement mode
            self.instr.write('INITiate:CONTinuous ON')  # turn on continuous measurement
        except Exception as err:
            logging.error(f"Error while initializing PyVisa: {err}")

    def measure(self):
        self.instr.write('DISP:WIND1:TRAC1:Y:AUTO ON')
        self.instr.write('INITiate:CONTinuous OFF')  # wyłącz ciągły pomiar
        self.instr.write('CALC:MARK1:MAX')
        value = self.instr.query_ascii_values('CALC:MARK1:Y?')
        freq = self.instr.query_ascii_values('CALC:MARK1:X?')
        self.instr.write('INITiate:CONTinuous ON')
        return freq, value
