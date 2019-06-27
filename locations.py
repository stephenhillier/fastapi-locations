from typing import List
from sqlalchemy.orm import Session

from models import Well


def get_wells(db: Session) -> List[Well]:
    """ retrieves all locations from the database """
    return db.query(Well).filter(Well.geom.isnot(None))
