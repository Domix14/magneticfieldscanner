import plotly.graph_objs as go
import numpy as np
import pandas as pd


class Plot_3D():

    def __init__(self):
        ...

    def start(self):

        # Przykładowe dane
        points = []
        center = (20 - 1) / 2  # Środek sześcianu
        for x in range(25):
            for y in range(25):
                for z in range(25):
                    distance = max(abs(x - center), abs(y - center), abs(z - center))
                    value = 20 - distance - 1  # Ustalanie wartości w oparciu o odległość od środka
                    points.append((x, y, z, value))

        df = pd.DataFrame(points, columns=['X', 'Y', 'Z', 'Value'])
        self.print_3D(df)

    def print_3D(self, raw_data):

        step_offset = 8
        df = raw_data.sort_values("Z")
        color_min = min(df["Value"])
        color_max = max(df["Value"])

        # Tworzenie wykresu Scatter3d
        fig = go.Figure()
        interval = int(df.shape[0] / 30)
        for step in np.arange(step_offset*interval, df.shape[0], interval):
            df_slice = df.head(step).copy()
            fig.add_trace(go.Scatter3d(
                x=df_slice['X'],
                y=df_slice['Y'],
                z=df_slice['Z'],
                mode='markers',
                marker=dict(
                    colorscale='Viridis',
                    color=df_slice["Value"],
                    opacity=0.4,
                    cmin=color_min,
                    cmax=color_max,
                    colorbar=dict(title='Magnetic field strength[mT]')
                )
            ))

        steps = []
        for i in range(len(fig.data)):
            percent = i / (len(fig.data) - 1) * 100
            step = dict(
                method="update",
                label=f"{int(percent)}%",
                args=[{"visible": [False] * len(fig.data)},
                      {"title": "Slider switched to step: " + str(int(step_offset* 1/(len(fig.data) - 1) * 100 + percent)) + "%"}],  # layout attribute
            )
            step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
            steps.append(step)

        # Tworzenie suwaka
        fig.update_layout(
            sliders=[dict(
                active=0,
                currentvalue={"prefix": "Percentages: "},
                pad={"t": 50},
                steps=steps
            )]
        )
        fig.show()
# Plot_3D().start()