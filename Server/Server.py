from flask import Flask, send_file
from Map import Map
from MapComposer import MapComposer
from MapRenderer import MapRenderer
from Utils import Utils, Definitions

app = Flask(__name__)

show = False
center_point = [50.635678, 26.212011]
zoom_level = 17

composer = MapComposer()
renderer = MapRenderer()
map = Map(center_point, zoom_level)

@app.route("/map/<float:lat>/<float:lon>/<int:zoom>", methods = ["GET"])
def render_map(lat, lon, zoom):
    map.center = [lat, lon]
    map.zoom = zoom
    composer.compose(map)
    renderer.render(map, show)
    return send_file(Utils.find_file("Map.png", Definitions.MAP_FOLDER), mimetype = "image/png")

@app.route("/map", methods = ["GET"])
def server_info():
    return "Server is running"

app.run(host = "0.0.0.0")