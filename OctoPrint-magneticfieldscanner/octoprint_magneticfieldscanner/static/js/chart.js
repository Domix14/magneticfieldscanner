function refreshPlot(data) {
    updateGraph(data);
}

function updateGraph(rawdata) {
    if (rawdata.length !== 0) {
        var points = rawdata.slice().sort((a, b) => a.z - b.z);
        var trace = {
            x: points.map(point => point.x),
            y: points.map(point => point.y),
            z: points.map(point => point.z),
            mode: 'markers',
            marker: {
                size: 3,
                color: points.map(point => point.value),
                colorscale: "Viridis",
                cmin: Math.min(...points.map(point => point.value)),
                cmax: Math.max(...points.map(point => point.value)),
                colorbar: { title: "Magnetic field strength [mT]" }
            },
            type: 'scatter3d'
        };

        Plotly.react('myDiv', [trace]);
    }
}

function plot(rawdata) {
    if (rawdata.length !== 0) {
        var layout = {
            width: 600,
            height: 500,
            margin: { t: 0, l: 0, b: 0 },
            scene: {
                camera: {
                    eye: {
                        x: 1.88,
                        y: -2.12,
                        z: 0.96
                    }
                }
            },
            sliders: [{
                pad: { t: 50 },
                currentvalue: {
                    prefix: "Percentages: ",
                    xanchor: "right",
                    font: { color: "#888", size: 12 }
                },
                steps: [],
                len: 0.9,
                x: 0.1,
                y: 0,
                active: 0
            }]
        };

        var points = rawdata.slice().sort((a, b) => a.z - b.z);
        var trace = {
            x: points.map(point => point.x),
            y: points.map(point => point.y),
            z: points.map(point => point.z),
            mode: 'markers',
            marker: {
                size: 3,
                color: points.map(point => point.value),
                colorscale: "Viridis",
                cmin: Math.min(...points.map(point => point.value)),
                cmax: Math.max(...points.map(point => point.value)),
                colorbar: { title: "Magnetic field strength [mT]" }
            },
            type: 'scatter3d'
        };

        var step_offset = 8;
        var interval = Math.floor(points.length / 30);

        for (var i = step_offset * interval; i < points.length; i += interval) {
            var df_slice = points.slice(0, i);
            layout.sliders[0].steps.push({
                method: "animate",
                label: Math.round(i / points.length * 100) + "%",
                args: [[null, {
                    x: df_slice.map(point => point.x),
                    y: df_slice.map(point => point.y),
                    z: df_slice.map(point => point.z),
                    marker: {
                        color: df_slice.map(point => point.value)
                    }
                }]],
                args2: [[null, {
                    title: "Slider switched to step: " + Math.round((step_offset * 1 / (points.length - 1) * 100 + (i / points.length * 100))) + "%"
                }]]
            });
        }

        const frames = [];
        const percentages = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1];

        for (let i = 0; i < percentages.length; i++) {
            const percentage = percentages[i];

            const frame = {
                name: percentage,
                data: [{
                    x: df_slice.map(point => point.x),
                    y: df_slice.map(point => point.y),
                    z: points.slice(0, points.length * percentage).map(point => point.z),
                    mode: 'markers',
                    marker: {
                        size: 3,
                        color: points.map(point => point.value),
                        colorscale: 'Viridis',
                        cmin: Math.min(...points.map(point => point.value)),
                        cmax: Math.max(...points.map(point => point.value)),
                        colorbar: { title: 'Magnetic field strength [mT]' }
                    },
                    type: 'scatter3d'
                }]
            };
            frames.push(frame);
        }

        const steps = percentages.map(percentage => ({
            label: percentage,
            method: 'animate',
            args: [[percentage], { mode: 'immediate' }]
        }));


        Plotly.newPlot('myDiv', {
            data: [trace],
            layout: {
                sliders: [{
                    pad: { t: 30 },
                    x: 0.05,
                    len: 0.95,
                    currentvalue: {
                        xanchor: 'right',
                        prefix: 'Percentages: ',
                        font: {
                            color: '#888',
                            size: 10
                        }
                    },
                    transition: { duration: 500 },
                    steps: steps
                }],
            },
            frames: frames
        })
    } else {
        // Kod dla braku danych
        var data = {
            x: [0],
            y: [0],
            z: [0],
            mode: 'markers',
            marker: {
                size: 3,
                colorscale: 'Viridis',
                cmin: 0,
                cmax: 0,
                colorbar: { title: 'Magnetic field strength [mT]' }
            },
            type: 'scatter3d'
        };

        Plotly.newPlot('myDiv', {
            data: [data]
        });
    }
}

function generateTestData() {
    var center = (20 - 1) / 2; // Środek sześcianu
    var points = [];
    var testData = [];
    for (var x = 0; x < 25; x++) {
        for (var y = 0; y < 25; y++) {
            for (var z = 0; z < 25; z++) {
                var distance = Math.max(Math.abs(x - center), Math.abs(y - center), Math.abs(z - center));
                var value = 20 - distance - 1; // Ustalanie wartości w oparciu o odległość od środka
                testData.push({
                    x: x,
                    y: y,
                    z: z,
                    value: value
                });
            }
        }
    }
    return testData
}


empty_data = []
plot(empty_data);
//plot(generateTestData());
