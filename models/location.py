from pydantic import BaseModel

class location(BaseModel):
	name: str
	country: str | None = None
	region: str | None = None