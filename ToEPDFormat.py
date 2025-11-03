
from Utils import Utils
from osmnx import plot, graph_to_gdfs
import matplotlib.pyplot as plt
import numpy

class ToEPDFormat:
    def convert(self, map, show):     
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

        ax.set_xlim(map.bbox[0], map.bbox[2])
        ax.set_ylim(map.bbox[1], map.bbox[3])
        ax.set_facecolor("#ffffff")
        fig = plt.gcf()
        tightbox = fig.get_tightbbox(fig.canvas.get_renderer())
        self.__annotate(ax, map)
        plt.savefig("Map.png", bbox_inches = tightbox, pad_inches = 0, dpi = 150)
        if (show): plt.show()
        plt.close(fig)

    def __annotate(self, ax, map):
        match (map.zoom):
            case 18 | 19:
                if (len(map.network.highway) != 0):
                   streets = graph_to_gdfs(map.network.highway, nodes = False, fill_edge_geometry = True).fillna('')
                   self.__annotate_streets(ax, streets)
                if (not map.features.buildings.empty): self.__annotate_buildings(ax, map.features.buildings)
                # amenities
            case 16 | 17:
                if (len(map.network.highway) != 0):
                    streets = graph_to_gdfs(map.network.highway, nodes = False, fill_edge_geometry = True).fillna('')
                    self.__annotate_streets(ax, streets)
                if (not map.features.buildings.empty):
                    buildings = Utils.filter_features_by_area(map.features.buildings, map.dist * 2)
                    self.__annotate_buildings(ax, buildings)
            case 14 | 15:
                if (len(map.network.highway) != 0):
                    streets = graph_to_gdfs(map.network.highway, nodes = False, fill_edge_geometry = True).fillna('')
                    streets = streets[streets["highway"].isin(["motorway", "trunk", "primary", "secondary", "tertiary"])]
                    self.__annotate_streets(ax, streets)
                if (not map.administrative_levels.empty):
                    admin_levels =  map.administrative_levels[map.administrative_levels.geometry.type.isin(["Point"])]
                    self.__annotate_administrative_levels(ax, admin_levels)
            case 12 | 13:
                if (len(map.network.highway) != 0):
                    streets = graph_to_gdfs(map.network.highway, nodes = False, fill_edge_geometry = True).fillna('')
                    streets = streets[streets["highway"].isin(["motorway", "trunk", "primary"])]
                    self.__annotate_streets(ax, streets)
                if (not map.administrative_levels.empty):
                    admin_levels =  map.administrative_levels[map.administrative_levels.geometry.type.isin(["Point"])]
                    self.__annotate_administrative_levels(ax, admin_levels)
            case 10 | 11:
                if (len(map.network.highway) != 0):
                    streets = graph_to_gdfs(map.network.highway, nodes = False, fill_edge_geometry = True).fillna('')
                    streets = streets[streets["highway"].isin(["motorway"])]
                    self.__annotate_streets(ax, streets)
                if (not map.administrative_levels.empty):
                    admin_levels =  map.administrative_levels[map.administrative_levels.geometry.type.isin(["Point"])]
                    self.__annotate_administrative_levels(ax, admin_levels)
            case 8 | 9:
                if (not map.administrative_levels.empty):
                    admin_levels =  map.administrative_levels[map.administrative_levels.geometry.type.isin(["Point"])]
                    self.__annotate_administrative_levels(ax, admin_levels)
                pass
            case 6 | 7:
                # state cities and country
                pass

    def __annotate_streets(self, ax, streets):
        streets_dict = dict()
        for _, edge in streets.iterrows():
            try: text = edge["name"]
            except (KeyError): continue
            if (type(text) is not str): continue
            if (text not in streets_dict.keys()):
                streets_dict[text] = []
            else:
                streets_dict[text].append(edge["geometry"])

        import shapely as sh
        for name, linestrings in streets_dict.items():
            streets_dict[name] = [sh.line_merge(linestrings)]

        for name, linestring in streets_dict.items():
            a = linestring[0][0].coords[0]
            b = linestring[0][0].coords[1]
            delta = (a[1] - b[1], a[0] - b[0])
            angle = numpy.rad2deg(numpy.atan2(delta[0], delta[1]))
            if (angle > 90.0): angle = angle - 180
            elif (angle < -90): angle = angle + 180
            ax.annotate(name, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2),
                        horizontalalignment = "center", verticalalignment= "center",
                        transform_rotates_text = True, rotation_mode = "anchor", rotation = angle,
                        color = "#000000", fontsize= "small")

        '''
        for _, edge in streets.iterrows():
            text = edge["name"]
            if (text == "" or type(text) is not str): continue
            a = edge["geometry"].coords[0]
            b = edge["geometry"].coords[1]
            delta = (a[1] - b[1], a[0] - b[0])
            angle = numpy.rad2deg(numpy.atan2(delta[0], delta[1]))
            if (angle > 90.0): angle = angle - 180
            elif (angle < -90): angle = angle + 180
            annotation = ax.annotate(text, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2),
                                     horizontalalignment = "center", verticalalignment= "center",
                                     transform_rotates_text = True, rotation_mode = "anchor", rotation = angle,
                                     color = "#000000", weight = "bold", fontsize= "small")
            bbox_a = ax.transData.inverted().transform_bbox(annotation.get_window_extent())
            s = edge["geometry"].coords[0]
            e = edge["geometry"].coords[-1]
            street_len = numpy.sqrt(numpy.power(s[0] - e[0], 2) + numpy.power(s[1] - e[1], 2))
            label_len = numpy.sqrt(numpy.power(bbox_a.x0 - bbox_a.x1, 2) + numpy.power(bbox_a.y0 - bbox_a.y1, 2))
            if (label_len > street_len * 3000):
                annotation.remove()
        '''
    
    def __annotate_buildings(self, ax, buildings):
        for _, build in buildings.iterrows():
            point = build["geometry"].centroid
            try:
                text = build["name"]
                if (type(text) is not str): text = build["addr:housenumber"]
            except (KeyError):
                text = build["addr:housenumber"]
            if (type(text) is not str): continue
            ax.annotate(text, (point.x, point.y), color = "#000000", horizontalalignment = "center", verticalalignment= "center")

    def __annotate_administrative_levels(self, ax, admin_levels):
        for _, level in admin_levels.iterrows():
            point = level["geometry"].centroid
            try: text = level["name"]
            except (KeyError): continue
            if (type(text) is not str): continue
            ax.annotate(text, (point.x, point.y), color = "#000000", horizontalalignment = "center", verticalalignment= "center", weight = "bold", fontsize = "medium")

    def __annotate_amenities(self, ax, amenities):
        for _, build in amenities.iterrows():
            point = build["geometry"].centroid
            try: text = build["name"]
            except (KeyError): continue
            if (type(text) is not str): continue
            ax.annotate(text, (point.x, point.y), color = "#000000", horizontalalignment = "center", verticalalignment= "center")