import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider
import streamlit as st
import plotly
import plotly.graph_objects as go


# function to calculate z from inputs

def z_calc(av, fl, h, a_h):
    b_v = 12.5 * (1 + 10 * av - (av ** 2))
    w_f = ((6 / h) ** 0.3) * ((0.62 + 90 * (0.4 - av) ** 4) / (1 + b_v * a_h))
    value = fl * corr_f * conv_f * w_f
    return value

#variables
a_h = 0  # horizontal openings
conv_f = 0.07  # conversion factor
corr_f = 1  # correction facdftor

st.set_page_config(layout="wide")
st.title("Equivalent fire severity surface plot")
col1, col2 = st.columns(2)
with col1:
    # add slider
    H = st.slider('Height of room', 1.0, 10.0, 2.0)
    highlight_x = st.slider('Fuel load', 0, 1500, 232)
with col2:
    floor_area_input = st.number_input('Floor area:')
    vrt_window_input = st.number_input('Vertical window area:')
    if floor_area_input > 0 and vrt_window_input > 0:
        av_input = vrt_window_input / floor_area_input
        if av_input > 0.25:
            st.write(f'a_v = {av_input}. Out of bounds!')
        elif av_input < 0.025:
            st.write(f'a_v = {av_input}. Out of bounds!')
        else:
            highlight_y = av_input
            highlight_z = z_calc(highlight_y, highlight_x, H, a_h)
            st.write(f'a_v = {av_input}. T_e = {highlight_z}.')



# create fire load array
maxfl = 1500
minfl = 50
flstep = 10

flarr = np.arange(minfl, maxfl + flstep, flstep)

# create a_v values array
minav = 0.025
maxav = 0.25
avstep = 0.001

avarr = np.arange(minav, maxav + avstep, avstep)

# create result array to for plotting surface
resultarr = np.zeros((len(avarr), len(flarr)))
count = 0
for i in range(len(avarr)):
    for j in range(len(flarr)):
        b_v = 12.5 * (1 + 10 * avarr[i] - (avarr[i] ** 2))
        w_f = ((6 / H) ** 0.3) * ((0.62 + 90 * (0.4 - avarr[i]) ** 4) / (1 + b_v * a_h))
        value = flarr[j] * corr_f * conv_f * w_f
        resultarr[i][j] = value

z = resultarr
sh_0, sh_1 = z.shape
y, x = avarr, flarr

fig = go.Figure(data=[go.Surface(
     contours={
         "z": {"show": True, "start": 30, "end": 181, "color": "white", "size": 30, "highlight": True, "highlightcolor": "white", "width": 3},
     },
    z=z, x=x, y=y)])
#fig.update_traces(contours_z=dict(show=True, usecolormap=False, project_z=True))
fig.update_layout(title='Equivalent fire severity surface', autosize=False,
                  width=3000, height=750, margin=dict(l=0, r=60, b=10, t=90),

                  )
fig.update_layout(
    scene=dict(
        xaxis=dict(nticks=8, range=[0, 1600], ),
        yaxis=dict(nticks=8, range=[0, 0.26], ),
        zaxis=dict(nticks=8, range=[0, 500], ),
        xaxis_title='fire load',
        yaxis_title='a_v',
        zaxis_title='T_e')
)
fig.update_scenes(camera = dict(
    up=dict(x=0, y=0, z=1),
    center=dict(x=0, y=0, z=0),
    eye=dict(x=1.056, y=1.98, z=1.056)
))

fig.update_yaxes(automargin=True)
fig.update_xaxes(automargin=True)
# fig.update_traces(hidesurface=True)
#fig.update_traces(marker=dict(size=50, color='green'), selector=dict(type='surface', scene='scene'), x=[highlight_x],
                #  y=[highlight_y], z=[highlight_z])
#fig.add_trace(go.Scatter3d(x=[highlight_x], y=[highlight_y], z=[highlight_z], mode='markers', marker=dict(size=5, color='red')))
fig.add_scatter3d(x=[], y=[], z=[], mode='markers', marker=dict(size=1, color='yellow'))
if floor_area_input > 0 and vrt_window_input > 0:
    fig.add_trace(go.Scatter3d(x=[highlight_x], y=[highlight_y], z=[highlight_z], mode='markers'))

#with st.expander("Surface", expanded=True):
st.plotly_chart(fig, use_container_width=True, theme=None)

#
# fig = plt.figure()
# fig.set_figheight(15)
# fig.set_figwidth(15)
# ax = fig.add_subplot(111, projection='3d')
# avarr_mesh, flarr_mesh = np.meshgrid(avarr, flarr)
# surf = ax.plot_surface(flarr_mesh, avarr_mesh, resultarr.T, cmap=cm.coolwarm, linewidth=0, antialiased=False)
#
#
# ax.set_xlabel('fuel load')
# ax.set_ylabel('a_v')
# ax.set_zlabel('T_E')
# ax.set_title('Surface plot')
# ax.set_zlim(0,250)
# fig.colorbar(surf, shrink=0.5, aspect=5)
#
# axheight = fig.add_axes([0.1, 0.25, 0.0225, 0.63])
# h_slider = Slider(ax=axheight, label='Height', valmin=1, valmax=10, valinit=H, orientation="vertical")
#
# def update(val):
#     H = h_slider.val
#     ax.clear()
#     for i in range(len(avarr)):
#         for j in range(len(flarr)):
#             b_v = 12.5 * (1 + 10 * avarr[i] - (avarr[i] ** 2))
#             w_f = ((6 / H) ** 0.3) * ((0.62 + 90 * (0.4 - avarr[i]) ** 4) / (1 + b_v * a_h))
#             value = flarr[j] * corr_f * conv_f * w_f
#             resultarr[i][j] = value
#
#     surf = ax.plot_surface(flarr_mesh, avarr_mesh, resultarr.T, cmap=cm.coolwarm, linewidth=0, antialiased=False)
#     ax.set_zlim(0, 250)
#     ax.set_xlabel('fuel load')
#     ax.set_ylabel('a_v')
#     ax.set_zlabel('T_E')
#     ax.set_title('Surface plot')
#
#
# h_slider.on_changed(update)
#
# plt.show()
# st.pyplot(fig)
