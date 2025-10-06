import osmnx

coords = [26.189690,50.628449,26.228657,50.642821]
print("START D")
features = osmnx.features.features_from_bbox(coords, {"building": True,})
network = osmnx.graph.graph_from_bbox(coords, truncate_by_edge = True)
print("END D")

_, ax = osmnx.plot.plot_graph(network, bgcolor = "#ffffff", edge_linewidth = 2, show = False, close = False)

streets = osmnx.graph_to_gdfs(network, nodes = False).fillna('')
street_labels = dict()

for _, edge in streets.iterrows():
    center = edge["geometry"].centroid
    text = edge["name"]
    if (text == "" or type(text) is not str): continue
    try:
        if (text not in street_labels.keys()):
            street_labels[text] = (center.x, center.y, 1)
    except:
        print("A")
    else:
        street_labels[text] = (street_labels[text][0] + center.x, street_labels[text][1] + center.y, street_labels[text][2] + 1)

for key, value in street_labels.items():
    ax.annotate(key, (value[0] / value[2], value[1] / value[2]), color = "#000000", weight = "bold")

osmnx.plot.plot_footprints(features, ax = ax)

import matplotlib.pyplot as plt
plt.show()