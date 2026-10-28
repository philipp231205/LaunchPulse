from pydantic import BaseModel

class organisation(BaseModel):
	name: str
	country: str | None = None
	type: str | None = None
	administrator: str | None = None
	website: str | None = None