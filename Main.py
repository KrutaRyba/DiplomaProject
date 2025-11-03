from MapComposer import MapComposer
from ToEPDFormat import ToEPDFormat
#from EPDDisplayer import EPDDisplayer
from Map import Map

show = True
center_point = [50.635678, 26.212011] #50.624903/26.258266
zoom_level = 10 # >= 9

composer = MapComposer()
toEPD = ToEPDFormat()
map = Map(center_point, zoom_level)
composer.compose(map)
toEPD.convert(map, show)
'''
displayer = EPDDisplayer()
displayer.init_epd()
displayer.display()
#displayer.sleep()
'''
exit()
command = ""
while(command != "exit"):
    command = input("Give input: ")
    match (command):
        case "exit":
            print("----- Exit -----")
        case "zoom m":
            try:
                zoom = int(input("Give zoom level: "))
                if (zoom > 19 or zoom < 6):
                    print("Zoom level must be between 6 and 19 (included)")
                    continue
                zoom_level = zoom
                map.zoom = zoom_level
                composer.compose(map)
                toEPD.convert(map, show)
                #displayer.display()
            except (ValueError):
                print("Input: numbers from 6 to 19 (included)")
        case "h":
            if (zoom_level < 19):
                zoom_level = zoom_level + 1
                map.zoom = zoom_level
                composer.compose(map)
                toEPD.convert(map, show)
                #displayer.display()
            else: print("Already at max zoom level")
        case "l":
            if (zoom_level > 6):
                zoom_level = zoom_level - 1
                map.zoom = zoom_level
                composer.compose(map)
                toEPD.convert(map, show)
                #displayer.display()
            else: print("Already at min zoom level")
        case "cp m":
            try:
                cp = input("Give center point: ").split("/")
                center_point = [float(cp[0]), float(cp[1])]
                map.center = center_point
                composer.compose(map)
                toEPD.convert(map, show)
                #displayer.display()
            except (ValueError):
                print("Input: numbers from X to Y (included)")
    

#displayer.sleep()