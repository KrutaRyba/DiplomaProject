from EPDDisplay import PhysicalEPD, EmulatedEPD
from EPDDisplayer import EPDDisplayer
from io import BytesIO
from json import load
from PIL import Image
from requests import ConnectTimeout, get
from Utils import Utils

try:
    SERVER_IP = None
    SERVER_PORT = None
    is_emulated = None

    with open("ClientConfig.json") as file:
        loaded = load(file)
        SERVER_IP = loaded["server_ip"]
        SERVER_PORT = loaded["server_port"]
        is_emulated = loaded["is_emulated"]

    if (SERVER_IP == None or SERVER_PORT == None or is_emulated == None): raise RuntimeError("Specify server ip and/or server port")
    URL = f"http://{SERVER_IP}:{SERVER_PORT}/map/"

    center_point = [50.635678, 26.212011]
    zoom_level = 16

    EPD  = EmulatedEPD() if (is_emulated) else PhysicalEPD()
    displayer = EPDDisplayer(EPD)
    displayer.init_epd()

    def handle_request(center_point, zoom_level):
        response = None
        try:
            response = get(f"{URL}/{('{0:0.6f}').format(center_point[0])}/{('{0:0.6f}').format(center_point[1])}/{zoom_level}")
        except ConnectTimeout as e:
            print(e)
        image = None
        if (response == None or response.status_code == 500): image = Image.open("Error.png")
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
                center_point = Utils.add_meters_to_point_lon(center_point, Utils.horizontal_distance(center_point[0], zoom_level))
                handle_request(center_point, zoom_level)
            case "s":
                center_point = Utils.add_meters_to_point_lon(center_point, -Utils.horizontal_distance(center_point[0], zoom_level))
                handle_request(center_point, zoom_level)
            case "a":
                center_point = Utils.add_meters_to_point_lat(center_point, -Utils.horizontal_distance(center_point[0], zoom_level))
                handle_request(center_point, zoom_level)
            case "d":
                center_point = Utils.add_meters_to_point_lat(center_point, Utils.horizontal_distance(center_point[0], zoom_level))
                handle_request(center_point, zoom_level)
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
