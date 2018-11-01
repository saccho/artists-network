from numpy import ceil, max
from matplotlib.colors import LinearSegmentedColormap

colors = ['white', 'darkblue', 'skyblue', 'limegreen', 'yellow', 'orange', 'red']
values = range(len(colors))
vmax = ceil(max(values))
color_list = []
for value, color in zip(values, colors):
    color_list.append((value/vmax, color))
node_cmap = LinearSegmentedColormap.from_list('node_cmap', color_list)
