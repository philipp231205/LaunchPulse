from pydantic import BaseModel

class location(BaseModel):
	id: int | None = None
	name: str
	country: str | None = None
	region: str | None = None