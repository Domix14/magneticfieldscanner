import random

import numpy as np
import plotly.graph_objs as go

# import pandas as pd

# luźno wjebane to sie tym prosze nie przejmować do przerobienai aktualnei to leci jako zewnetrzbny plik
# def wyjebansko():
#     with open("plik_wej.gcode", "r") as input_file, open("output_plik.gcode", "w") as output_file:
#         for line in input_file:
#             if not line.startswith("M109") and not line.startswith("M190") and not line.startswith("M104") and not line.startswith("M140"):
#                 # Split the line into individual words
#                 words = line.split()

#                 # Remove any words that start with "E"
#                 words = [word for word in words if not word.startswith("E")]
#     # Remove any words that start with "E"
#                 words = [word for word in words if not word.startswith("M104")]
#     # Remove any words that start with "E"
#                 words = [word for word in words if not word.startswith("M140")]

#                 # Reassemble the line with the remaining words
#                 new_line = " ".join(words) + "\n"

#                 output_file.write(new_line)


# class R_and_S_init():
#     rm = pyvisa.ResourceManager()
#     # replace with your instrument's VISA address
#     instr = rm.open_resource('TCPIP0::192.168.11.182::INSTR')
#     okno = 10
#     freq = 13.56
#     tablica = []


# def R_and_S_tuning():
#     # # Select the measurement parameters you want to measure
#     R_and_S_init.instr.write('SENS:FREQ:STAR ' + (R_and_S_init.freq -
#                              R_and_S_init.okno) + 'MHz')  # set the start frequency
#     R_and_S_init.instr.write('SENS:FREQ:STOP ' + (R_and_S_init.req +
#                              R_and_S_init.okno) + 'MHz')  # set the stop frequency
#     # define an S21 measurement named "MyMeasurement"
#     R_and_S_init.instr.write('CALC:PAR:DEF:EXT "MyMeasurement",Z21')
#     # # Set the analyzer to continuous measurement mode
#     R_and_S_init.instr.write('INITiate:CONTinuous ON')  # turn on continuous measurement


# def R_and_S_read_val():
#     R_and_S_init.instr.write('INITiate:CONTinuous OFF')  # wyłącz ciągły pomiar
#     R_and_S_init.instr.write('CALC:MARK2:MAX')
#     # print(instr.query_ascii_values('CALC:MARK2:Y?'))
#     value = R_and_S_init.instr.query_ascii_values('CALC:MARK2:Y?')
#     R_and_S_init.instr.write('INITiate:CONTinuous ON')
#     # print(value)
#     return value


# def print_3D(df):
#     color_table = []
#
#
#
#     # count colour table
#     for point in df["Value"]:
#         proportion = 1-(point - min(df["Value"]))/(max(df["Value"])-min(df["Value"]))
#         r = 176
#         g = int(proportion*256)
#         b = 0
#         color = f'rgb({r}, {g}, {b})'
#         color_table.append(color)
#
#
#     # Tworzenie wykresu Scatter3d
#     fig = go.Figure(go.Scatter3d(
#         x=df['X'],
#         y=df['Y'],
#         z=df['Z'],
#         mode='markers',
#         marker=dict(
#             colorscale='Viridis',
#             color = color_table,
#             opacity=0.4
#         )
#     ))
#     fig.show()


# path = r'D:\Studia\Python_code\OctoPrint\venv\Lib\site-packages\octoprint_showchart\scripts\data.csv'
# df = pd.read_csv(path, sep= ';')

# points = []
# center = (20 - 1) / 2  # Środek sześcianu
# for x in range(5):
#     for y in range(5):
#         for z in range(5):
#             distance = max(abs(x - center), abs(y - center), abs(z - center))
#             value = 20 - distance -1 # Ustalanie wartości w oparciu o odległość od środka
#             points.append((x, y, z, value))
#
# df = pd.DataFrame(points, columns=['X', 'Y', 'Z', 'Value'])
# print_3D(df)

def foo():
    x = np.linspace(0, 2 * np.pi, 100)
    y = R_and_S_read_val()

    R_and_S_init.tablica.append(R_and_S_read_val())
    # Tworzenie wykresu
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y))

    # Wyświetlanie wykresu
    fig.show()
