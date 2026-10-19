import asyncio
from typing import Any

class Broadcaster:
	"""Keeps one queue per connected client and copies each event into all of them"""

	def __init__(self) -> None:
		self._clients: set[tuple[asyncio.Queue, asyncio.AbstractEventLoop]] = set()

	def subscribe(self) -> tuple[asyncio.Queue, asyncio.AbstractEventLoop]:
		client = (asyncio.Queue(maxsize=100), asyncio.get_running_loop())
		self._clients.add(client)
		return client

	def unsubscribe(
			self, client: tuple[asyncio.Queue, asyncio.AbstractEventLoop]
	) -> None:
		self._clients.discard(client)

	def publish(self, event: dict[str, Any]) -> None:
		# Safe to call from a plain def endpoint (worker thread).

		for queue, loop in list(self._clients):
			loop.call_soon_threadsafe(self._put, queue, event)

	@staticmethod
	def _put(queue: asyncio.Queue, event: dict[str, Any]) -> None:
		if not queue.full(): # a stuck client must not block everyone else
			queue.put_nowait(event)

broadcaster = Broadcaster()