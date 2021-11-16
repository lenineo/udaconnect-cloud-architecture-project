import logging
import requests
import os
from datetime import datetime, timedelta
from typing import Dict, List
from geoalchemy2.functions import ST_AsText, ST_Point

from app.udaconnect.models import Connection, Location, Person


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("contact-ms")

PERSON_SERVICE_API_URL = os.environ["PERSON_MS_URL"]
LOCATION_SERVICE_API_URL = os.environ["LOCATION_MS_URL"]


class ConnectionService:
    @staticmethod
    def find_contacts(person_id: int, start_date: datetime, end_date: datetime, meters=5) -> List[Connection]:
        locations: List[Location] = []
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

        locationsResp = requests.get("{}/locations/persons/{}?start_date={}&end_date={}&meters={}".format(
            LOCATION_SERVICE_API_URL, person_id, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), meters))


        body = locationsResp.json()

        for item in body:
            location = Location()
            location.id = item["id"]
            location.person_id = item["person_id"]
            location.coordinate = ST_Point(item["latitude"], item["longitude"])
            location.creation_time = datetime.strptime(item['creation_time'], "%Y-%m-%dT%H:%M:%S")
            locations.append(location)

        return locations


class PersonService:
    @staticmethod
    def find_persons(person_id: int, start_date: datetime, end_date: datetime, meters=5)  -> List[Person]:
        persons: List[Person] = []
        personsResp = requests.get("{}/persons".format(
            PERSON_SERVICE_API_URL))
        body = personsResp.json()
        for item in body:
            person = Person()
            person.id = item["id"]
            person.first_name = item["first_name"]
            person.last_name = item["last_name"]
            person.company_name = item["company_name"]
            persons.append(person)

        return persons
