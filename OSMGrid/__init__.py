from itertools import product
from operator import itemgetter
from json import dump

from PIL import Image
from PIL.ImageDraw import ImageDraw

from psycopg2 import connect

from .data import get_landusages_imposm, get_roads_imposm, get_buildings_imposm

class GridResponse:

    def __init__(self, image, values):
        self.image = image
        self.values = values
    
    def save(self, out, format):
        if format == 'PNG':
            self.image.save(out, format)
        elif format == 'JSON':
            dump(self.values, out, separators=(',',':'))

class Provider:
    
    def __init__(self, layer):
        self.layer = layer
        self.scale = 4
    
    def getTypeByExtension(self, ext):
        
        if ext.lower() == 'png':
            return 'image/png', 'PNG'

        if ext.lower() == 'json':
            return 'text/json', 'JSON'
    
    def renderTile(self, width, height, srs, coord):
        # return an object with a PIL-like save() method for a tile
        
        _width, _height = width/self.scale, height/self.scale
        
        img = Image.new('RGB', (_width, _height), (0, 0, 0))
        draw = ImageDraw(img)
        
        #
        # Prepare query geometry.
        #
        
        ul = self.layer.projection.coordinateProj(coord)
        lr = self.layer.projection.coordinateProj(coord.down().right())
        
        x_offset, y_offset = -ul.x, -ul.y
        x_scale, y_scale = _width / (lr.x - ul.x), _height / (lr.y - ul.y)
        transform = x_offset, y_offset, x_scale, y_scale
        
        buf = (lr.x - ul.x) / 2
        bbox = 'ST_SetSRID(ST_Buffer(ST_MakeBox2D(ST_MakePoint(%.3f, %.3f), ST_MakePoint(%.3f, %.3f)), %.3f, 2), 900913)' % (ul.x, ul.y, lr.x, lr.y, buf)
        colors = product(range(0, 0xff, 4), range(0, 0xff, 4), range(0x66, 0xff, 4))
        
        #
        # Draw the grid itself and note object color keys as we go.
        #
        
        objects = {}
        db = connect(database='geodata', user='geodata').cursor()
        
        for (id, type, name, shape) in get_landusages_imposm(db, bbox, *transform):
            rgb = colors.next()
            objects[rgb] = 'land', type, name, id
            
            for geom in getattr(shape, 'geoms', [shape]):
                for ring in [geom.exterior] + list(geom.interiors):
                    draw.polygon(list(ring.coords), fill=rgb)
        
        
        if coord.zoom >= 16:
            for (id, type, shape) in get_buildings_imposm(db, bbox, *transform):
                rgb = colors.next()
                objects[rgb] = 'building', name, id
                
                for geom in getattr(shape, 'geoms', [shape]):
                    for ring in [geom.exterior] + list(geom.interiors):
                        draw.polygon(list(ring.coords), fill=rgb)
        
        for (id, type, name, way) in get_roads_imposm(db, bbox, *transform):
            rgb = colors.next()
            objects[rgb] = 'road', type, name, id
            
            for geom in getattr(way, 'geoms', [way]):
                stroke = {18: 4, 17: 3}.get(coord.zoom, 2)
                draw.line(list(geom.coords), fill=rgb, width=stroke)
        
        db.close()
        
        #
        # Collect actual rgb values from image and sort them by frequency
        # so we can build up a grid with the most number of one-and-two-digit
        # numbers that are also keys into the details array.
        #
        
        data = [(r, g, b) for (r, g, b) in img.getdata()]
        rgb_counts = {}
        
        for rgb in data:
            rgb_counts[rgb] = rgb_counts.get(rgb, 0) + 1
        
        rgb_counts = sorted(rgb_counts.items(), key=itemgetter(1), reverse=True)
        rgb_indexes = [key for (key, count) in rgb_counts]
        
        #
        # Build a details array and a two-dimensional column-major grid.
        #
        
        details = [objects.get(rgb, None) for rgb in rgb_indexes]
        
        grid = []

        for row in range(_height):
            row, data = data[:_width], data[_width:]
            row = [rgb_indexes.index(rgb) for rgb in row]
            grid.append(row)
        
        return GridResponse(img.resize((width, height), Image.NEAREST), [details, grid])
