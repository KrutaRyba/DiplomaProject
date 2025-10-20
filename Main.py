from MapComposer import MapComposer
from ToEPDFormat import ToEPDFormat
from Map import Map

#bbox = [26.235330, 50.626312, 26.243752, 50.629368] # Rail
#bbox = [33.469369, 44.5166561, 33.473580, 44.518373] # Sand
#bbox = [26.236250, 50.619697, 26.240461, 50.621226] # River
bbox = [26.209651, 50.634805, 26.213862, 50.636333] # :3
zoom = 1
show = True
composer = MapComposer()
toEPD = ToEPDFormat()
map = Map(bbox, zoom)
composer.compose(map)
toEPD.convert(map, show)