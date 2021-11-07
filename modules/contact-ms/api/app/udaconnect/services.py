import logging
import requests
import os
from datetime import datetime, timedelta
from typing import Dict, List

from app import db
from app.udaconnect.models import Connection, Location, Person
from app.udaconnect.schemas import ConnectionSchema, LocationSchema, PersonSchema
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-api")

PERSON_SERVICE_API_URL = os.environ["PERSON_SERVICE_API_URL"]
LOCATION_SERVICE_API_URL = os.environ["LOCATION_SERVICE_API_URL"]


class ConnectionService:
    @staticmethod
    def find_contacts(person_id: int, start_date: datetime, end_date: datetime, meters=5) -> List[Connection]:
        locations = LocationService.find_locations(person_id, start_date, end_date, meters=5)

        persons: List[Person] = []
        persons = PersonService.find_persons(person_id, start_date, end_date, meters=5)

        # Cache all users in memory for quick lookup
        person_map: Dict[str, Person] = {person.id: person for person in persons}

        result: List[Connection] = []

        for location in locations:
            result.append(
                Connection(
                    person=person_map[location.person_id], location=location
                )
            )

        return result


class LocationService:
    @staticmethod
    def find_locations(person_id: int, start_date: datetime, end_date: datetime, meters=5) -> List[Location]:
        locations: List[Location] = []
        locations = requests.get("{}/locations/{}?person_id={}&start_date={}&end_date={}&meters={}".format(
            LOCATION_SERVICE_API_URL, person_id, start_date, end_date, meters))
        return locations


class PersonService:
    @staticmethod
    def find_persons(person_id: int, start_date: datetime, end_date: datetime, meters=5):
        persons: List[Person] = []
        persons = requests.get("{}/persons/{}?person_id={}&start_date={}&end_date={}&meters={}".format(
            LOCATION_SERVICE_API_URL, person_id, start_date, end_date, meters))
        return persons
