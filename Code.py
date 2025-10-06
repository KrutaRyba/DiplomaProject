import osmnx

# 26.189690,50.628449,26.228657,50.642821
coords = [26.210933,50.635019,26.213604,50.636244]
print("START D")
features = osmnx.features.features_from_bbox(coords, {"building": True,})
network = osmnx.graph.graph_from_bbox(coords, truncate_by_edge = True)
print("END D")

_, ax = osmnx.plot.plot_graph(network, bgcolor = "#ffffff", edge_linewidth = 2, show = False, close = False)

streets = osmnx.graph_to_gdfs(network, nodes = False).fillna('')
# street_labels = dict()

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
    # center = edge["geometry"].centroid
    # try:
    #     if (text not in street_labels.keys()):
    #         street_labels[text] = (center.x, center.y, 1)
    # except:
    #     print("A")
    # else:
    #     street_labels[text] = (street_labels[text][0] + center.x, street_labels[text][1] + center.y, street_labels[text][2] + 1)

# for key, value in street_labels.items():
#     ax.annotate(key, (value[0] / value[2], value[1] / value[2]), color = "#000000", weight = "bold")

osmnx.plot.plot_footprints(features, ax = ax)

import matplotlib.pyplot as plt
plt.show()