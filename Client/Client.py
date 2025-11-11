from requests import get
from PIL import Image
from io import BytesIO
from EPDDisplayer import EPDDisplayer
from EPDDisplay import PhysicalEPD, EmulatedEPD
from Utils import Utils
from json import load

center_point = [50.635678, 26.212011]
zoom_level = 16

#EPD = PhysicalEPD()
EPD = EmulatedEPD()
displayer = EPDDisplayer(EPD)
displayer.init_epd()

SERVER_IP = None
SERVER_PORT = None
with open("ClientConfig.json") as file:
    loaded = load(file)
    SERVER_IP = loaded["server_ip"]
    SERVER_PORT = loaded["server_port"]
if (SERVER_IP == None or SERVER_PORT == None): raise RuntimeError("Specify server ip and/or server port")
URL = f"http://{SERVER_IP}:{SERVER_PORT}/map/"

def handle_request(center_point, zoom_level):
    response = get(f"{URL}/{('{0:0.6f}').format(center_point[0])}/{('{0:0.6f}').format(center_point[1])}/{zoom_level}")
    image = None
    if (response.status_code == 500): image = Image.open("Error.png")
    else: image = Image.open(BytesIO(response.content))
    image.save("Map.png")
    displayer.display()

handle_request(center_point, zoom_level)

command = ""
while(command != "exit"):
    print(f"\nCurrent zoom: {zoom_level}, center point: {center_point}\n")
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
                print("Input: numbers from 6 to 19 (included)")
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
                cp = input("Give center point [lon/lat]: ").split("/")
                center_point = [float(cp[0]), float(cp[1])]
                handle_request(center_point, zoom_level)
            except (ValueError):
                print("Input: numbers from X to Y (included)")
        case "w":
            center_point = Utils.add_meters_to_point_lon(center_point, Utils.calculate_distance(center_point, zoom_level))
            handle_request(center_point, zoom_level)
        case "s":
            center_point = Utils.add_meters_to_point_lon(center_point, -Utils.calculate_distance(center_point, zoom_level))
            handle_request(center_point, zoom_level)
        case "a":
            center_point = Utils.add_meters_to_point_lat(center_point, -Utils.calculate_distance(center_point, zoom_level))
            handle_request(center_point, zoom_level)
        case "d":
            center_point = Utils.add_meters_to_point_lat(center_point, Utils.calculate_distance(center_point, zoom_level))
            handle_request(center_point, zoom_level)