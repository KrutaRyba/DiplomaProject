from flask import Flask, send_file
from LocalConnector import LocalConnector
from OSMNXConnector import OSMNXConnector
from Map import Map
from MapComposer import MapComposer
from MapRenderer import MapRenderer
from json import load
from Utils import ConsoleStyles
from os.path import exists

app = Flask(__name__)

from_file = None
osm_file = None
show = False

with open("ServerConfig.json") as file:
    loaded = load(file)
    from_file = loaded["from_file"]
    osm_file = loaded["osm_file"]

if (from_file == None or osm_file == None):
    print(f"{ConsoleStyles.ERROR}Configure ServerConfig.json{ConsoleStyles.NORMAL}")
    exit()

if (not exists(osm_file)):
    print(f"{ConsoleStyles.WARNING}OSM file does not exist or specified path is incorrect. Proceeding with OSMnx API{ConsoleStyles.NORMAL}")
    from_file = False

@app.route("/map/<float:lat>/<float:lon>/<int:zoom>", methods = ["GET"])
def render_map(lat, lon, zoom):
    if (zoom > 19): zoom = 19
    if (zoom < 6): zoom = 6
    map = Map((lat, lon), zoom)
    connector = LocalConnector() if (from_file) else OSMNXConnector()
    composer = MapComposer(connector)
    renderer = MapRenderer()
    composer.compose(map)
    bytes = renderer.render(map, show)
    return send_file(bytes, mimetype = "image/png")

@app.route("/map", methods = ["GET"])
def server_info():
    return "Server is running"

app.run(host = "0.0.0.0")