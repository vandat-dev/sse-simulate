import asyncio

from fastapi import Body, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.sse import EventSourceResponse

app = FastAPI(title="BE1 - SSE Publisher")
# ponytail: any origin for this local demo; restrict origins when deploying.
app.add_middleware(CORSMiddleware, allow_origins=["*"])
messages = asyncio.Queue(maxsize=100)


@app.get("/events", response_class=EventSourceResponse)
async def events():
    while True:
        message = await messages.get()
        print("BE1 sending SSE:", message, flush=True)
        yield message


@app.post("/publish")
async def publish(message: str = Body(embed=True, min_length=1, max_length=10_000)):
    try:
        messages.put_nowait({"message": message})
    except asyncio.QueueFull:
        raise HTTPException(503, "Queue is full. Please try again later.")
    print("BE1 received POST:", message, flush=True)
    return {"queued": True}
