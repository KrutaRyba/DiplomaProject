from json import load
from typing import Self
from APIConnector import APIConnector
from LinearFolderManager import LinearFolderManager
from networkx import MultiDiGraph
from osmnx import features, graph, _overpass
from re import findall
from subprocess import check_call
from Utils import Definitions, Utils
from geopandas import GeoDataFrame
from random import choices
from string import ascii_letters, digits
class LocalConnector(APIConnector):

    def __init__(self) -> None:
        self.__osm_file: str
        with open("ServerConfig.json") as file:
            self.__osm_file = load(file)["osm_file"]
        if (self.__osm_file == None): raise RuntimeError("Configure ServerConfig.json")
        folder = ''.join(choices(ascii_letters + digits, k = 16))
        self.__f_manager: LinearFolderManager = LinearFolderManager(Utils.find_file(Definitions.OSM_FOLDER))
        self.__f_manager.create_folder(folder, 0)
        self.__cached_bbox: str | None = None

    def get_features(self, bbox: tuple[float, float, float, float], tags: dict[str, bool | str | list[str]]) -> GeoDataFrame:
        feature = GeoDataFrame()
        master_file = self.__f_manager.get_path("out.osm.pbf", 1)
        out_file = self.__f_manager.get_path("out.osm", 1)
        bbox_str = ",".join([("{0:0.6f}").format(x) for x in bbox])
        try:
            self.__extract(bbox_str, master_file)
            self.Osmium().tags_filter().overwrite().remove_tags() \
                .output(out_file).osm_file(master_file).filter_expression(self.__tags_to_args(tags)) \
                .execute()
            feature = features.features_from_xml(out_file)
        except Exception as e:
            print("  Not found")
            print(e)
        return feature
    
    def get_network(self, bbox: tuple[float, float, float, float], network_type: str | None, custom_filter: str | None) -> MultiDiGraph:
        network = MultiDiGraph()
        type = "all" if (network_type == None) else network_type
        master_file = self.__f_manager.get_path("out.osm.pbf", 1)
        out_file = self.__f_manager.get_path("out.osm", 1)
        bbox_str = ",".join([("{0:0.6f}").format(x) for x in bbox])
        try:
            self.__extract(bbox_str, master_file)
            tags = self.__filter_to_args(_overpass._get_network_filter(type)) if (custom_filter == None) \
                else self.__filter_to_args(custom_filter)
            self.__filter(tags, master_file, out_file)
            network = graph.graph_from_xml(out_file, retain_all = True)
        except Exception as e:
            print("  Not found")
            print(e)
        return network
    
    def __extract(self, bbox_str: str, out_file: str) -> None:
        if (self.__cached_bbox == None or self.__cached_bbox != bbox_str):
            self.Osmium().extract().bbox(bbox_str).overwrite().output(out_file).osm_file(self.__osm_file).execute()
            self.__cached_bbox = bbox_str

    def __filter(self, tags: list[str], master_file: str, out_file: str) -> None:
        counter = 0
        self.__f_manager.create_folder("osm_filter", 1)
        for tag in tags:
            tmp_file = self.__f_manager.get_path(f"{counter}.osm.pbf", 2)
            counter += 1
            if ("=" in tag):
                # Key-Value
                if ("!=" in tag):
                    sub_tags = tag.split("!=")
                    self.Osmium().tags_filter().invert_match().overwrite().remove_tags().output(tmp_file).osm_file(master_file) \
                        .filter_expression("w/" + sub_tags[0]).execute()
                    tmp_file = self.__f_manager.get_path(f"{counter}.osm.pbf", 2)
                    self.Osmium().tags_filter().overwrite().remove_tags().output(tmp_file).osm_file(master_file) \
                        .filter_expression("w/" + tag).execute()
                    counter += 1
                    tmp_file = self.__f_manager.get_path(f"{counter}.osm.pbf", 2)
                    self.Osmium().merge().overwrite().output(tmp_file) \
                        .options([self.__f_manager.get_path(f"{counter - 2}.osm.pbf", 2), self.__f_manager.get_path(f"{counter - 1}.osm.pbf", 2)]) \
                        .execute()
                    counter += 1
                else:
                    self.Osmium().tags_filter().overwrite().remove_tags().output(tmp_file).osm_file(master_file) \
                        .filter_expression("w/" + tag).execute()
            else:
                # Key
                command = self.Osmium().tags_filter().overwrite().remove_tags().output(tmp_file).filter_expression("w/" + tag).osm_file(master_file)
                if ("!" in tag): command.invert_match()
                command.execute()
            master_file = tmp_file
        self.Osmium().cat().overwrite().output(out_file).osm_file(master_file).execute()

    def __tags_to_args(self, tags: dict[str, bool|str|list[str]]) -> list[str]:
        elements = list()
        for key, value in tags.items():
            string = f"{key}="
            if (type(value) is list): string += ",".join([x for x in value])
            elif (type(value) is str): string += value
            else: string = key if (value) else "!" + key
            elements.append(string)
        return elements

    def __filter_to_args(self, filter: str) -> list[str]:
        elements = [x.replace("\"", "").replace("'", "").replace("~", "=").replace("|", ",") for x in findall(r"[^\[\]]+", filter)]
        return elements
    
    class Osmium:
        def __init__(self) -> None:
            self.__command: str | None = None
            self.__options: list[str] = []
            self.__osm_file: str | None = None
            self.__filter: list[str] = []

        def cat(self) -> Self:
            self.__command = "cat"
            return self

        def extract(self) -> Self:
            self.__command = "extract"
            return self

        def merge(self) -> Self:
            self.__command = "merge"
            return self
        
        def tags_filter(self) -> Self:
            self.__command = "tags-filter"
            return self
        
        def bbox(self, bbox: str) -> Self:
            self.__options.append("--bbox")
            self.__options.append(bbox)
            return self

        def filter_expression(self, filter: list[str] | str) -> Self:
            if (type(filter) == str): self.__filter.append(filter)
            else: self.__filter += filter
            return self

        def invert_match(self) -> Self:
            self.__options.append("--invert-match")
            return self

        def omit_referenced(self) -> Self:
            self.__options.append("--omit-referenced")
            return self

        def options(self, options: list[str]) -> Self:
            self.__options += options
            return self

        def output(self, output: str) -> Self:
            self.__options.append("--output")
            self.__options.append(output)
            return self

        def overwrite(self) -> Self:
            self.__options.append("--overwrite")
            return self
        
        def osm_file(self, file: str) -> Self:
            self.__osm_file = file
            return self
        
        def remove_tags(self) -> Self:
            self.__options.append("--remove-tags")
            return self

        def execute(self) -> None:
            args = ["osmium", self.__command] \
                + (self.__options if (len(self.__options) != 0) else []) \
                + ([self.__osm_file] if (self.__osm_file != None) else []) \
                + (self.__filter if (len(self.__filter) != 0) else [])
            print(args)
            check_call(args)
