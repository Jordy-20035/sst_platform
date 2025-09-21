from typing import Tuple
import asyncio
import json
from typing import Dict

# Each connected client gets a Queue to receive messages
class Broadcaster:
    def __init__(self):
        self._clients: Dict[int, asyncio.Queue] = {}
        self._next_id = 0
        self._lock = asyncio.Lock()

    async def register(self) -> Tuple[int, asyncio.Queue]:
        async with self._lock:
            client_id = self._next_id
            self._next_id += 1
            q: asyncio.Queue = asyncio.Queue()
            self._clients[client_id] = q
            return client_id, q

    async def unregister(self, client_id: int):
        async with self._lock:
            if client_id in self._clients:
                del self._clients[client_id]

    async def publish(self, event: dict):
        payload = json.dumps(event)
        # do not await inside lock for long time; snapshot clients
        async with self._lock:
            clients = list(self._clients.items())
        for client_id, q in clients:
            try:
                q.put_nowait(payload)
            except asyncio.QueueFull:
                # skip slow clients
                pass


broadcaster = Broadcaster()
