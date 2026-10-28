from fastapi import FastAPI, Response, status
import os
from dotenv import load_dotenv

import psycopg
from psycopg.rows import dict_row

from app.broadcaster import broadcaster

app = FastAPI()

from fastapi.staticfiles import StaticFiles
from app.routes import alerts

app.include_router(alerts.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

load_dotenv()

DB_CONNECTION = os.getenv("DATABASE_URL")

from models.organisation import organisation
from models.location import location
from models.launchpad import launchpad
from models.vehicle import vehicle
from models.launch import launch


from datetime import datetime
from pydantic import BaseModel

class launch_update(BaseModel):
	id: int
	rocket: str
	provider: str
	launch_time: datetime
	status: str
	is_crewed: bool
	webcast_url: str


# Endpoint to check the health of the API
@app.get("/health")
def get_health(response: Response):
	response.status_code = status.HTTP_200_OK
	return


# Endpoints to get all data in the specified table

# Gets all rows in organisations table
@app.get("/organisations")
def get_organisations(response: Response) -> dict:

	try:
		with psycopg.connect(DB_CONNECTION, row_factory = dict_row) as conn:
			rows = conn.execute(
				"SELECT * FROM organisations ORDER BY name"
			).fetchall()

		result = {row["id"]: row for row in rows}

		response.status_code = status.HTTP_200_OK
		return result

	except Exception:
		response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return

# Gets all rows in locations table
@app.get("/locations")
def get_locations(response: Response) -> dict:

	try:
		with psycopg.connect(DB_CONNECTION, row_factory = dict_row) as conn:
			rows = conn.execute(
				"SELECT * FROM locations ORDER BY name"
			).fetchall()

		result = {row["id"]: row for row in rows}

		response.status_code = status.HTTP_200_OK
		return result

	except Exception:
		response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return

# Gets all rows in launchpads table
@app.get("/launchpads")
def get_launchpads(response: Response) -> dict:

	try:
		with psycopg.connect(DB_CONNECTION, row_factory = dict_row) as conn:
			rows = conn.execute(
				"SELECT * FROM launchpads ORDER BY name"
			).fetchall()

		result = {row["id"]: row for row in rows}

		response.status_code = status.HTTP_200_OK
		return result

	except Exception:
		response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return

# Gets all rows in vehicles table
@app.get("/vehicles")
def get_vehicles(response: Response) -> dict:

	try:
		with psycopg.connect(DB_CONNECTION, row_factory = dict_row) as conn:
			rows = conn.execute(
				"SELECT * FROM vehicles ORDER BY name"
			).fetchall()

		result = {row["id"]: row for row in rows}

		response.status_code = status.HTTP_200_OK
		return result

	except Exception:
		response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return

# Gets all rows in launches table
@app.get("/launches")
def get_launches(response: Response) -> dict:

	try:
		with psycopg.connect(DB_CONNECTION, row_factory = dict_row) as conn:
			rows = conn.execute(
				"SELECT * FROM launches ORDER BY date"
			).fetchall()

		result = {row["id"]: row for row in rows}

		response.status_code = status.HTTP_200_OK
		return result

	except Exception:
		response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return


# Endpoints to get 1 row with a given id

# Gets row by id for organisations
@app.get("/organisations/{organisation_id}")
def get_organisations_by_id(organisation_id: int, response: Response) -> dict:

	try:
		with psycopg.connect(DB_CONNECTION, row_factory = dict_row) as conn:
			row = conn.execute(
				"SELECT * FROM organisations WHERE id = %s", (organisation_id,)
			).fetchall()

		response.status_code = status.HTTP_200_OK
		return row[0]

	except Exception:
		response.status_code = status.HTTP_404_NOT_FOUND
		return

# Gets row by id for locations
@app.get("/locations/{location_id}")
def get_locations_by_id(location_id: int, response: Response) -> dict:

	try:
		with psycopg.connect(DB_CONNECTION, row_factory = dict_row) as conn:
			row = conn.execute(
				"SELECT * FROM locations WHERE id = %s", (location_id,)
			).fetchall()

		response.status_code = status.HTTP_200_OK
		return row[0]

	except Exception:
		response.status_code = status.HTTP_404_NOT_FOUND
		return

# Gets row by id for launchpads
@app.get("/launchpads/{launchpad_id}")
def get_launchpads_by_id(launchpad_id: int, response: Response) -> dict:

	try:
		with psycopg.connect(DB_CONNECTION, row_factory = dict_row) as conn:
			row = conn.execute(
				"SELECT * FROM launchpads WHERE id = %s", (launchpad_id,)
			).fetchall()

		response.status_code = status.HTTP_200_OK
		return row[0]

	except Exception:
		response.status_code = status.HTTP_404_NOT_FOUND
		return

# Gets row by id for vehicles
@app.get("/vehicles/{vehicle_id}")
def get_vehicles_by_id(vehicle_id: int, response: Response) -> dict:

	try:
		with psycopg.connect(DB_CONNECTION, row_factory = dict_row) as conn:
			row = conn.execute(
				"SELECT * FROM vehicles WHERE id = %s", (vehicle_id,)
			).fetchall()

		response.status_code = status.HTTP_200_OK
		return row[0]

	except Exception:
		response.status_code = status.HTTP_404_NOT_FOUND
		return

# Gets row by id for launches
@app.get("/launches/{launch_id}")
def get_launches_by_id(launch_id: int, response: Response) -> dict:

	try:
		with psycopg.connect(DB_CONNECTION, row_factory = dict_row) as conn:
			row = conn.execute(
				"SELECT * FROM launches WHERE id = %s", (launch_id,)
			).fetchall()

		response.status_code = status.HTTP_200_OK
		return row[0]

	except Exception:
		response.status_code = status.HTTP_404_NOT_FOUND
		return


# Create endpoints for all tables

# Creates a new organisation
@app.post("/organisations/create")
def create_organisation(payload: organisation, response: Response) -> dict:

	try:
		with psycopg.connect(DB_CONNECTION, row_factory = dict_row) as conn:
			organisation = conn.execute(
				"INSERT INTO organisations (name, country, type, administrator, website) VALUES (%(name)s, %(country)s, %(type)s, %(administrator)s, %(website)s) RETURNING *",
				{
					"name": payload.name,
					"country": payload.country,
					"type": payload.type,
					"administrator": payload.administrator,
					"website": payload.website
				}
			).fetchone()

			conn.commit()

		broadcaster.publish(organisation)

		response.status_code = status.HTTP_201_CREATED
		return organisation

	except Exception:
		response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return

# Creates a new location
@app.post("/locations/create")
def create_location(payload: location, response: Response) -> dict:

	try:
		with psycopg.connect(DB_CONNECTION, row_factory = dict_row) as conn:
			location = conn.execute(
				"INSERT INTO locations (name, country, region) VALUES (%(name)s, %(country)s, %(region)s) RETURNING *",
				{
					"name": payload.name,
					"country": payload.country,
					"region": payload.region
				}
			).fetchone()

			conn.commit()

		broadcaster.publish(location)

		response.status_code = status.HTTP_201_CREATED
		return location

	except Exception:
		response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

# Creates a new launchpad
@app.post("/launchpads/create")
def create_launchpad(payload: launchpad, response: Response) -> dict:

	try:
		with psycopg.connect(DB_CONNECTION, row_factory = dict_row) as conn:
			launchpad = conn.execute(
				"INSERT INTO launchpads (name, longitude, latitude, status, organisation_id, location_id) VALUES (%(name)s, %(longitude)s, %(latitude)s, %(status)s, %(organisation_id)s, %(location_id)s) RETURNING *",
				{
					"name": payload.name,
					"longitude": payload.longitude,
					"latitude": payload.latitude,
					"status": payload.status,
					"organisation_id": payload.organisation_id,
					"location_id": payload.location_id
				}
			).fetchone()

			conn.commit()

		broadcaster.publish(launchpad)

		response.status_code = status.HTTP_201_CREATED
		return launchpad

	except Exception:
		response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return

# Creates a new vehicle
@app.post("/vehicles/create")
def create_vehicle(payload: vehicle, response: Response) -> dict:

	try:
		with psycopg.connect(DB_CONNECTION, row_factory = dict_row) as conn:
			vehicle = conn.execute(
				"INSERT INTO vehicles (name, family, height_m, diameter_m, mass_kg, payload_leo_kg, payload_gto_kg, payload_sso_kg, stages, first_flight, thrust_kn, status, organisation_id) VALUES (%(name)s, %(family)s, %(height_m)s, %(diameter_m)s, %(mass_kg)s, %(payload_leo_kg)s, %(payload_gto_kg)s, %(payload_sso_kg)s, %(stages)s, %(first_flight)s, %(thrust_kn)s, %(status)s, %(organisation_id)s) RETURNING *",
				{
					"name": payload.name,
					"family": payload.family,
					"height_m": payload.height_m,
					"diameter_m": payload.diameter_m,
					"mass_kg": payload.mass_kg,
					"payload_leo_kg": payload.payload_leo_kg,
					"payload_gto_kg": payload.payload_gto_kg,
					"payload_sso_kg": payload.payload_sso_kg,
					"stages": payload.stages,
					"first_flight": payload.first_flight,
					"thrust_kn": payload.thrust_kn,
					"status": payload.status,
					"organisation_id": payload.organisation_id
				}
			).fetchone()

			conn.commit()

		broadcaster.publish(vehicle)

		response.status_code = status.HTTP_201_CREATED
		return vehicle

	except Exception:
		response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return

# Creates a new launch
@app.post("/launches/create")
def create_launch(payload: launch, response: Response) -> dict:

	try:
		with psycopg.connect(DB_CONNECTION, row_factory = dict_row) as conn:
			launch = conn.execute(
				"INSERT INTO launches (date, status, webcast_url, mission, payload, vehicle_id, launchpad_id, organisation_id) VALUES (%(date)s, %(status)s, %(webcast_url)s, %(mission)s, %(payload)s, %(vehicle_id)s, %(launchpad_id)s, %(organisation_id)s) RETURNING *",
				{
					"date": payload.date,
					"status": payload.status,
					"webcast_url": payload.webcast_url,
					"mission": payload.mission,
					"payload": payload.payload,
					"vehicle_id": payload.vehicle_id,
					"launchpad_id": payload.launchpad_id,
					"organisation_id": payload.organisation_id
				}
			).fetchone()

			conn.commit()

		broadcaster.publish(launch)

		response.status_code = status.HTTP_201_CREATED
		return launch

	except Exception:
		response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return

@app.put("/launches/update")
def update_launch(payload: launch_update) -> dict:

	with psycopg.connect(DB_CONNECTION, row_factory = dict_row) as conn:
		conn.execute(
			"UPDATE launches SET rocket = %(rocket)s, provider = %(provider)s, launch_time = %(launch_time)s, status = %(status)s, is_crewed = %(is_crewed)s, webcast_url = %(webcast_url)s WHERE id = %(id)s",
			{
				"rocket":  payload.rocket,
				"provider": payload.provider,
				"launch_time": payload.launch_time,
				"status": payload.status,
				"is_crewed": payload.is_crewed,
				"webcast_url": payload.webcast_url,
				"id": payload.id
			}
		)

	return payload


# Endpoints to delete rows by id

# Deletes organisation by id
@app.delete("/organisations/delete/{organisation_id}")
def delete_organisation(organisation_id: int, response: Response):

	try:
		with psycopg.connect(DB_CONNECTION, row_factory = dict_row) as conn:
			conn.execute(
				"DELETE FROM organisations WHERE id = %s", (organisation_id,)
			)

		response.status_code = status.HTTP_204_NO_CONTENT
		return

	except Exception:
		response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return

# Deletes location by id
@app.delete("/locations/delete/{location_id}")
def delete_location(location_id: int, response: Response):

	try:
		with psycopg.connect(DB_CONNECTION, row_factory = dict_row) as conn:
			conn.execute(
				"DELETE FROM locations WHERE id = %s", (location_id,)
			)

		response.status_code = status.HTTP_204_NO_CONTENT
		return

	except Exception:
		response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return

# Deletes launchpad by id
@app.delete("/launchpads/delete/{launchpad_id}")
def delete_launchpad(launchpad_id: int, response: Response):

	try:
		with psycopg.connect(DB_CONNECTION, row_factory = dict_row) as conn:
			conn.execute(
				"DELETE FROM launchpads WHERE id = %s", (launchpad_id,)
			)

		response.status_code = status.HTTP_204_NO_CONTENT
		return

	except Exception:
		response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return

# Deletes vehicle by id
@app.delete("/vehicles/delete/{vehicle_id}")
def delete_vehicle(vehicle_id: int, response: Response):

	try:
		with psycopg.connect(DB_CONNECTION, row_factory = dict_row) as conn:
			conn.execute(
				"DELETE FROM vehicles WHERE id = %s", (vehicle_id,)
			)

		response.status_code = status.HTTP_204_NO_CONTENT
		return

	except Exception:
		response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return

# Deletes launch by id
@app.delete("/launches/delete/{launch_id}")
def delete_launch(launch_id: int, response: Response):

	try:
		with psycopg.connect(DB_CONNECTION, row_factory = dict_row) as conn:
			conn.execute(
				"DELETE FROM launches WHERE id = %s", (launch_id,)
			)

		response.status_code = status.HTTP_204_NO_CONTENT
		return

	except Exception:
		response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return