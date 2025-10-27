from osmnx import plot, graph_to_gdfs
import matplotlib.pyplot as plt

class ToEPDFormat:
    def convert(self, map, show):
        should_show = [not show] * 6
        if (not map.features.grass.empty): should_show[0] = show
        if(not map.features.sand.empty):
            should_show = [not show] * 6
            should_show[1] = show
        if (not map.features.sand.empty):
            should_show = [not show] * 6
            should_show[2] = show
        if (len(map.network.railway.graph) != 0):
            should_show = [not show] * 6
            should_show[3] = show
        if (len(map.network.highway.graph) != 0):
            should_show = [not show] * 6
            should_show[4] = show
        if (not map.features.buildings.empty):
            should_show = [not show] * 6
            should_show[5] = show      

        ax = None
        # Features
        if (not map.features.grass.empty):
            _, ax = plot.plot_footprints(map.features.grass, ax = ax, color = "#00ff00", show = False, close = False)
        if (not map.features.sand.empty):
            _, ax = plot.plot_footprints(map.features.sand, ax = ax, color = "#ffff00", show = False, close = False)
        if (not map.features.water.empty):
            _, ax = plot.plot_footprints(map.features.water, ax = ax, color = "#0000ff", show = False, close = False)
        # Network
        if (len(map.network.railway.graph) != 0):
            _, ax = plot.plot_graph(map.network.railway, ax = ax, edge_color = "#000000", edge_linewidth = map.railway_width, node_size = 0, show = False, close = False)
        if (len(map.network.highway.graph) != 0):
            _, ax = plot.plot_figure_ground(map.network.highway, ax = ax, color = "#ff0000", street_widths = map.street_widths, default_width = 1, node_size = 0, show = False, close = False)
        # Buildings
        if (not map.features.buildings.empty):
            _, ax = plot.plot_footprints(map.features.buildings, ax = ax, color = "#ff8000", show = False, close = False)
        
        '''
        streets = graph_to_gdfs(map.network.highway, nodes = False, fill_edge_geometry = True).fillna('')
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
            if (label_len > street_len * 3000):
                annotation.remove()
        '''

        ax.set_xlim(map.bbox[0], map.bbox[2])
        ax.set_ylim(map.bbox[1], map.bbox[3])
        ax.set_facecolor("#ffffff")
        plt.savefig("Map.png", bbox_inches = "tight", pad_inches = 0)
        if (show): plt.show()
        plt.close()