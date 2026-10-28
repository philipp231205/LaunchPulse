from datetime import datetime
from pydantic import BaseModel

class launch(BaseModel):
	date: datetime
	status: str | None = None
	webcast_url: str | None = None
	mission: str
	payload: str | None = None
	vehicle_id: int
	launchpad_id: int
	organisation_id: int