from fastapi import APIRouter, Response, status

from models.vehicle import vehicle
from app import broadcaster
from app.db import get_conn

router = APIRouter(prefix="/vehicles", tags=["vehicles"])

# Gets all rows in vehicles table
@router.get("")
def get_vehicles(response: Response) -> dict:

	try:
		with get_conn() as conn:
			rows = conn.execute(
				"SELECT * FROM vehicles ORDER BY name"
			).fetchall()

		result = {row["id"]: row for row in rows}

		response.status_code = status.HTTP_200_OK
		return result

	except Exception:
		response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return


# Gets row by id for vehicles
@router.get("/{id}")
def get_vehicles_by_id(id: int, response: Response) -> dict:

	try:
		with get_conn() as conn:
			row = conn.execute(
				"SELECT * FROM vehicles WHERE id = %s", (id,)
			).fetchall()

		response.status_code = status.HTTP_200_OK
		return row[0]

	except Exception:
		response.status_code = status.HTTP_404_NOT_FOUND
		return


# Creates a new vehicle
@router.post("")
def create_vehicle(payload: vehicle, response: Response) -> dict:

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

		response.status_code = status.HTTP_201_CREATED
		return vehicle

	except Exception:
		response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return


# Update vehicle by id
@router.put("")
def update_vehicle(payload: vehicle, response: Response):
	try:
		with get_conn() as conn:
			conn.execute(
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
					"id": payload.id
				}
			)

		response.status_code = status.HTTP_200_OK
		return

	except Exception:
		response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return


# Deletes vehicle by id
@router.delete("/{id}")
def delete_vehicle(id: int, response: Response):

	try:
		with get_conn() as conn:
			conn.execute(
				"DELETE FROM vehicles WHERE id = %s", (id,)
			)

		response.status_code = status.HTTP_204_NO_CONTENT
		return

	except Exception:
		response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return