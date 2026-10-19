from collections.abc import AsyncIterable

from fastapi import APIRouter
from fastapi.sse import EventSourceResponse, ServerSentEvent

from app.broadcaster import broadcaster

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.get("/stream", response_class=EventSourceResponse)
async def alert_stream() -> AsyncIterable[ServerSentEvent]:
	client = broadcaster.subscribe()
	queue, _loop = client

	try:
		yield ServerSentEvent(comment="connected to LaunchPulse alerts")
		while True:
			event = await queue.get() # waits without blocking anyone else
			yield ServerSentEvent(
				data=event,
				event="launch_created",
				id=str(event["id"]),
			)

	finally:
		# Runs when the client disconnects
		broadcaster.unsubscribe(client)