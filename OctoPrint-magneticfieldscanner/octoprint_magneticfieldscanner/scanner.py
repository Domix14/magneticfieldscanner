import logging

import pyvisa


class Scanner:
    def __init__(self):
        self.connected = False
        self.ip = ""
        self.freq = 0
        self.window = 0
        self.instr = None

    def connect(self, ip, freq, window):
        try:
            self.rm = pyvisa.ResourceManager()
            # replace with your instrument's VISA address
            self.window = window
            self.freq = freq
            self.ip = ip
            self.instr = self.rm.open_resource(f"TCPIP0::{self.ip}::INSTR")

            # Set the frequency span
            self.instr.write(f"FREQ:SPAN {self.window}Hz")

            # Set the center frequency
            self.instr.write(f"FREQ:CENT {self.freq}Hz")

            # Set the measurement type to S21
            self.instr.write("CALC:PAR:DEF:EXT 'MyMeasurement', 'S21'")

            # Turn off all markers
            self.instr.write("CALC:MARK:AOFF")

            # Turn on Marker 1 and set it to the peak
            self.instr.write("CALC:MARK1:STAT ON")
            self.instr.write("CALC:MARK1:MAX")

            # Set the analyzer to continuous measurement mode
            self.instr.write("INITiate:CONTinuous ON")  # turn on continuous measurement

            self.connected = True
        except Exception as err:
            logging.error(f"Error while initializing PyVisa: {err}")
            self.connected = False

        return self.connected

    def measure(self):
        self.instr.write("DISP:WIND1:TRAC1:Y:AUTO ON")
        self.instr.write("INITiate:CONTinuous OFF")  # wyłącz ciągły pomiar
        self.instr.write("CALC:MARK1:MAX")
        value = self.instr.query_ascii_values("CALC:MARK1:Y?")
        freq = self.instr.query_ascii_values("CALC:MARK1:X?")
        self.instr.write("INITiate:CONTinuous ON")
        return freq, value
