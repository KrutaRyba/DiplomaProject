import osmnx
from osmnx import utils_geo
import numpy
import matplotlib.pyplot as plt
# default
osmnx.settings.use_cache = True

# 26.189690,50.628449,26.228657,50.642821
#coords = [26.210933,50.635019,26.213604,50.636244]
center_point = [50.635678, 26.212011]
zoom_level = 18
hor_dist = (40075016.686 * numpy.cos(numpy.radians(center_point[0]))) / numpy.exp2(zoom_level)
bbox = utils_geo.bbox_from_point(center_point, hor_dist)
print("START D")
features = osmnx.features.features_from_bbox(bbox, {"building": True,})
network = osmnx.graph.graph_from_bbox(bbox, truncate_by_edge = True, simplify = True)
#admin = osmnx.features.features_from_point(center_point, {"admin_level": "4"}, hor_dist / 2)
print("END D")

dpi = 150
figsize = (8, 8)

_, ax = osmnx.plot.plot_graph(network, bgcolor = "#ffffff", edge_linewidth = 2, bbox = bbox, show = False, close = False, dpi = dpi)

streets = osmnx.graph_to_gdfs(network, nodes = False, fill_edge_geometry = True).fillna('')

import numpy

for _, edge in streets.iterrows():
    text = edge["name"]
    if (text == "" or type(text) is not str): continue
    idx = 1
    # idx = int(len(edge["geometry"].coords) / 2)
    if (idx <= 0): continue
    a = edge["geometry"].coords[idx - 1]
    b = edge["geometry"].coords[idx]
    delta = (a[1] - b[1], a[0] - b[0])
    angle = numpy.rad2deg(numpy.atan2(delta[0], delta[1]))
    if (angle > 90.0): angle = angle - 180
    elif (angle < -90): angle = angle + 180
    annotation = ax.annotate(text, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2),
                horizontalalignment = "center", verticalalignment= "center",
                transform_rotates_text = True, rotation_mode = "anchor", rotation = angle,
                color = "#000000", weight = "bold", fontsize= "small")
    bbox_a = plt.gca().transData.inverted().transform_bbox(annotation.get_window_extent())
    s = edge["geometry"].coords[0]
    e = edge["geometry"].coords[-1]
    street_len = numpy.sqrt(numpy.power(s[0] - e[0], 2) + numpy.power(s[1] - e[1], 2))
    label_len = numpy.sqrt(numpy.power(bbox_a.x0 - bbox_a.x1, 2) + numpy.power(bbox_a.y0 - bbox_a.y1, 2))
    if (label_len > street_len): annotation.remove()

osmnx.plot.plot_footprints(features, ax = ax, bbox = bbox, save = True, show = True, filepath = "mapA.png", dpi = dpi)

from PIL import Image

Image.open("MapA.png").save("MapA.bmp")
Himage = Image.open("MapA.bmp")

new_width = 800
new_height = 480

resized_img = Himage.resize((new_width, new_width))

left = (new_width - new_width) / 2
top = (new_width - new_height) / 2
right = (new_width + new_width) / 2
bottom = (new_width + new_height) / 2

resized_img = resized_img.crop((left, top, right, bottom))
resized_img.save("MapAC.bmp")
