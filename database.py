import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URI = "postgres://{}:{}@{}/{}".format(
    os.getenv("DBUSER") or "gwells",  # defaults for local dev
    os.getenv("DBPASS") or "",
    os.getenv("DBHOST") or "localhost",
    os.getenv("DBNAME") or "gwells"

)

engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
