from sqlalchemy import Column, Integer
from geoalchemy2 import Geometry

from database import Base


class Well(Base):
    """ Well represents a well in the database """
    __tablename__ = "well"

    well_tag_number = Column(Integer, primary_key=True, index=True)
    geom = Column(Geometry('POINT'))
