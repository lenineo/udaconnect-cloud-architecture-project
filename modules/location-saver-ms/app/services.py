import logging
from .config import SQLALCHEMY_DATABASE_URI
from .models import Location
import os
from typing import Dict
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import sessionmaker
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text
from .shemas import LocationSchema

KAFKA_TOPIC = os.environ["KAFKA_TOPIC"]
KAFKA_SERVER = os.environ["KAFKA_SERVER"]
DB_USERNAME = os.environ['DB_USERNAME']
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_NAME = os.environ['DB_NAME']
DB_HOST = os.environ['DB_HOST']
DB_PORT = os.environ['DB_PORT']

# Logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("location-saver-api")

# Set up database connection
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

Session = sessionmaker(bind=engine)
session = Session()


class LocationService:
    @staticmethod
    def retrieve(location_id) -> Location:
        location, coord_text = (
            session.query(Location, Location.coordinate.ST_AsText())
            .filter(Location.id == location_id)
            .one()
        )

        # Rely on database to return text form of point to reduce overhead of conversion in app code
        location.wkt_shape = coord_text
        return location

    @staticmethod
    def create(location: Dict) -> Location:
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")

        new_location = Location()
        new_location.person_id = location["person_id"]
        new_location.creation_time = location["creation_time"]
        new_location.coordinate = ST_Point(location["latitude"], location["longitude"])
        session.add(new_location)
        session.commit()

        return new_location
