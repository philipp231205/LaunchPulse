from fastapi import FastAPI, Response, status

from app.broadcaster import broadcaster

app = FastAPI(title="LaunchPulse", version="1.0.0")

from fastapi.staticfiles import StaticFiles
from app.routes import alerts

app.include_router(alerts.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

from app.routes import organisations, locations, launchpads, vehicles, launches

app.include_router(organisations.router)
app.include_router(locations.router)
app.include_router(launchpads.router)
app.include_router(vehicles.router)
app.include_router(launches.router)


# Endpoint to check the health of the API
@app.get("/health")
def get_health(response: Response):
	response.status_code = status.HTTP_200_OK
	return