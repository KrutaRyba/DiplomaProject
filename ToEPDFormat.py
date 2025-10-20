from osmnx import plot

class ToEPDFormat:
    def convert(self, map, show):
        ax = None
        # Features
        if (map.features.grass.empty == False):
            _, ax = plot.plot_footprints(map.features.grass, ax = ax, color = "green", bgcolor = "white", show = False, close = False)
        if (map.features.sand.empty == False):
            _, ax = plot.plot_footprints(map.features.sand, ax = ax, color = "yellow", bgcolor = "white", show = False, close = False)
        if (map.features.water.empty == False):
            _, ax = plot.plot_footprints(map.features.water, ax = ax, color = "blue", bgcolor = "white", show = False, close = False)
        # Network
        if (len(map.network.railway.graph) != 0):
            _, ax = plot.plot_graph(map.network.railway, ax = ax, edge_color = "black", bgcolor = "white", edge_linewidth = map.railway_width, node_size = 0, show = False, close = False)
        if (len(map.network.highway.graph) != 0):
            _, ax = plot.plot_figure_ground(map.network.highway, ax = ax, color = "red", bgcolor = "white", street_widths = map.street_widths, default_width = 1, node_size = 0, show = False, close = False)
        # Buildings
        if (map.features.buildings.empty == False):
            _, ax = plot.plot_footprints(map.features.buildings, ax = ax, color = "orange", bgcolor = "white", bbox = map.bbox, show = show, save = not show, filepath = "Map.png")