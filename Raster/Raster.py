import math
from PIL import Image
from urllib3 import request
import io

HEIGHT = 480
WIDTH = 800
TILE_SIZE = 256

def sec(x):
    return 1.0 / math.cos(x)

def LatLonToXY(lat, lon, zoom):
    n = pow(2.0, zoom)
    X = int(n * ((lon + 180.0) / 360.0))
    latRad = math.radians(lat)
    Y = int(n * (1 - (math.log(math.tan(latRad) + sec(latRad)) / math.pi)) / 2.0)
    return (X, Y)

def XYtoLatLon(X, Y, zoom):
    n = math.pow(2.0, zoom)
    lon = (X / n) * 360.0 - 180.0
    lat = math.atan(math.sinh(math.pi - (Y / n) * 2 * math.pi)) * (180.0 / math.pi)
    return(lat, lon)

def GetMap(lat, lon, zoom):
    img = Image.new("RGB", (WIDTH, HEIGHT))
    n_x = math.ceil(WIDTH / TILE_SIZE)
    n_y = math.ceil(HEIGHT / TILE_SIZE)
    x, y = LatLonToXY(lat, lon, zoom)
    # TODO: restrict number of tiles (numer of tiles = [2^zoom * 2^zoom] or [(2^zoom)^2])
    for i in range(n_x):
        for j in range(n_y):
            response = request("GET", "https://tile.openstreetmap.org/{zPar}/{xPar}/{yPar}.png".format(zPar = zoom, xPar = i + x, yPar = j + y))
            img.paste(Image.open(io.BytesIO(response.data)), (i * TILE_SIZE, j * TILE_SIZE))
    img.show("Map")
    img.close()

zoom = 2
lon = 31.1828699
lat = 48.383022
GetMap(lat, lon, zoom)
command = ""
delta = 20.0 / (zoom + 1e-12)
while(command != "exit"):
    command = input("Give input: ")
    if (command == "w"):
        lat = lat + delta
        GetMap(lat, lon, zoom)
    elif (command == "s"):
        lat = lat - delta
        GetMap(lat, lon, zoom)
    elif (command == "a"):
        lon = lon - delta
        GetMap(lat, lon, zoom)
    elif (command == "d"):
        lon = lon - delta
        GetMap(lat, lon, zoom)
    elif (command == "o"):
        if (zoom <= 18):
            zoom = zoom + 1
            GetMap(lat, lon, zoom)
    elif (command == "p"):
        if (zoom >= 1):
            zoom = zoom - 1
            GetMap(lat, lon, zoom)