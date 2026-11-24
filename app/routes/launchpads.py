from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from models.launchpad import launchpad
from app.broadcaster import broadcaster
from app.db import get_conn, ForeignKeyViolation

router = APIRouter(prefix="/launchpads", tags=["launchpads"])


# Gets all rows in launchpads table
@router.get("")
def get_launchpads(
	organisation_id: Optional[int] = None,
	location_id: Optional[int] = None,
	status: Optional[str] = None,
	limit: int = Query(50, ge=1, le=200),
	offset: int = Query(0, ge=0),
) -> dict:

	conditions = []
	params = {"limit": limit, "offset": offset}

	if organisation_id is not None:
		conditions.append("organisation_id = %(organisation_id)s")
		params["organisation_id"] = organisation_id
	if location_id is not None:
		conditions.append("location_id = %(location_id)s")
		params["location_id"] = location_id
	if status is not None:
		conditions.append("status = %(status)s")
		params["status"] = status

	where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
	sql = f"SELECT * FROM launchpads {where} ORDER BY name LIMIT %(limit)s OFFSET %(offset)s"

	with get_conn() as conn:
		rows = conn.execute(sql, params).fetchall()

	return {row["id"]: row for row in rows}


# Gets row by id for launchpads
@router.get("/{id}")
def get_launchpads_by_id(id: int) -> dict:

	with get_conn() as conn:
		row = conn.execute(
			"SELECT * FROM launchpads WHERE id = %s", (id,)
		).fetchone()

	if row is None:
		raise HTTPException(status_code=404, detail="launchpad not found")

	return row


# Creates a new launchpad
@router.post("", status_code=201)
def create_launchpad(payload: launchpad) -> dict:

	try:
		with get_conn() as conn:
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

		return launchpad

	except ForeignKeyViolation:
		raise HTTPException(status_code=404, detail="organisation or location not found")


# Update launchpad by id
@router.put("/{id}")
def update_launchpad(id: int, payload: launchpad):
	try:
		with get_conn() as conn:
			cur = conn.execute(
				"UPDATE launchpads SET name = %(name)s, longitude = %(longitude)s, latitude = %(latitude)s, status = %(status)s, organisation_id = %(organisation_id)s, location_id = %(location_id)s WHERE id = %(id)s RETURNING *",
				{
					"name": payload.name,
					"longitude": payload.longitude,
					"latitude": payload.latitude,
					"status": payload.status,
					"organisation_id": payload.organisation_id,
					"location_id": payload.location_id,
					"id": id
				}
			)

		if cur.rowcount == 0:
			raise HTTPException(status_code=404, detail="launchpad not found")

		return cur.fetchone()

	except ForeignKeyViolation:
		raise HTTPException(status_code=404, detail="organisation or location not found")


# Deletes launchpad by id
@router.delete("/{id}", status_code=204)
def delete_launchpad(id: int):

	try:
		with get_conn() as conn:
			cur = conn.execute(
				"DELETE FROM launchpads WHERE id = %s", (id,)
			)

		if cur.rowcount == 0:
			raise HTTPException(status_code=404, detail="launchpad not found")
		
		return

	except ForeignKeyViolation:
		raise HTTPException(status_code=409, detail="launchpad still referenced")