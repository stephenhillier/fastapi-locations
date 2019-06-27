""" retrieve well locations from database and respond with geojson """
from geojson import FeatureCollection
from fastapi import FastAPI
from starlette.middleware.gzip import GZipMiddleware

from locations import get_wells, get_wells_geojson_from_db

app = FastAPI()

app.add_middleware(GZipMiddleware, minimum_size=1000)


@app.get("/gwells/api/v2/fa-locations", response_model=FeatureCollection)
def read_locations_py_geojson():
    wells = get_wells()

    return wells


@app.get("/gwells/api/v3/fa-locations", response_model=FeatureCollection)
def read_locations_db_geojson():
    wells = get_wells_geojson_from_db()

    return wells
