import random

import plotly.graph_objs as go
# import numpy as np
# import pandas as pd

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
    y = np.sin(x)

    # Tworzenie wykresu
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y))



    # Wyświetlanie wykresu
    fig.show()