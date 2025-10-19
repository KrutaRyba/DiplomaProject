import osmnx
import numpy

# default
osmnx.settings.use_cache = True

# 26.189690,50.628449,26.228657,50.642821
#coords = [26.210933,50.635019,26.213604,50.636244]
center_point = [50.635678, 26.212011]
zoom_level = 16
hor_dist = (40075016.686 * numpy.cos(numpy.radians(center_point[0]))) / numpy.exp2(zoom_level)

print("START D")
features = osmnx.features.features_from_point(center_point, {"building": True,}, hor_dist / 2)
network = osmnx.graph.graph_from_point(center_point, hor_dist / 2, truncate_by_edge = True)
#admin = osmnx.features.features_from_point(center_point, {"admin_level": "4"}, hor_dist / 2)
print("END D")

_, ax = osmnx.plot.plot_graph(network, bgcolor = "#ffffff", edge_linewidth = 2, show = False, close = False)

streets = osmnx.graph_to_gdfs(network, nodes = False).fillna('')

import numpy

for _, edge in streets.iterrows():
    text = edge["name"]
    if (text == "" or type(text) is not str): continue
    # idx = 1 ???
    idx = int(len(edge["geometry"].coords) / 2)
    if (idx <= 0): continue
    a = edge["geometry"].coords[idx - 1]
    b = edge["geometry"].coords[idx]
    delta = (a[1] - b[1], a[0] - b[0])
    angle = numpy.rad2deg(numpy.atan2(delta[0], delta[1]))
    if (angle > 90.0): angle = angle - 180
    elif (angle < -90): angle = angle + 180
    ax.annotate(text, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2),
                horizontalalignment = "center", verticalalignment= "center",
                transform_rotates_text = True, rotation_mode = "anchor", rotation = angle,
                color = "#000000", weight = "bold", fontsize= "small")

osmnx.plot.plot_footprints(features, ax = ax)

import matplotlib.pyplot as plt
plt.show()