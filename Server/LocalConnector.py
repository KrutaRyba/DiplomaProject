from json import load
from LinearFolderManager import LinearFolderManager
from networkx import MultiDiGraph
from osmnx import features, graph, _overpass
from pandas import DataFrame
from re import findall
from subprocess import check_call
from Utils import Definitions, Utils
from geopandas import GeoDataFrame

class LocalConnector:

    def __init__(self):
        self.__osm_file = None
        with open("ServerConfig.json") as file:
            self.__osm_file = load(file)["osm_file"]
        if (self.__osm_file == None): raise RuntimeError("Specify an OSM file")
        self.__f_manager = LinearFolderManager(Utils.find_file(Definitions.OSM_FOLDER))
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
                self.Osmium().tags_filter().overwrite().remove_tags() \
                    .output(out_file).osm_file(master_file).filter_expression(self.__tags_to_args(tags)) \
                    .execute()
            else:
                self.Osmium().cat().overwrite().output(out_file).osm_file(master_file).execute()
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
            self.Osmium().extract().bbox(bbox_str).overwrite().output(out_file).osm_file(self.__osm_file).execute()
            self.__cached_bbox = bbox_str

    def __filter(self, tags, master_file, out_file):
        counter = 0
        self.__f_manager.create_folder("osm_filter", 0)
        for tag in tags:
            tmp_file = self.__f_manager.get_path(f"{counter}.osm.pbf", 1)
            counter += 1
            if ("=" in tag):
                # Key-Value
                if ("!=" in tag):
                    sub_tags = tag.split("!=")
                    self.Osmium().tags_filter().invert_match().overwrite().remove_tags().output(tmp_file).osm_file(master_file) \
                        .filter_expression("w/" + sub_tags[0]).execute()
                    tmp_file = self.__f_manager.get_path(f"{counter}.osm.pbf", 1)
                    self.Osmium().tags_filter().overwrite().remove_tags().output(tmp_file).osm_file(master_file) \
                        .filter_expression("w/" + tag).execute()
                    counter += 1
                    tmp_file = self.__f_manager.get_path(f"{counter}.osm.pbf", 1)
                    self.Osmium().merge().overwrite().output(tmp_file) \
                        .options([self.__f_manager.get_path(f"{counter - 2}.osm.pbf", 1), self.__f_manager.get_path(f"{counter - 1}.osm.pbf", 1)]) \
                        .execute()
                    counter += 1
                else:
                    self.Osmium().tags_filter().overwrite().remove_tags().output(tmp_file).osm_file(master_file) \
                        .filter_expression("w/" + tag).execute()
            else:
                # Key
                command = self.Osmium().tags_filter().overwrite().remove_tags().output(tmp_file).filter_expression("w/" + tag).osm_file(master_file)
                if ("!=" in tag): command.invert_match()
                command.execute()
            master_file = tmp_file
        self.Osmium().cat().overwrite().output(out_file).osm_file(master_file).execute()

    def __tags_to_args(self, tags: dict[str, bool|str|list[str]]) -> list[str]:
        elements = list()
        for key, value in tags.items():
            string = f"{key}="
            if (type(value) is list): string += ",".join([x for x in value])
            elif (type(value) is str): string += value
            else: string = key
            elements.append(string)
        return elements

    def __filter_to_args(self, filter: str) -> list[str]:
        elements = [x.replace("\"", "").replace("'", "").replace("~", "=").replace("|", ",") for x in findall(r"[^\[\]]+", filter)]
        return elements
    
    class Osmium:
        def __init__(self):
            self.__command = None
            self.__options = []
            self.__osm_file = None
            self.__filter = []

        def cat(self):
            self.__command = "cat"
            return self

        def extract(self):
            self.__command = "extract"
            return self

        def merge(self):
            self.__command = "merge"
            return self
        
        def tags_filter(self):
            self.__command = "tags-filter"
            return self
        
        def bbox(self, bbox):
            self.__options.append("--bbox")
            self.__options.append(bbox)
            return self

        def filter_expression(self, filter: list[str] | str):
            if (type(filter) == str): self.__filter.append(filter)
            else: self.__filter += filter
            return self

        def invert_match(self):
            self.__options.append("--invert-match")
            return self

        def omit_referenced(self):
            self.__options.append("--omit-referenced")
            return self

        def options(self, options: list[str]):
            self.__options += options
            return self

        def output(self, output):
            self.__options.append("--output")
            self.__options.append(output)
            return self

        def overwrite(self):
            self.__options.append("--overwrite")
            return self
        
        def osm_file(self, file):
            self.__osm_file = file
            return self
        
        def remove_tags(self):
            self.__options.append("--remove-tags")
            return self

        def execute(self):
            args = ["osmium", self.__command] \
                + (self.__options if (len(self.__options) != 0) else []) \
                + ([self.__osm_file] if (self.__osm_file != None) else []) \
                + (self.__filter if (len(self.__filter) != 0) else [])
            print(args)
            check_call(args)