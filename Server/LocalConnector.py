from osmnx import features, graph, _overpass
from pandas import DataFrame
from networkx import MultiDiGraph
from subprocess import check_call
from re import findall
from LinearFolderManager import LinearFolderManager
from json import load

class LocalConnector:

    def __init__(self):
        self.__osm_file = None
        with open("ServerConfig.json") as file:
            self.__osm_file = load(file)["osm_file"]
        if (self.__osm_file == None): raise RuntimeError("Specify an OSM file")
        self.__f_manager = LinearFolderManager(".osm_tmp")
        self.__cached_bbox = None

    def __del__(self):
        self.__f_manager.cleanup()

    def get_features(self, bbox, tags):
        feature = DataFrame()
        master_file = self.__f_manager.get_path("out.osm.pbf", 0)
        out_file = self.__f_manager.get_path("out.osm", 0)
        bbox_str = ",".join([("{0:0.6f}").format(x) for x in bbox])
        try:
            self.__extract(bbox_str, master_file)
            if (tags != None):
                args = ["osmium", "tags-filter", "--overwrite", "-o", out_file, master_file] + self.__tags_to_args(tags)
            else:
                args = ["osmium", "cat", "--overwrite", "-o", out_file, master_file]
            print(args)
            check_call(args)
            feature = features.features_from_xml(out_file)
        except Exception as e:
            print("  Not found")
            print(e)
        return feature
    
    def get_network(self, bbox, network_type = "all", custom_filter = None):
        network = MultiDiGraph()
        master_file = self.__f_manager.get_path("out.osm.pbf", 0)
        out_file = self.__f_manager.get_path("out.osm", 0)
        bbox_str = ",".join([("{0:0.6f}").format(x) for x in bbox])
        try:
            self.__extract(bbox_str, master_file)
            tags = self.__filter_to_args(_overpass._get_network_filter(network_type)) if (custom_filter == None) \
                else self.__filter_to_args(custom_filter)
            self.__filter(tags, master_file, out_file)
            network = graph.graph_from_xml(out_file, retain_all = True)
        except Exception as e:
            print("  Not found")
            print(e)
        return network
    
    def __extract(self, bbox_str, out_file):
        if (self.__cached_bbox == None or self.__cached_bbox != bbox_str):
            args = ["osmium", "extract", "--bbox", bbox_str, "--overwrite", "-o", out_file, self.__osm_file]
            print(args)
            check_call(args)
            self.__cached_bbox = bbox_str

    def __filter(self, tags, master_file, out_file):
        args = []
        counter = 0
        self.__f_manager.create_folder("osm_filter", 0)
        for tag in tags:
            tmp_file = self.__f_manager.get_path(f"{counter}.osm.pbf", 1)
            counter += 1
            if ("=" in tag):
                # Key-Value
                if ("!=" in tag):
                    # ?
                    sub_tags = tag.split("!=")
                    args = ["osmium", "tags-filter", "-i", "--overwrite", "-o", tmp_file, master_file, "w/" + sub_tags[0]]
                    print(args)
                    check_call(args)
                    tmp_file = self.__f_manager.get_path(f"{counter}.osm.pbf", 1)
                    args = ["osmium", "tags-filter", "--overwrite", "-o", tmp_file, master_file, "w/" + tag]
                    print(args)
                    check_call(args)
                    counter += 1
                    tmp_file = self.__f_manager.get_path(f"{counter}.osm.pbf", 1)
                    args = ["osmium", "merge", "--overwrite", "-o", tmp_file, self.__f_manager.get_path(f"{counter - 2}.osm.pbf", 1), \
                            self.__f_manager.get_path(f"{counter - 1}.osm.pbf", 1)]
                    counter += 1
                else:
                    args = ["osmium", "tags-filter", "--overwrite", "-o", tmp_file, master_file, "w/" + tag]
            else:
                # Key
                if ("!=" in tag):
                    args = ["osmium", "tags-filter", "-i", "--overwrite", "-o", tmp_file, master_file, "w/" + tag]
                else:
                    args = ["osmium", "tags-filter", "--overwrite", "-o", tmp_file, master_file, "w/" + tag]
            print(args)
            check_call(args)
            master_file = tmp_file
        args = ["osmium", "cat", "--overwrite", "-o", out_file, master_file]
        print(args)
        check_call(args)

    def __tags_to_args(self, tags: dict[str, bool|str|list[str]]) -> list[str]:
        elements = list()
        for key, value in tags.items():
            string = f"{key}="
            if (type(value) is list):
                string += ",".join([x for x in value])
            elif (type(value) is str):
                string += value
            else:
                string += "yes" if (value) else "no"
            elements.append(string)
            if (key == "building"):
                elements.append("addr:housenumber")
                elements.append("addr:street")
        return elements

    def __filter_to_args(self, filter: str) -> list[str]:
        elements = [x.replace("\"", "").replace("'", "").replace("~", "=").replace("|", ",") for x in findall(r"[^\[\]]+", filter)]
        return elements