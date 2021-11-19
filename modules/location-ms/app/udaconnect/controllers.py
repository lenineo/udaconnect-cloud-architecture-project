from datetime import datetime

from app.udaconnect.models import Location
from app.udaconnect.schemas import (
    LocationSchema
)
from app.udaconnect.services import LocationService
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import Optional, List

DATE_FORMAT = "%Y-%m-%d"


api = Namespace("UdaConnect", description="Location microservice - microservice to get geolocation data of UdaConnect project..")  # noqa


@api.route("/locations")
class LocationPostResource(Resource):
    @accepts(schema=LocationSchema)
    @responds(schema=LocationSchema)
    def post(self) -> Location:
        request.get_json()
        location: Location = LocationService.create(request.get_json())
        return location

@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")
class LocationGetResource(Resource):
    @responds(schema=LocationSchema)
    def get(self, location_id) -> Location:
        location: Location = LocationService.retrieve(location_id)
        return location



@api.route("/locations/persons/<person_id>")
@api.param("person_id", "Unique ID for a given Person", _in="query")
@api.param("start_date", "Lower bound of date range",  _in="query", required=True)
@api.param("end_date", "Upper bound of date range",  _in="query", required=True)
@api.param("distance", "Proximity to a given user in meters", _in="query")
class LocationsResource(Resource):
    @responds(schema=LocationSchema, many=True)
    def get(self, person_id) -> List[Location]:
        start_date: datetime = datetime.strptime(
            request.args["start_date"], DATE_FORMAT
        )
        end_date: datetime = datetime.strptime(request.args["end_date"], DATE_FORMAT)
        distance: Optional[int] = request.args.get("distance", 5)

        locations: List[Location] = LocationService.find_contacts_locations(person_id,
             start_date=start_date,
             end_date=end_date,
             meters=distance)
        return locations
