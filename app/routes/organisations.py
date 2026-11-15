from fastapi import APIRouter, HTTPException

from models.organisation import organisation
from app.broadcaster import broadcaster
from app.db import get_conn

router = APIRouter(prefix="/organisations", tags=["organisations"])

# Gets all rows in organisations table
@router.get("")
def get_organisations() -> dict:

	with get_conn() as conn:
		rows = conn.execute(
			"SELECT * FROM organisations ORDER BY name"
		).fetchall()

	result = {row["id"]: row for row in rows}

	return result


# Gets row by id for organisations
@router.get("/{id}")
def get_organisations_by_id(id: int) -> dict:

	with get_conn() as conn:
		row = conn.execute(
			"SELECT * FROM organisations WHERE id = %s", (id,)
		).fetchone()

	if row is None:
		raise HTTPException(status_code=404, detail="organisation not found")

	return row


# Creates a new organisation
@router.post("", status_code=201)
def create_organisation(payload: organisation) -> dict:

	with get_conn() as conn:
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

	return organisation


# Update organisation by id
@router.put("/{id}")
def update_organisation(id: int, payload: organisation):

	with get_conn() as conn:
		cur = conn.execute(
			"UPDATE organisations SET name = %(name)s, country = %(country)s, type = %(type)s, administrator = %(administrator)s, website = %(website)s WHERE id = %(id)s",
			{
				"name": payload.name,
				"country": payload.country,
				"type": payload.type,
				"administrator": payload.administrator,
				"website": payload.website,
				"id": id
			}
		)

	if cur.rowcount == 0:
		raise HTTPException(status_code=404, detail="organisation not found")

	return


# Deletes organisation by id
@router.delete("/{id}", status_code=204)
def delete_organisation(id: int):

	with get_conn() as conn:
		cur = conn.execute(
			"DELETE FROM organisations WHERE id = %s", (id,)
		)

	if cur.rowcount == 0:
		raise HTTPException(status_code=404, detail="organisation not found")

	return