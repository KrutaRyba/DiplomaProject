from Utils import Utils
from osmnx import plot, graph_to_gdfs
from matplotlib.patheffects import withStroke
from shapely import line_merge, MultiLineString
from numpy import rad2deg, atan2
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

class Street:
    def __init__(self, name):
        self.name = name
        self.sub_streets = []

class ToEPDFormat:
    def convert(self, map, show):
        ax = plt.gca()
        # Features
        if (not map.features.grass.empty):
            _, ax = plot.plot_footprints(map.features.grass, ax = ax, color = "#00ff00", show = False, close = False)
        if (not map.features.sand.empty):
            _, ax = plot.plot_footprints(map.features.sand, ax = ax, color = "#ffff00", show = False, close = False)
        if (not map.features.water.empty):
            _, ax = plot.plot_footprints(map.features.water, ax = ax, color = "#0000ff", show = False, close = False)
        if (not map.features.buildings.empty):
            _, ax = plot.plot_footprints(map.features.buildings, ax = ax, color = "#ff8000", show = False, close = False)
        # Network
        if (len(map.network.railway.graph) != 0):
            _, ax = plot.plot_graph(map.network.railway, ax = ax, edge_color = "#000000", edge_linewidth = map.railway_width, node_size = 0, show = False, close = False)
        if (len(map.network.highway.graph) != 0):
            _, ax = plot.plot_figure_ground(map.network.highway, ax = ax, color = "#ff0000", street_widths = map.street_widths, default_width = 1, node_size = 0, show = False, close = False)
        # Administrative levels
        if (not map.administrative_levels.empty):
            admin_levels = map.administrative_levels[map.administrative_levels.geometry.type.isin(["Polygon", "MultiPolygon"]) & map.administrative_levels["place"].isin(["state", "country"])]
            if (not admin_levels.empty):
                _, ax = plot.plot_footprints(admin_levels, ax = ax, color = "none", edge_color = "#000000", edge_linewidth = 1, show = False, close = False)
        
        ax.set_axis_off()
        ax.set_xlim(map.bbox[0], map.bbox[2])
        ax.set_ylim(map.bbox[1], map.bbox[3])
        ax.set_facecolor("#ffffff")
        fig = plt.gcf()
        fig.set_size_inches(8, 8)
        tightbox = fig.get_tightbbox(fig.canvas.get_renderer())
        self.__annotate(ax, map)
        plt.savefig("Map.png", bbox_inches = tightbox, pad_inches = 0, dpi = 150)
        if (show): plt.show()
        plt.close(fig)

    def __annotate(self, ax, map):
        match (map.zoom):
            case 18 | 19:
                if (not map.features.buildings.empty): self.__annotate_buildings(ax, map.features.buildings)
                if (len(map.network.highway) != 0):
                   streets = graph_to_gdfs(map.network.highway, nodes = False, fill_edge_geometry = True).fillna('')
                   self.__annotate_streets(ax, streets)
                # amenities
            case 16 | 17:
                if (not map.features.buildings.empty):
                    buildings = Utils.filter_features_by_area(map.features.buildings, map.dist * 2)
                    self.__annotate_buildings(ax, buildings)
                if (len(map.network.highway) != 0):
                    streets = graph_to_gdfs(map.network.highway, nodes = False, fill_edge_geometry = True).fillna('')
                    self.__annotate_streets(ax, streets)
            case 14 | 15:
                if (len(map.network.highway) != 0):
                    streets = graph_to_gdfs(map.network.highway, nodes = False, fill_edge_geometry = True).fillna('')
                    streets = streets[streets["highway"].isin(["motorway", "trunk", "primary", "secondary", "tertiary"])]
                    self.__annotate_streets(ax, streets)
                if (not map.administrative_levels.empty):
                    admin_levels = map.administrative_levels[map.administrative_levels.geometry.type.isin(["Point"])]
                    self.__annotate_administrative_levels(ax, admin_levels)
            case 12 | 13:
                if (len(map.network.highway) != 0):
                    streets = graph_to_gdfs(map.network.highway, nodes = False, fill_edge_geometry = True).fillna('')
                    streets = streets[streets["highway"].isin(["motorway", "trunk", "primary"])]
                    self.__annotate_streets(ax, streets)
                if (not map.administrative_levels.empty):
                    admin_levels = map.administrative_levels[map.administrative_levels.geometry.type.isin(["Point"])]
                    self.__annotate_administrative_levels(ax, admin_levels)
            case 10 | 11:
                if (len(map.network.highway) != 0):
                    streets = graph_to_gdfs(map.network.highway, nodes = False, fill_edge_geometry = True).fillna('')
                    streets = streets[streets["highway"].isin(["motorway"])]
                    self.__annotate_streets(ax, streets)
                if (not map.administrative_levels.empty):
                    admin_levels = map.administrative_levels[map.administrative_levels.geometry.type.isin(["Point"])]
                    self.__annotate_administrative_levels(ax, admin_levels)
            case 8 | 9:
                if (not map.administrative_levels.empty):
                    admin_levels = map.administrative_levels[map.administrative_levels.geometry.type.isin(["Point"])]
                    self.__annotate_administrative_levels(ax, admin_levels)
            case 6 | 7:
                if (not map.administrative_levels.empty):
                    admin_levels = map.administrative_levels[map.administrative_levels.geometry.type.isin(["Point"])]
                    self.__annotate_administrative_levels(ax, admin_levels)

    def __search_tail(self, node, linestrings, checked, line):
        adjacent_lines = []
        for linestring, check in zip(linestrings, checked):
            if (check): continue
            if (node.coords[0] == linestring.coords[-1] or node.coords[0] == linestring.coords[0] or node.coords[-1] == linestring.coords[0] or node.coords[-1] == linestring.coords[-1]):
                adjacent_lines.append(linestring)
        # check if intersection or one line per side
        if (len(adjacent_lines) == 2):
            # intersection
            if (adjacent_lines[0].coords[0] == adjacent_lines[1].coords[-1] or adjacent_lines[0].coords[0] == adjacent_lines[1].coords[0] or adjacent_lines[0].coords[-1] == adjacent_lines[1].coords[0] or adjacent_lines[0].coords[-1] == adjacent_lines[1].coords[-1]):
                return
        if (len(adjacent_lines) > 2 or len(adjacent_lines) == 0): return
        line.append(adjacent_lines[0])
        checked[linestrings.index(adjacent_lines[0])] = True
        self.__search_tail(adjacent_lines[0], linestrings, checked, line)

    def __annotate_streets(self, ax, streets):
        streets_dict = dict()
        for _, edge in streets.iterrows():
            try: text = edge["name"]
            except (KeyError): continue
            if (text == "" or type(text) is not str): continue
            if (text not in streets_dict.keys()):
                streets_dict[text] = []
                streets_dict[text].append(edge["geometry"])
            else:
                streets_dict[text].append(edge["geometry"])
        
        streets = []  
        for name, linestrings in streets_dict.items():
            street = Street(name)
            checked = [False] * len(linestrings)
            for linestring, check in zip(linestrings, checked):
                if (check): continue
                line = [linestring]
                checked[linestrings.index(linestring)] = True
                self.__search_tail(linestring, linestrings, checked, line)
                # in case first linestring is not borderline
                self.__search_tail(linestring, linestrings, checked, line)
                street.sub_streets.append(line_merge(MultiLineString(line)))
            streets.append(street)

        for street in streets:
            for sub_street in street.sub_streets:
                a = sub_street.coords[0]
                b = sub_street.coords[-1]
                delta = (a[1] - b[1], a[0] - b[0])
                angle = rad2deg(atan2(delta[0], delta[1]))
                if (angle > 90.0): angle = angle - 180
                elif (angle < -90): angle = angle + 180
                point = sub_street.centroid
                txt = ax.annotate(street.name, (point.x, point.y),
                                  horizontalalignment = "center", verticalalignment = "center",
                                  transform_rotates_text = True, rotation_mode = "anchor", rotation = angle,
                                  color = "#000000", fontsize = "x-small")
                txt.set_path_effects([withStroke(linewidth = 2, foreground = "#ffffff")])
    
    def __annotate_buildings(self, ax, buildings):
        for _, build in buildings.iterrows():
            point = build["geometry"].centroid
            try:
                text = build["name"]
                if (type(text) is not str): text = build["addr:housenumber"]
            except (KeyError):
                text = build["addr:housenumber"]
            if (type(text) is not str): continue
            txt = ax.annotate(text, (point.x, point.y), color = "#000000", horizontalalignment = "center", verticalalignment = "center", fontsize = "x-small")
            txt.set_path_effects([withStroke(linewidth = 2, foreground = "#ffffff")])

    def __annotate_administrative_levels(self, ax, admin_levels):
        for _, level in admin_levels.iterrows():
            point = level["geometry"].centroid
            try: text = level["name"]
            except (KeyError): continue
            if (type(text) is not str): continue
            fontsize = "small"
            match (level["place"]):
                case "country": fontsize = "x-large"
                case "state": fontsize = "large"
                case "city": fontsize = "medium"
                case "town": fontsize = "small"
                case "village": fontsize = "small"
                case "suburb": fontsize = "x-small"
            txt = ax.annotate(text, (point.x, point.y), color = "#000000", horizontalalignment = "center", verticalalignment = "center", weight = "bold", fontsize = fontsize)
            txt.set_path_effects([withStroke(linewidth = 2, foreground = "#ffffff")])

    def __annotate_amenities(self, ax, amenities):
        for _, build in amenities.iterrows():
            point = build["geometry"].centroid
            try: text = build["name"]
            except (KeyError): continue
            if (type(text) is not str): continue
            ax.annotate(text, (point.x, point.y), color = "#000000", horizontalalignment = "center", verticalalignment = "center")