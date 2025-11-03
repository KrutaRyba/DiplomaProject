from osmnx import features, graph, _overpass
from pandas import DataFrame
from networkx import MultiDiGraph
from subprocess import check_call
from re import findall
import os

class LocalConnector:

    def __init__(self, osm_file):
        self.osm_file = osm_file
        self._cached_bbox = None

    def get_features(self, bbox, tags):
        feature = DataFrame()
        out_file = "out.osm.pbf"
        true_out_file = "out.osm"
        bbox_str = ",".join([("{0:0.6f}").format(x) for x in bbox])
        try:
            self.__extract(bbox_str, out_file)
            if (tags != None):
                args = ["osmium", "tags-filter", "--overwrite", "-o", true_out_file, out_file] + self.__tags_to_args(tags)
                print(args)
                check_call(args)
            else:
                args = ["osmium", "cat", "--overwrite", "-o", true_out_file, out_file]
                check_call(args)
            feature = features.features_from_xml(true_out_file)
        except Exception as e:
            print("  Not found")
            print(e)
        return feature
    
    def get_network(self, bbox, network_type = "all", custom_filter = None):
        network = MultiDiGraph()
        out_file = "out.osm.pbf"
        true_out_file = "out.osm"
        bbox_str = ",".join([("{0:0.6f}").format(x) for x in bbox])
        try:
            self.__extract(bbox_str, out_file)
            tags = self.__filter_to_args(_overpass._get_network_filter(network_type)) if (custom_filter == None) \
                else self.__filter_to_args(custom_filter)

            self.__filter(tags, out_file, true_out_file)

            
            network = graph.graph_from_xml(true_out_file, retain_all = True)
        except Exception as e:
            print("  Not found")
            print(e)
        return network
    
    def __extract(self, bbox_str, out_file):
        if (self._cached_bbox == None or self._cached_bbox != bbox_str):
            args = ["osmium", "extract", "--bbox", bbox_str, "--overwrite", "-o", out_file, self.osm_file]
            check_call(args)
            self._cached_bbox = bbox_str

    def __filter(self, tags, master_file, out_file):
        args = []
        counter = 0
        folder = "tmp_osm"
        if (not os.path.exists(folder)): os.mkdir(folder)
        for tag in tags:
            tmp_file = os.path.join(folder, f"{counter}_tmp_out.osm.pbf")
            counter += 1
            if ("=" in tag):
                # Key-Value
                if ("!=" in tag):
                    # ?
                    sub_tags = tag.split("!=")
                    args = ["osmium", "tags-filter", "-i", "--overwrite", "-o", tmp_file, master_file, sub_tags[0]]
                    print(args)
                    check_call(args)
                    tmp_file = os.path.join(folder, f"{counter}_tmp_out.osm.pbf")
                    args = ["osmium", "tags-filter", "--overwrite", "-o", tmp_file, master_file, tag]
                    print(args)
                    check_call(args)
                    counter += 1
                    tmp_file = os.path.join(folder, f"{counter}_tmp_out.osm.pbf")
                    args = ["osmium", "merge", "--overwrite", "-o", tmp_file, os.path.join(folder, f"{counter - 2}_tmp_out.osm.pbf"), \
                            os.path.join(folder, f"{counter - 1}_tmp_out.osm.pbf")]
                    counter += 1
                else:
                    args = ["osmium", "tags-filter", "--overwrite", "-o", tmp_file, master_file, tag]
            else:
                # Key
                if ("!=" in tag):
                    args = ["osmium", "tags-filter", "-i", "--overwrite", "-o", tmp_file, master_file, tag]
                else:
                    args = ["osmium", "tags-filter", "--overwrite", "-o", tmp_file, master_file, tag]
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
        return elements

    def __filter_to_args(self, filter: str) -> list[str]:
        elements = [x.replace("\"", "").replace("~", "=").replace("|", ",") for x in findall(r"[^\[\]]+", filter)]
        return elements
    
    def __idk(self):
    #     filters["drive"] = (
    #     f'["highway"]["area"!~"yes"]{settings.default_access}'
    #     f'["highway"!~"abandoned|bridleway|bus_guideway|construction|corridor|'
    #     f"cycleway|elevator|escalator|footway|no|path|pedestrian|planned|platform|"
    #     f'proposed|raceway|razed|rest_area|service|services|steps|track"]'
    #     f'["motor_vehicle"!~"no"]["motorcar"!~"no"]'
    #     f'["service"!~"alley|driveway|emergency_access|parking|parking_aisle|private"]'
    # )

        return ('--keep="highway="', '--drop="( highway=abandoned or highway=bridleway or highway=foot or highway=path or highway=no ) and '
                  'motor_vehicle=no and motorcar=no and ( service=alley or service=driveway or service=parking )"'
                  )

    # # drive+service: allow ways tagged 'service' but filter out certain types
    # filters["drive_service"] = (
    #     f'["highway"]["area"!~"yes"]{settings.default_access}'
    #     f'["highway"!~"abandoned|bridleway|bus_guideway|construction|corridor|'
    #     f"cycleway|elevator|escalator|footway|no|path|pedestrian|planned|platform|"
    #     f'proposed|raceway|razed|rest_area|services|steps|track"]'
    #     f'["motor_vehicle"!~"no"]["motorcar"!~"no"]'
    #     f'["service"!~"emergency_access|parking|parking_aisle|private"]'
    # )
