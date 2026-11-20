from fastapi import APIRouter, HTTPException
from typing import Optional
from datetime import datetime

from models.launch import launch
from app.broadcaster import broadcaster
from app.db import get_conn, ForeignKeyViolation

router = APIRouter(prefix="/launches", tags=["launches"])


# Gets all rows in launches table
@router.get("")
def get_launches(
	status: Optional[str] = None,
	organisation_id: Optional[int] = None,
	launchpad_id: Optional[int] = None,
	vehicle_id: Optional[int] = None,
	from_date: Optional[datetime] = None,
	to_date: Optional[datetime] = None,
	limit: Optional[int] = 50,
	offset: Optional[int] = 0,
) -> dict:

	conditions = []
	params = {"limit": limit, "offset": offset}

	if status is not None:
		conditions.append("status = %(status)s")
		params["status"] = status
	if organisation_id is not None:
		conditions.append("organisation_id = %(organisation_id)s")
		params["organisation_id"] = organisation_id
	if launchpad_id is not None:
		conditions.append("launchpad_id = %(launchpad_id)s")
		params["launchpad_id"] = launchpad_id
	if vehicle_id is not None:
		conditions.append("vehicle_id = %(vehicle_id)s")
		params["vehicle_id"] = vehicle_id
	if from_date is not None:
		conditions.append("date >= %(from_date)s")
		params["from_date"] = from_date
	if to_date is not None:
		conditions.append("date <= %(to_date)s")
		params["to_date"] = to_date

	where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
	sql = f"SELECT * FROM launches {where} ORDER BY date LIMIT %(limit)s OFFSET %(offset)s"

	with get_conn() as conn:
		rows = conn.execute(sql, params).fetchall()

	return {row["id"]: row for row in rows}


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
				"UPDATE launches SET date = %(date)s, status = %(status)s, webcast_url = %(webcast_url)s, mission = %(mission)s, payload = %(payload)s, vehicle_id = %(vehicle_id)s, launchpad_id = %(launchpad_id)s, organisation_id = %(organisation_id)s WHERE id = %(id)s RETURNING *",
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

		return cur.fetchone()

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
		raise HTTPException(status_code=404, detail="launch not found")
	return