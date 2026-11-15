from fastapi import APIRouter, Response, status, HTTPException

from models.organisation import organisation
from app.broadcaster import broadcaster
from app.db import get_conn

router = APIRouter(prefix="/organisations", tags=["organisations"])

# Gets all rows in organisations table
@router.get("")
def get_organisations(response: Response) -> dict:

	try:
		with get_conn() as conn:
			rows = conn.execute(
				"SELECT * FROM organisations ORDER BY name"
			).fetchall()

		result = {row["id"]: row for row in rows}

		response.status_code = status.HTTP_200_OK
		return result

	except Exception:
		response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return


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
@router.post("")
def create_organisation(payload: organisation, response: Response) -> dict:

	try:
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

		response.status_code = status.HTTP_201_CREATED
		return organisation

	except Exception:
		response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return


# Update organisation by id
@router.put("/{id}")
def update_organisation(id: int, payload: organisation, response: Response):

	try:
		with get_conn() as conn:
			conn.execute(
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

		response.status_code = status.HTTP_200_OK
		return

	except Exception:
		response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return


# Deletes organisation by id
@router.delete("/{id}")
def delete_organisation(id: int, response: Response):

	try:
		with get_conn() as conn:
			conn.execute(
				"DELETE FROM organisations WHERE id = %s", (id,)
			)

		response.status_code = status.HTTP_204_NO_CONTENT
		return

	except Exception:
		response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return