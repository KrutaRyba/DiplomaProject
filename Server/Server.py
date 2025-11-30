from flask import Flask, send_file
from LocalConnector import LocalConnector
from OSMNXConnector import OSMNXConnector
from Map import Map
from MapComposer import MapComposer
from MapRenderer import MapRenderer
from json import load

app = Flask(__name__)

from_file = None
show = False

with open("ServerConfig.json") as file:
    loaded = load(file)
    from_file = loaded["from_file"]

if (from_file == None): raise RuntimeError("Configure ServerConfig.json")

connector = LocalConnector() if (from_file) else OSMNXConnector()
composer = MapComposer(connector)
renderer = MapRenderer()

@app.route("/map/<float:lat>/<float:lon>/<int:zoom>", methods = ["GET"])
def render_map(lat, lon, zoom):
    if (zoom > 19): zoom = 19
    if (zoom < 6): zoom = 6
    map = Map((lat, lon), zoom)
    composer.compose(map)
    bytes = renderer.render(map, show)
    return send_file(bytes, mimetype = "image/png")

@app.route("/map", methods = ["GET"])
def server_info():
    return "Server is running"

app.run(host = "0.0.0.0")