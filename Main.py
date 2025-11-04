from MapComposer import MapComposer
from ToEPDFormat import ToEPDFormat
from EPDDisplayer import EPDDisplayer
from EPDDisplay import PhysicalEPD, EmulatedEPD
from Map import Map
from Utils import Utils

show = False
center_point = [50.635678, 26.212011]
zoom_level = 16 # >= 9

#EPD = PhysicalEPD()
EPD = EmulatedEPD()
displayer = EPDDisplayer(EPD)
displayer.init_epd()
composer = MapComposer()
toEPD = ToEPDFormat()
map = Map(center_point, zoom_level)
composer.compose(map)
toEPD.convert(map, show)
displayer.display()
#displayer.sleep()
#exit()

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
                map.zoom = zoom_level
                composer.compose(map)
                toEPD.convert(map, show)
                displayer.display()
            except (ValueError):
                print("Input: numbers from 6 to 19 (included)")
        case "h":
            if (zoom_level < 19):
                zoom_level = zoom_level + 1
                map.zoom = zoom_level
                composer.compose(map)
                toEPD.convert(map, show)
                displayer.display()
            else: print("Already at max zoom level")
        case "l":
            if (zoom_level > 6):
                zoom_level = zoom_level - 1
                map.zoom = zoom_level
                composer.compose(map)
                toEPD.convert(map, show)
                displayer.display()
            else: print("Already at min zoom level")
        case "cp m":
            try:
                cp = input("Give center point [lon/lat]: ").split("/")
                center_point = [float(cp[0]), float(cp[1])]
                map.center = center_point
                composer.compose(map)
                toEPD.convert(map, show)
                displayer.display()
            except (ValueError):
                print("Input: numbers from X to Y (included)")
        case "w":
            center_point = Utils.add_meters_to_point_lon(center_point, map.dist)
            map.center = center_point
            composer.compose(map)
            toEPD.convert(map, show)
            displayer.display()
        case "s":
            center_point = Utils.add_meters_to_point_lon(center_point, -map.dist)
            map.center = center_point
            composer.compose(map)
            toEPD.convert(map, show)
            displayer.display()
        case "a":
            center_point = Utils.add_meters_to_point_lat(center_point, -map.dist)
            map.center = center_point
            composer.compose(map)
            toEPD.convert(map, show)
            displayer.display()
        case "d":
            center_point = Utils.add_meters_to_point_lat(center_point, map.dist)
            map.center = center_point
            composer.compose(map)
            toEPD.convert(map, show)
            displayer.display()