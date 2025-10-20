class Map:
    def __init__(self, bbox, zoom):
        self.bbox = bbox
        self.zoom = zoom
        self.features = None
        self.network = None
        self.street_widths = None
        self.railway_width = None