from fastapi import APIRouter, HTTPException

from models.launch import launch
from app.broadcaster import broadcaster
from app.db import get_conn, ForeignKeyViolation

router = APIRouter(prefix="/launches", tags=["launches"])


# Gets all rows in launches table
@router.get("")
def get_launches() -> dict:

	with get_conn() as conn:
		rows = conn.execute(
			"SELECT * FROM launches ORDER BY date"
		).fetchall()

	result = {row["id"]: row for row in rows}

	return result


# Gets row by id for launches
@router.get("/{id}")
def get_launches_by_id(id: int) -> dict:

	with get_conn() as conn:
		row = conn.execute(
			"SELECT * FROM launches WHERE id = %s", (id,)
		).fetchone()

	if row is None:
		raise HTTPException(status_code=404, detail="launch not found")

	return row


# Creates a new launch
@router.post("", status_code=201)
def create_launch(payload: launch) -> dict:

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

		return launch

	except ForeignKeyViolation:
		raise HTTPException(status_code=404, detail="vehicle, launchpad or organisation not found")


# Update launch by id
@router.put("/{id}")
def update_launch(id: int, payload: launch):

	try:
		with get_conn() as conn:
			cur = conn.execute(
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

		if cur.rowcount == 0:
			raise HTTPException(status_code=404, detail="launch not found")

		return

	except ForeignKeyViolation:
		raise HTTPException(status_code=404, detail="vehicle, launchpad or organisation not found")

# Deletes launch by id
@router.delete("/{id}", status_code=204)
def delete_launch(id: int):

	with get_conn() as conn:
		cur = conn.execute(
			"DELETE FROM launches WHERE id = %s", (id,)
		)

	if cur.rowcount == 0:
		raise HTTPException(status_code=404, detail="launches not found")
	return