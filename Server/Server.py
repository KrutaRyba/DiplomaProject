from flask import Flask, send_file
from LocalConnector import LocalConnector
from OSMNXConnector import OSMNXConnector
from Map import Map
from MapComposer import MapComposer
from MapRenderer import MapRenderer
from Utils import Utils, Definitions
from json import load

app = Flask(__name__)

is_local = None
show = False

with open("ServerConfig.json") as file:
    loaded = load(file)
    is_local = loaded["is_local"]

if (is_local == None): raise RuntimeError("Configure ServerConfig.json")

connector = LocalConnector() if (is_local) else OSMNXConnector()
composer = MapComposer(connector)
renderer = MapRenderer()

@app.route("/map/<float:lat>/<float:lon>/<int:zoom>", methods = ["GET"])
def render_map(lat, lon, zoom):
    if (zoom > 19): zoom = 19
    if (zoom < 6): zoom = 6
    map = Map((lat, lon), zoom)
    composer.compose(map)
    renderer.render(map, show)
    return send_file(Utils.find_file("Map.png", Definitions.MAP_FOLDER), mimetype = "image/png")

@app.route("/map", methods = ["GET"])
def server_info():
    return "Server is running"

app.run(host = "0.0.0.0")