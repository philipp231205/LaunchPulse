from pydantic import BaseModel

class launchpad(BaseModel):
	id: int | None = None
	name: str
	longitude: float
	latitude: float
	status: str | None = None
	organisation_id: int
	location_id: int