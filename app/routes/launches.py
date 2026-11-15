from fastapi import APIRouter, Response, status

from models.launch import launch
from app import broadcaster
from app.db import get_conn

router = APIRouter(prefix="/launches", tags=["launches"])


# Gets all rows in launches table
@router.get("")
def get_launches(response: Response) -> dict:

	try:
		with get_conn() as conn:
			rows = conn.execute(
				"SELECT * FROM launches ORDER BY date"
			).fetchall()

		result = {row["id"]: row for row in rows}

		response.status_code = status.HTTP_200_OK
		return result

	except Exception:
		response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return


# Gets row by id for launches
@router.get("/{id}")
def get_launches_by_id(id: int, response: Response) -> dict:

	try:
		with get_conn() as conn:
			row = conn.execute(
				"SELECT * FROM launches WHERE id = %s", (id,)
			).fetchall()

		response.status_code = status.HTTP_200_OK
		return row[0]

	except Exception:
		response.status_code = status.HTTP_404_NOT_FOUND
		return


# Creates a new launch
@router.post("")
def create_launch(payload: launch, response: Response) -> dict:

	try:
		with get_conn() as conn:
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


# Update launch by id
@router.put("/{id}")
def update_launch(id: int, payload: launch, response: Response):

	try:
		with get_conn() as conn:
			conn.execute(
				"UPDATE launches SET date = %(date)s, status = %(status)s, webcast_url = %(webcast_url)s, mission = %(mission)s, payload = %(payload)s, vehicle_id = %(vehicle_id)s, launchpad_id = %(launchpad_id)s, organisation_id = %(organisation_id)s WHERE id = %(id)s",
				{
					"date": payload.date,
					"status": payload.status,
					"webcast_url": payload.webcast_url,
					"mission": payload.mission,
					"payload": payload.payload,
					"vehicle_id": payload.vehicle_id,
					"launchpad_id": payload.launchpad_id,
					"organisation_id": payload.organisation_id,
					"id": id
				}
			)

		response.status_code = status.HTTP_200_OK
		return

	except Exception:
		response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return


# Deletes launch by id
@router.delete("/{id}")
def delete_launch(id: int, response: Response):

	try:
		with get_conn() as conn:
			conn.execute(
				"DELETE FROM launches WHERE id = %s", (id,)
			)

		response.status_code = status.HTTP_204_NO_CONTENT
		return

	except Exception:
		response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return