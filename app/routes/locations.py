from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from models.location import location
from app.broadcaster import broadcaster
from app.db import get_conn, ForeignKeyViolation

router = APIRouter(prefix="/locations", tags=["locations"])


# Gets all rows in locations table
@router.get("")
def get_locations(
	country: Optional[str] = None,
	limit: int = Query(50, ge=1, le=200),
	offset: int = Query(0, ge=0),
) -> dict:

	conditions = []
	params = {"limit": limit, "offset": offset}

	if country is not None:
		conditions.append("country = %(country)s")
		params["country"] = country

	where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
	sql = f"SELECT * FROM locations {where} ORDER BY name LIMIT %(limit)s OFFSET %(offset)s"

	with get_conn() as conn:
		rows = conn.execute(sql, params).fetchall()

	return {row["id"]: row for row in rows}


# Gets row by id for locations
@router.get("/{id}")
def get_locations_by_id(id: int) -> dict:

	with get_conn() as conn:
		row = conn.execute(
			"SELECT * FROM locations WHERE id = %s", (id,)
		).fetchone()

	if row is None:
		raise HTTPException(status_code=404, detail="location not found")

	return row


# Creates a new location
@router.post("", status_code=201)
def create_location(payload: location) -> dict:

	with get_conn() as conn:
		location = conn.execute(
			"INSERT INTO locations (name, country, region) VALUES (%(name)s, %(country)s, %(region)s) RETURNING *",
			{
				"name": payload.name,
				"country": payload.country,
				"region": payload.region
			}
		).fetchone()

		conn.commit()

	return location

# Update location by id
@router.put("/{id}")
def update_location(id: int, payload: location):

	with get_conn() as conn:
		cur = conn.execute(
			"UPDATE locations SET name = %(name)s, country = %(country)s, region = %(region)s WHERE id = %(id)s RETURNING *",
			{
				"name": payload.name,
				"country": payload.country,
				"region": payload.region,
				"id": id
			}
		)

	if cur.rowcount == 0:
		raise HTTPException(status_code=404, detail="location not found")

	return cur.fetchone()

# Deletes location by id
@router.delete("/{id}", status_code=204)
def delete_location(id: int):

	try:
		with get_conn() as conn:
			cur = conn.execute(
				"DELETE FROM locations WHERE id = %s", (id,)
			)

		if cur.rowcount == 0:
			raise HTTPException(status_code=404, detail="location not found")
		
		return

	except ForeignKeyViolation:
		raise HTTPException(status_code=409, detail="location still referenced")