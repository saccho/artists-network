import numpy as np
import matplotlib.colors as clr

colors = ['white', 'darkblue', 'skyblue', 'limegreen', 'yellow', 'orange', 'red']
values = range(len(colors))

vmax = np.ceil(np.max(values))
color_list = []
for value, color in zip(values, colors):
    color_list.append((value/vmax, color))
node_color_map = clr.LinearSegmentedColormap.from_list('custom_cmap', color_list)
