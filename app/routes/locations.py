from fastapi import APIRouter, Response, status

from models.location import location

import os
from dotenv import load_dotenv
load_dotenv()

DB_CONNECTION = os.getenv("DATABASE_URL")

import psycopg
from psycopg.rows import dict_row

router = APIRouter(prefix="/locations", tags=["locations"])


# Gets all rows in locations table
@router.get("")
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


# Gets row by id for locations
@router.get("/{id}")
def get_locations_by_id(id: int, response: Response) -> dict:

	try:
		with psycopg.connect(DB_CONNECTION, row_factory = dict_row) as conn:
			row = conn.execute(
				"SELECT * FROM locations WHERE id = %s", (id,)
			).fetchall()

		response.status_code = status.HTTP_200_OK
		return row[0]

	except Exception:
		response.status_code = status.HTTP_404_NOT_FOUND
		return


# Creates a new location
@router.post("")
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

		#broadcaster.publish(location)

		response.status_code = status.HTTP_201_CREATED
		return location

	except Exception:
		response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return

# Update location by id
@router.put("")
def update_location(payload: location, response: Response):

	try:
		with psycopg.connect(DB_CONNECTION, row_factory = dict_row) as conn:
			conn.execute(
				"UPDATE locations SET name = %(name)s, country = %(country)s, region = %(region)s WHERE id = %(id)s",
				{
					"name": payload.name,
					"country": payload.country,
					"region": payload.region,
					"id": payload.id
				}
			)

		response.status_code = status.HTTP_200_OK
		return

	except Exception:
		response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return

# Deletes location by id
@router.delete("/{id}")
def delete_location(id: int, response: Response):

	try:
		with psycopg.connect(DB_CONNECTION, row_factory = dict_row) as conn:
			conn.execute(
				"DELETE FROM locations WHERE id = %s", (id,)
			)

		response.status_code = status.HTTP_204_NO_CONTENT
		return

	except Exception:
		response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return