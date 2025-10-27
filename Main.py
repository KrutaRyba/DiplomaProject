from MapComposer import MapComposer
from ToEPDFormat import ToEPDFormat
#from EPDDisplayer import EPDDisplayer
from Map import Map

show = True
center_point = [50.635678, 26.212011]
zoom_level = 17 # >= 9

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

'''
bbox15 = [[26.22046, 50.61347, 26.28784, 50.63792], 15] # :3 Zoom 15
bbox16 = [[26.25853, 50.60180, 26.29221, 50.61403], 16] # :3 Zoom 16
bbox17 = [[26.239064, 50.616918, 26.255908, 50.623031], 17] # :3 Zoom 17
bbox18 = [[26.208277, 50.633920, 26.216699, 50.636976], 18] # :3 Zoom 18
bbox19 = [[26.209651, 50.634805, 26.213862, 50.636333], 19] # :3 Zoom 19
'''