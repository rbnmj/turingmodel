import plotly.graph_objs as go
import plotly.express as px
import numpy as np

from turing_model import TuringModel as tm

t_end = 2000
number_steps = 2000
t = np.linspace(0, t_end, number_steps)


#var = [N_a, N_b, A_a, A_b, H_1a, H_1b, H_2a, H_2b]
var0 = [2, 2.5, 2.5, 2, 0.08, 0.4, 0.08, 0.4, 0, 0, 0, 0, 0, 0]

var = []
k_1 = 5
k_2 = 0
d_Hmax1 = 0.001
d_Hmax2 = 0.001
model = tm(var0, t, k_1, k_2, d_Hmax1, d_Hmax2)
var = integ.odeint(tm.equations_wrapper, var0, t, args=(model,))


# Generate some sample data (replace this with your actual data)
time_steps = 2000
actor1_data = var[:, 4]  # Replace this with your first actor's data
actor2_data = var[:, 4]  # Replace this with your second actor's data

# Create the figure
fig = go.Figure()

# Add initial heatmap
initial_heatmap = go.Heatmap(z=[actor1_data[:1], actor2_data[:1]], zmin=-1, zmax=1, colorscale='RdBu')
fig.add_trace(initial_heatmap)

# Update function for animation frames
frames = []
for i in range(1, time_steps):
    frame = go.Frame(
        data=[go.Heatmap(z=[actor1_data[:i+1], actor2_data[:i+1]], zmin=-1, zmax=1, colorscale='RdBu')],
        name=f"frame_{i}"
    )
    frames.append(frame)

# Add frames to the figure
fig.frames = frames

# Configure layout
fig.update_layout(
    title='Actors Oscillation over Time',
    xaxis_title='Time',
    yaxis_title='Actors',
    yaxis=dict(
        tickmode='array',
        tickvals=[0, 1],
        ticktext=['Actor 1', 'Actor 2']
    ),
    updatemenus=[{
        'buttons': [
            {
                'args': [None, {'frame': {'duration': 100, 'redraw': True}, 'fromcurrent': True}],
                'label': 'Play',
                'method': 'animate',
            },
            {
                'args': [[None], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate',
                                  'transition': {'duration': 0}}],
                'label': 'Pause',
                'method': 'animate',
            }
        ],
        'direction': 'left',
        'pad': {'r': 10, 't': 87},
        'showactive': False,
        'type': 'buttons',
        'x': 0.1,
        'xanchor': 'right',
        'y': 0,
        'yanchor': 'top'
    }]
)

# Show the figure
fig.show()
