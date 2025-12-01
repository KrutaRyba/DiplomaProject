from EPDDisplay import PhysicalEPD, EmulatedEPD
from EPDDisplayer import EPDDisplayer
from io import BytesIO
from json import load
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from PIL import Image
from Utils import Utils

import os
if (os.name == "posix"):
    def handler(signum, _):
        displayer.exit()
    from signal import signal, SIGTERM, SIGQUIT, SIGHUP
    signal(SIGTERM, handler)
    signal(SIGQUIT, handler)
    signal(SIGHUP, handler)

SERVER_IP = None
SERVER_PORT = None
is_emulated = None

with open("ClientConfig.json") as file:
    loaded = load(file)
    SERVER_IP = loaded["server_ip"]
    SERVER_PORT = loaded["server_port"]
    is_emulated = loaded["is_emulated"]

if (SERVER_IP == None or SERVER_PORT == None or is_emulated == None): raise RuntimeError("Configure ClientConfig.json")
URL = f"http://{SERVER_IP}:{SERVER_PORT}/map"

try:
    with urlopen(URL, timeout = 3) as response:
        resp = response.read()
except (HTTPError, URLError, TimeoutError):
    print("Connection refused or timeout. Make sure that ClientConfig.json is properly configured")
    exit()

center_point = [50.635678, 26.212011]
zoom_level = 16
EPD = EmulatedEPD() if (is_emulated) else PhysicalEPD()
displayer = EPDDisplayer(EPD)

try:
    def handle_request(center_point: list[float], zoom_level: int) -> None:
        response = None
        try:
            with urlopen(f"{URL}/{('{0:0.6f}').format(center_point[0])}/{('{0:0.6f}').format(center_point[1])}/{zoom_level}", timeout = 600) as r:
                response = r.read()
        except (HTTPError, URLError, TimeoutError):
            print("Connection refused or timeout. Make sure that ClientConfig.json is properly configured")
            displayer.sleep()
            exit()
        image = None
        if (response == None): image = Image.open("Error.png")
        else: image = Image.open(BytesIO(response))
        displayer.display(image)
    
    displayer.init_epd()
    handle_request(center_point, zoom_level)
    
    ua_bbox = [22.137059, 44.184598, 40.2275801, 52.3791473]
    command = ""
    while(command != "exit"):
        print(f"\nCurrent zoom: {zoom_level}, center point [lat, lon]: {center_point[0]}, {center_point[1]}\n")
        command = input("Give input: ")
        match (command):
            case "exit":
                print("----- Exit -----")
                displayer.sleep()
            case "zoom m":
                try:
                    zoom = int(input("Give zoom level [zoom]: "))
                    if (zoom > 19 or zoom < 6):
                        print("Zoom level must be between 6 and 19 (included)")
                        continue
                    zoom_level = zoom
                    handle_request(center_point, zoom_level)
                except (ValueError):
                    print("Input: number from 6 to 19 (included)")
            case "h":
                if (zoom_level < 19):
                    zoom_level = zoom_level + 1
                    handle_request(center_point, zoom_level)
                else: print("Already at max zoom level")
            case "l":
                if (zoom_level > 6):
                    zoom_level = zoom_level - 1
                    handle_request(center_point, zoom_level)
                else: print("Already at min zoom level")
            case "cp m":
                try:
                    cp = input("Give center point [lat/lon]: ").split("/")
                    cp_arr = [float(cp[0]), float(cp[1])]
                    if (cp_arr[0] > ua_bbox[3] or cp_arr[0] < ua_bbox[1] or cp_arr[1] > ua_bbox[2] or cp_arr[1] < ua_bbox[0]):
                        print(f"Center point must be between: latitude {ua_bbox[1]}:{ua_bbox[3]}, longitude {ua_bbox[0]}:{ua_bbox[2]}")
                        continue
                    center_point = cp_arr
                    handle_request(center_point, zoom_level)
                except (ValueError):
                    print("Input: number/number")
            case "w":
                cp = Utils.add_meters_to_point_lat(center_point, Utils.horizontal_distance(center_point[0], zoom_level))
                if (cp[0] < ua_bbox[3]):
                    center_point = cp
                    handle_request(center_point, zoom_level)
                else: print("Already at max latitude")
            case "s":
                cp = Utils.add_meters_to_point_lat(center_point, -Utils.horizontal_distance(center_point[0], zoom_level))
                if (cp[0] > ua_bbox[1]):
                    center_point = cp
                    handle_request(center_point, zoom_level)
                else: print("Already at min latitude")
            case "a":
                cp = Utils.add_meters_to_point_lon(center_point, -Utils.horizontal_distance(center_point[0], zoom_level))
                if (cp[1] > ua_bbox[0]):
                    center_point = cp
                    handle_request(center_point, zoom_level)
                else: print("Already at min longitude")
            case "d":
                cp = Utils.add_meters_to_point_lon(center_point, Utils.horizontal_distance(center_point[0], zoom_level))
                if (cp[1] < ua_bbox[2]):
                    center_point = cp
                    handle_request(center_point, zoom_level)
                else: print("Already at max longitude")
            case "help":
                print("----- Help -----")
                print("exit\tExit")
                print("zoom m\tSet zoom")
                print("h\tZoom in")
                print("l\tZoom out")
                print("cp m\tSet center point")
                print("w\tNorth")
                print("s\tSouth")
                print("a\tWest")
                print("d\tEast")
                print("----- Help -----")
            case _:
                print("Incorrect command. Print 'help' for help")
except KeyboardInterrupt:
    displayer.exit()