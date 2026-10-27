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

from datetime import datetime
from typing import Literal

from pydantic import BaseModel

Status = Literal["upcoming", "launched", "scrubbed", "failed"]

class launch_create(BaseModel):
	rocket: str
	provider: str
	launch_time: datetime
	status: str
	is_crewed: bool
	webcast_url: str

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

@app.get("/launches/{launch_id}")
def get_launches_by_id(launch_id: int) -> dict:

	with psycopg.connect(DB_CONNECTION, row_factory = dict_row) as conn:
		row = conn.execute(
			"SELECT * FROM launches WHERE id = %s", (launch_id,)
		).fetchall()

	if len(row) > 0: return row[0]
	else: return {"status": "FAILED"}

@app.post("/launches/create")
def create_launch(payload: launch_create) -> dict:

	with psycopg.connect(DB_CONNECTION, row_factory = dict_row) as conn:
		launch = conn.execute(
			"INSERT INTO launches (rocket, provider, launch_time, status, is_crewed, webcast_url) VALUES (%(rocket)s, %(provider)s, %(launch_time)s, %(status)s, %(is_crewed)s, %(webcast_url)s) RETURNING *",
			{
				"rocket":  payload.rocket,
				"provider": payload.provider,
				"launch_time": payload.launch_time,
				"status": payload.status,
				"is_crewed": payload.is_crewed,
				"webcast_url": payload.webcast_url
			}
		).fetchone()

		conn.commit()

	broadcaster.publish(launch)

	return launch

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

@app.delete("/launches/delete/{launch_id}")
def delete_launch(launch_id: int) -> dict:

	with psycopg.connect(DB_CONNECTION, row_factory = dict_row) as conn:
		conn.execute(
			"DELETE FROM launches WHERE id = %s", (launch_id,)
		)

	return {"status": "SUCCESS"}