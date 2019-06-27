import os
from typing import List
from sqlalchemy.orm import Session
from geojson import FeatureCollection, Feature, Point
from models import Well
from geoalchemy2.shape import to_shape

import psycopg2

DBUSER = os.getenv("DBUSER") or "gwells",  # defaults for local dev
DBPASS = os.getenv("DBPASS") or "",
DBHOST = os.getenv("DBHOST") or "localhost",
DBNAME = os.getenv("DBNAME") or "gwells"


def get_coordinates_from_geom(geom):
    """ converts geom (PostGIS) to coordinates """
    shply_geom = to_shape(geom)
    coordinates = (shply_geom.x, shply_geom.y)
    return coordinates


def get_wells(db: Session) -> FeatureCollection:
    """ retrieves all locations from the database """

    points = []

    try:
        conn = psycopg2.connect(user=DBUSER, password=DBPASS, host=DBHOST, port=5432, database=DBNAME)
        cursor = conn.cursor()
        query = """ SELECT well_tag_number, ST_AsText(geom) as geom FROM well; """
        cursor.execute(query)
        records = cursor.fetchall()

        for row in records:
            pt = Point(get_coordinates_from_geom(row[1]))
            ft = Feature(pt, properties={"n": row[0]})
            points.append(ft)

    except (Exception, psycopg2.Error) as error:
        print("Error retrieving data")

    finally:
        conn.close()

    fc = FeatureCollection(points)

    return fc
