from fastapi import FastAPI
import os
from dotenv import load_dotenv

import psycopg
from psycopg.rows import dict_row

app = FastAPI()

load_dotenv()

DB_CONNECTION = os.getenv("DATABASE_URL")

from datetime import datetime
from typing import Literal

from pydantic import BaseModel

Status = Literal["upcoming", "launched", "scrubbed", "failed"]

class launch_create(BaseModel):
	rocket: str
	provider: str
	launch_time: datetime
	status: Status = "upcoming"
	is_crewed: bool
	webcast_url: str

class launch_update(BaseModel):
	id: int
	rocket: str
	provider: str
	launch_time: datetime
	status: str
	is_crewed: bool
	webcast_url: str


@app.get("/health")
def get_health() -> dict[str, str]:
	return {"status": "UP"}

@app.get("/launches")
def get_launches() -> dict:

	with psycopg.connect(DB_CONNECTION, row_factory = dict_row) as conn:
		rows = conn.execute(
			"SELECT * FROM launches ORDER BY launch_time"
		).fetchall()

	result = {row["id"]: row for row in rows}

	return result

@app.get("/launches/{launch_id}")
def get_launches_by_id(launch_id: int) -> dict:

	with psycopg.connect(DB_CONNECTION, row_factory = dict_row) as conn:
		row = conn.execute(
			"SELECT * FROM launches WHERE id = %s", (launch_id,)
		).fetchall()

	if len(row) > 0: return row[0]
	else: return {"status": "FAILED"}

@app.post("/launches/create")
def create_launch(payload: launch_create) -> dict:

	with psycopg.connect(DB_CONNECTION, row_factory = dict_row) as conn:
		conn.execute(
			"INSERT INTO launches (rocket, provider, launch_time, status, is_crewed, webcast_url) VALUES (%(rocket)s, %(provider)s, %(launch_time)s, %(status)s, %(is_crewed)s, %(webcast_url)s)",
			{
				"rocket":  payload.rocket,
				"provider": payload.provider,
				"launch_time": payload.launch_time,
				"status": payload.status,
				"is_crewed": payload.is_crewed,
				"webcast_url": payload.webcast_url
			}
		)

	return payload

@app.put("/launches/update")
def update_launch(payload: launch_update) -> dict:

	with psycopg.connect(DB_CONNECTION, row_factory = dict_row) as conn:
		conn.execute(
			"UPDATE launches SET rocket = %(rocket)s, provider = %(provider)s, launch_time = %(launch_time)s, status = %(status)s, is_crewed = %(is_crewed)s, webcast_url = %(webcast_url)s WHERE id = %(id)s",
			{
				"rocket":  payload.rocket,
				"provider": payload.provider,
				"launch_time": payload.launch_time,
				"status": payload.status,
				"is_crewed": payload.is_crewed,
				"webcast_url": payload.webcast_url,
				"id": payload.id
			}
		)

	return payload

@app.delete("/launches/delete/{launch_id}")
def delete_launch(launch_id: int) -> dict:

	with psycopg.connect(DB_CONNECTION, row_factory = dict_row) as conn:
		conn.execute(
			"DELETE FROM launches WHERE id = %s", (launch_id,)
		)

	return {"status": "SUCCESS"}