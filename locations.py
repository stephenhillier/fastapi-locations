import os
from typing import List
from sqlalchemy.orm import Session
from geojson import FeatureCollection, Feature, Point
from models import Well
import shapely.wkt

import psycopg2

DBUSER = os.getenv("DBUSER") or "gwells",  # defaults for local dev
DBPASS = os.getenv("DBPASS") or "",
DBHOST = os.getenv("DBHOST") or "localhost",
DBNAME = os.getenv("DBNAME") or "gwells"


def get_coordinates_from_geom(geom):
    """ converts geom (PostGIS) to coordinates """
    point = shapely.wkt.loads(geom)
    return point


def get_wells(db: Session) -> FeatureCollection:
    """ retrieves all locations from the database """

    points = []
    conn = None
    cursor = None

    try:
        print("getting wells from db")
        conn = psycopg2.connect(user="gwells", password="test_pw", host="db", port=5432, database="gwells")
        cursor = conn.cursor()
        query = """ SELECT well_tag_number, ST_AsText(geom) as geom FROM well where geom is not null; """
        cursor.execute(query)
        records = cursor.fetchall()

        for row in records:
            pt = get_coordinates_from_geom(row[1])
            ft = Feature(geometry=pt, id=row[0], properties={"n": row[0]})
            points.append(ft)

    except (Exception, psycopg2.Error) as error:
        print("Error retrieving data", error)
    finally:
        if conn is not None:
            conn.close()

        if cursor is not None:
            cursor.close()

    fc = FeatureCollection(points)

    return fc


def get_wells_geojson_from_db() -> FeatureCollection:

    fc = ""
    conn = None
    cursor = None

    try:
        print("getting wells from db")
        conn = psycopg2.connect(user="gwells", password="test_pw", host="db", port=5432, database="gwells")
        cursor = conn.cursor()
        query = """
            select row_to_json(fc)
            from (
                select 
                    'FeatureCollection' as "type",
                    array_to_json(array_agg(f)) as "features"
                from (
                    select
                        'Feature' as "type",
                        ST_AsGeoJSON(ST_Transform(geom, 4326), 6) :: json as "geometry",
                        (
                            select json_strip_nulls(row_to_json(t))
                            from (
                                select
                                    well_tag_number
                            ) t
                        ) as "properties"
                    from well
                    where geom is not null
                ) as f

            ) as fc;            
        """
        cursor.execute(query)
        records = cursor.fetchall()

        print(len(records), "rows")

        fc = records[0][0]

    except (Exception, psycopg2.Error) as error:
        print("Error retrieving data", error)
    finally:
        if conn is not None:
            conn.close()

        if cursor is not None:
            cursor.close()

    return fc
