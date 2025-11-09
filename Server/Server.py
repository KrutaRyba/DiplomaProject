from flask import Flask, send_file
from MapComposer import MapComposer
from ToEPDFormat import ToEPDFormat
from Map import Map

app = Flask(__name__)

show = False
center_point = [50.635678, 26.212011]
zoom_level = 17

composer = MapComposer()
toEPD = ToEPDFormat()
map = Map(center_point, zoom_level)

@app.route("/map/<float:lat>/<float:lon>/<int:zoom>", methods = ["GET"])
def render_map(lat, lon, zoom):
    map.center = [lat, lon]
    map.zoom = zoom
    composer.compose(map)
    toEPD.convert(map, show)
    return send_file("Map.png", mimetype = "image/png")

@app.route("/map", methods = ["GET"])
def server_info():
    return "Server is running"

app.run(host = "0.0.0.0")