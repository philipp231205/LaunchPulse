from fastapi import APIRouter, Response, status

from models.launchpad import launchpad

import os
from dotenv import load_dotenv
load_dotenv()

DB_CONNECTION = os.getenv("DATABASE_URL")

import psycopg
from psycopg.rows import dict_row

router = APIRouter(prefix="/launchpads", tags=["launchpads"])


# Gets all rows in launchpads table
@router.get("")
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


# Gets row by id for launchpads
@router.get("/{id}")
def get_launchpads_by_id(id: int, response: Response) -> dict:

	try:
		with psycopg.connect(DB_CONNECTION, row_factory = dict_row) as conn:
			row = conn.execute(
				"SELECT * FROM launchpads WHERE id = %s", (id,)
			).fetchall()

		response.status_code = status.HTTP_200_OK
		return row[0]

	except Exception:
		response.status_code = status.HTTP_404_NOT_FOUND
		return


# Creates a new launchpad
@router.post("")
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

		#broadcaster.publish(launchpad)

		response.status_code = status.HTTP_201_CREATED
		return launchpad

	except Exception:
		response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return


# Update launchpad by id
@router.put("")
def update_launchpad(payload: launchpad, response: Response):
	try:
		with psycopg.connect(DB_CONNECTION, row_factory = dict_row) as conn:
			conn.execute(
				"UPDATE launchpads SET name = %(name)s, longitude = %(longitude)s, latitude = %(latitude)s, status = %(status)s, organisation_id = %(organisation_id)s, location_id = %(location_id)s WHERE id = %(id)s",
				{
					"name": payload.name,
					"longitude": payload.longitude,
					"latitude": payload.latitude,
					"status": payload.status,
					"organisation_id": payload.organisation_id,
					"location_id": payload.location_id,
					"id": payload.id
				}
			)

		response.status_code = status.HTTP_200_OK
		return

	except Exception:
		response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return


# Deletes launchpad by id
@router.delete("/{id}")
def delete_launchpad(id: int, response: Response):

	try:
		with psycopg.connect(DB_CONNECTION, row_factory = dict_row) as conn:
			conn.execute(
				"DELETE FROM launchpads WHERE id = %s", (id,)
			)

		response.status_code = status.HTTP_204_NO_CONTENT
		return

	except Exception:
		response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return