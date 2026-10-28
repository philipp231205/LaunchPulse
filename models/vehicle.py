from datetime import datetime
from pydantic import BaseModel

class vehicle(BaseModel):
	id: int | None = None
	name: str
	family: str | None = None
	height_m: float | None = None
	diameter_m: float | None = None
	mass_kg: int | None = None
	payload_leo_kg: int | None = None
	payload_gto_kg: int | None = None
	payload_sso_kg: int | None = None
	stages: int | None = None
	first_flight: datetime | None = None
	thrust_kn: float | None = None
	status: str | None = None
	organisation_id: int | None = None