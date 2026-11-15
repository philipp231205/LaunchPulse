from fastapi import APIRouter, HTTPException

from models.vehicle import vehicle
from app.broadcaster import broadcaster
from app.db import get_conn, ForeignKeyViolation

router = APIRouter(prefix="/vehicles", tags=["vehicles"])

# Gets all rows in vehicles table
@router.get("")
def get_vehicles() -> dict:

	with get_conn() as conn:
		rows = conn.execute(
			"SELECT * FROM vehicles ORDER BY name"
		).fetchall()

	result = {row["id"]: row for row in rows}

	return result


# Gets row by id for vehicles
@router.get("/{id}")
def get_vehicles_by_id(id: int) -> dict:

	with get_conn() as conn:
		row = conn.execute(
			"SELECT * FROM vehicles WHERE id = %s", (id,)
		).fetchone()

	if row is None:
		raise HTTPException(status_code=404, detail="vehicle not found")

	return row


# Creates a new vehicle
@router.post("", status_code=201)
def create_vehicle(payload: vehicle) -> dict:

	try:
		with get_conn() as conn:
			vehicle = conn.execute(
				"INSERT INTO vehicles (name, family, height_m, diameter_m, mass_kg, payload_leo_kg, payload_gto_kg, payload_sso_kg, stages, first_flight, thrust_kn, status, organisation_id) VALUES (%(name)s, %(family)s, %(height_m)s, %(diameter_m)s, %(mass_kg)s, %(payload_leo_kg)s, %(payload_gto_kg)s, %(payload_sso_kg)s, %(stages)s, %(first_flight)s, %(thrust_kn)s, %(status)s, %(organisation_id)s) RETURNING *",
				{
					"name": payload.name,
					"family": payload.family,
					"height_m": payload.height_m,
					"diameter_m": payload.diameter_m,
					"mass_kg": payload.mass_kg,
					"payload_leo_kg": payload.payload_leo_kg,
					"payload_gto_kg": payload.payload_gto_kg,
					"payload_sso_kg": payload.payload_sso_kg,
					"stages": payload.stages,
					"first_flight": payload.first_flight,
					"thrust_kn": payload.thrust_kn,
					"status": payload.status,
					"organisation_id": payload.organisation_id
				}
			).fetchone()

			conn.commit()

		broadcaster.publish(vehicle)

		return vehicle

	except ForeignKeyViolation:
		raise HTTPException(status_code=404, detail="organisation not found")


# Update vehicle by id
@router.put("/{id}")
def update_vehicle(id: int, payload: vehicle):
	try:
		with get_conn() as conn:
			cur = conn.execute(
				"UPDATE vehicles SET name = %(name)s, family = %(family)s, height_m = %(height_m)s, diameter_m = %(diameter_m)s, mass_kg = %(mass_kg)s, payload_leo_kg = %(payload_leo_kg)s, payload_gto_kg = %(payload_gto_kg)s, payload_sso_kg = %(payload_sso_kg)s, stages = %(stages)s, first_flight = %(first_flight)s, thrust_kn = %(thrust_kn)s, status = %(status)s, organisation_id = %(organisation_id)s WHERE id = %(id)s",
				{
					"name": payload.name,
					"family": payload.family,
					"height_m": payload.height_m,
					"diameter_m": payload.diameter_m,
					"mass_kg": payload.mass_kg,
					"payload_leo_kg": payload.payload_leo_kg,
					"payload_gto_kg": payload.payload_gto_kg,
					"payload_sso_kg": payload.payload_sso_kg,
					"stages": payload.stages,
					"first_flight": payload.first_flight,
					"thrust_kn": payload.thrust_kn,
					"status": payload.status,
					"organisation_id": payload.organisation_id,
					"id": id
				}
			)

		if cur.rowcount == 0:
			raise HTTPException(status_code=404, detail="vehicle not found")

		return

	except ForeignKeyViolation:
		raise HTTPException(status_code=404, detail="organisation not found")


# Deletes vehicle by id
@router.delete("/{id}", status_code=204)
def delete_vehicle(id: int):

	with get_conn() as conn:
		cur = conn.execute(
			"DELETE FROM vehicles WHERE id = %s", (id,)
		)

	if cur.rowcount == 0:
		raise HTTPException(status_code=404, detail="vehicle not found")
	
	return