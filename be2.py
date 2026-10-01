import asyncio
import os
from contextlib import asynccontextmanager, suppress

import httpx
from fastapi import FastAPI

BE1_URL = os.getenv("BE1_URL", "http://127.0.0.1:8001")


async def subscribe():
    # BE1 sends a ping every 15s to keep the connection alive when idle.
    async with httpx.AsyncClient(timeout=httpx.Timeout(5, read=45)) as client:
        while True:
            try:
                async with client.stream("GET", f"{BE1_URL}/events") as response:
                    async for line in response.aiter_lines():
                        if line.startswith("data:"):
                            print("BE2 received:", line, flush=True)
            except (httpx.HTTPError, ValueError) as exc:
                print("SSE error, retrying in 2s:", exc, flush=True)
            await asyncio.sleep(2)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(subscribe())
    try:
        yield
    finally:
        task.cancel()
        with suppress(asyncio.CancelledError):
            await task


app = FastAPI(title="BE2 - SSE Subscriber", lifespan=lifespan)
