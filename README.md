# Launchpulse

Launchpulse is an API endpoint that provides data about rocket & related subjects.

## How to start

Launchpulse uses Docker.

'docker compose up' to start the application.

## Endpoints

Endpoints are being changed constantly.

/health : Check if the application is running

/launches : Get a list of all launches currently stored in the database

/launches/{id} : Get data about a specific launch with given id

/launches/create : Create a new launch

/launches/update : Updates a launch

/launches/delete : Deletes a launch

/alerts/stream : Get live updates about any new launches being created. Works with SSE

## Future updates

Currently working on expanding the database to include more information. Updates on endpoints will follow soon.

Github actions are currently failing because the endpoints are not yet updated to the new schema.