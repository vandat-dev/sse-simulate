# edge_sse.py -> BE1 -> SSE -> BE2

Install dependencies: `.venv/bin/python -m pip install -r requirements.txt`.

Open three terminals in the project directory:

```bash
# Terminal 1: BE1 accepts POST requests and publishes SSE messages
.venv/bin/python -m uvicorn be1:app --port 8001

# Terminal 2: BE2 subscribes to BE1's GET /events and keeps the connection open
.venv/bin/python -m uvicorn be2:app --port 8002

# Terminal 3: send a message to BE1
.venv/bin/python edge_sse.py
```

The BE2 terminal will print:

```text
BE2 received: data: {"message":"Hello BE2, this message is from edge_sse.py!"}
```

Edit `message` in `edge_sse.py` to change the content. Each run sends one message.
You can also use `POST /publish` at <http://127.0.0.1:8001/docs>.

Start BE1 with the command above, then open `events.html` directly in your browser.
The HTML connects to `http://127.0.0.1:8001/events`. If BE1 is already running, restart it to load the CORS configuration.
BE1 uses [CORSMiddleware](https://fastapi.tiangolo.com/tutorial/cors/) to allow any origin without credentials for this local demo. Restrict origins when deploying.
BE2 is unchanged, and no extra entry point is needed.
The page uses the browser's [EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) to listen directly to BE1 and display the latest 100 messages as text. It does not connect to BE2.
BE1 has one shared queue: the browser and BE2 compete for messages if both connect. Stop BE2 if you want the browser to receive every message.

BE1 uses an in-memory queue with a maximum of 100 messages, for one BE2. Run each service with one worker.
`queued: true` only confirms that BE1 queued the message; check BE2's logs to confirm receipt.
BE2 reconnects after two seconds if the connection drops. Messages are not persisted or replayed if missed.
Close the browser page and stop BE2 before BE1 to close the streams promptly.
If you change BE1's port, set `BE1_URL=http://127.0.0.1:PORT` when running BE2 and the sender script.
