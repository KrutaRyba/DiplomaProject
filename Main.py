from MapComposer import MapComposer
from ToEPDFormat import ToEPDFormat
#from EPDDisplayer import EPDDisplayer
from Map import Map

show = True
center_point = [50.635678, 26.212011]
zoom_level = 18 # >= 9

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

command = ""
while(command != "exit"):
    command = input("Give input: ")
    try:
        zoom_level = int(command)
        if (zoom_level > 19 or zoom_level < 6):
            print("Zoom level must be between 6 and 19 (including)")
            continue
        map.zoom = zoom_level
        composer.compose(map)
        toEPD.convert(map, show)
        #displayer.display()
    except (ValueError):
        print("Input: numbers, 'exit'")

#displayer.sleep()