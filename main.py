""" retrieve well locations from database and respond with geojson """
import os
from typing import List
from geojson import FeatureCollection, Point, Feature

from fastapi import FastAPI, Depends
from starlette.requests import Request
from starlette.responses import Response
from pydantic import BaseModel, validator, BaseConfig
from geoalchemy2 import WKTElement
from geoalchemy2.shape import to_shape
from sqlalchemy.orm import Session

from database import SessionLocal
from locations import get_wells, get_wells_geojson_from_db

app = FastAPI()


def get_coordinates_from_geom(geom: WKTElement):
    """ converts geom (PostGIS) to coordinates """
    shply_geom = to_shape(geom)
    coordinates = (shply_geom.x, shply_geom.y)
    return coordinates


def get_db(request: Request):
    return request.state.db


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


@app.get("/gwells/api/v2/fa-locations", response_model=FeatureCollection)
def read_locations(db: Session = Depends(get_db)):
    wells = get_wells(db)

    return wells


@app.get("/gwells/api/v3/fa-locations", response_model=FeatureCollection)
def read_locations(db: Session = Depends(get_db)):
    wells = get_wells_geojson_from_db()

    return wells
