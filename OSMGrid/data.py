from shapely.wkb import loads

def get_polygons_osm2pgsql(db, bbox, xoff, yoff, xfac, yfac):
    """
    """
    query = """SELECT osm_id, name,
                      ST_AsBinary(ST_TransScale(way, %(xoff).3f, %(yoff).3f, %(xfac).3f, %(yfac).3f)) AS way
               FROM planet_osm_polygon
               WHERE way && %(bbox)s
                 AND ST_Intersects(way, %(bbox)s)
                 AND osm_id > 0
               ORDER BY ST_Area(way) DESC""" \
          % locals()
    
    db.execute(query)
    
    return [(id, name, loads(str(way_wkb)))
            for (id, name, way_wkb) in db.fetchall()]

def get_polygons_osm2pgsql(db, bbox, xoff, yoff, xfac, yfac):
    """
    """
    query = """SELECT osm_id, name,
                      ST_AsBinary(ST_TransScale(way, %(xoff).3f, %(yoff).3f, %(xfac).3f, %(yfac).3f)) AS way
               FROM planet_osm_polygon
               WHERE way && %(bbox)s
                 AND ST_Intersects(way, %(bbox)s)
                 AND osm_id > 0
               ORDER BY ST_Area(way) DESC""" \
          % locals()
    
    db.execute(query)
    
    return [(id, name, loads(str(way_wkb)))
            for (id, name, way_wkb) in db.fetchall()]

def get_linestrings_osm2pgsql(db, bbox, xoff, yoff, xfac, yfac):
    """
    """
    query = """SELECT osm_id, name,
                      ST_AsBinary(ST_TransScale(way, %(xoff).3f, %(yoff).3f, %(xfac).3f, %(yfac).3f)) AS way
               FROM planet_osm_line
               WHERE way && %(bbox)s
                 AND ST_Intersects(way, %(bbox)s)
                 AND osm_id > 0
               ORDER BY ST_Length(way) DESC""" \
          % locals()
    
    db.execute(query)
    
    return [(id, name, loads(str(way_wkb)))
            for (id, name, way_wkb) in db.fetchall()]

def get_landusages_imposm(db, bbox, xoff, yoff, xfac, yfac):
    """
    """
    query = """SELECT osm_id, type, name,
                      ST_AsBinary(ST_TransScale(the_geom, %(xoff).3f, %(yoff).3f, %(xfac).3f, %(yfac).3f)) AS the_geom
               FROM imposm_oakland_landusages
               WHERE the_geom && %(bbox)s
                 AND ST_Intersects(the_geom, %(bbox)s)
                 AND osm_id > 0
               ORDER BY z_order ASC, area ASC""" \
          % locals()
    
    db.execute(query)
    
    return [(id, type, name, loads(str(way_wkb)))
            for (id, type, name, way_wkb) in db.fetchall()]

def get_roads_imposm(db, bbox, xoff, yoff, xfac, yfac):
    """
    """
    query = """SELECT osm_id, type, name,
                      ST_AsBinary(ST_TransScale(the_geom, %(xoff).3f, %(yoff).3f, %(xfac).3f, %(yfac).3f)) AS the_geom
               FROM imposm_oakland_roads
               WHERE the_geom && %(bbox)s
                 AND ST_Intersects(the_geom, %(bbox)s)
                 AND osm_id > 0
               ORDER BY z_order ASC, ST_Length(the_geom) ASC""" \
          % locals()
    
    db.execute(query)
    
    return [(id, type, name, loads(str(way_wkb)))
            for (id, type, name, way_wkb) in db.fetchall()]

def get_mainroads_imposm(db, bbox, xoff, yoff, xfac, yfac):
    """
    """
    query = """SELECT osm_id, type, name,
                      ST_AsBinary(ST_TransScale(the_geom, %(xoff).3f, %(yoff).3f, %(xfac).3f, %(yfac).3f)) AS the_geom
               FROM imposm_oakland_mainroads
               WHERE the_geom && %(bbox)s
                 AND ST_Intersects(the_geom, %(bbox)s)
                 AND osm_id > 0
               ORDER BY z_order ASC, ST_Length(the_geom) ASC""" \
          % locals()
    
    db.execute(query)
    
    return [(id, type, name, loads(str(way_wkb)))
            for (id, type, name, way_wkb) in db.fetchall()]

def get_motorways_imposm(db, bbox, xoff, yoff, xfac, yfac):
    """
    """
    query = """SELECT osm_id, type, name,
                      ST_AsBinary(ST_TransScale(the_geom, %(xoff).3f, %(yoff).3f, %(xfac).3f, %(yfac).3f)) AS the_geom
               FROM imposm_oakland_motorways
               WHERE the_geom && %(bbox)s
                 AND ST_Intersects(the_geom, %(bbox)s)
                 AND osm_id > 0
               ORDER BY z_order ASC, ST_Length(the_geom) ASC""" \
          % locals()
    
    db.execute(query)
    
    return [(id, type, name, loads(str(way_wkb)))
            for (id, type, name, way_wkb) in db.fetchall()]

def get_buildings_imposm(db, bbox, xoff, yoff, xfac, yfac):
    """
    """
    query = """SELECT osm_id, name,
                      ST_AsBinary(ST_TransScale(the_geom, %(xoff).3f, %(yoff).3f, %(xfac).3f, %(yfac).3f)) AS the_geom
               FROM imposm_oakland_buildings
               WHERE the_geom && %(bbox)s
                 AND ST_Intersects(the_geom, %(bbox)s)
                 AND osm_id > 0""" \
          % locals()
    
    db.execute(query)
    
    return [(id, name, loads(str(way_wkb)))
            for (id, name, way_wkb) in db.fetchall()]
