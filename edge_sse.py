"""Start BE1 and BE2 first, then run this file to send a message."""

import os

import httpx

BE1_URL = os.getenv("BE1_URL", "http://127.0.0.1:8001")


if __name__ == "__main__":
    response = httpx.post(
        f"{BE1_URL}/publish",
        json={"message": "Hello BE2, this message is from edge_sse.py!"},
    )
    response.raise_for_status()
    assert response.json() == {"queued": True}
    print("BE1 accepted the message. Check the BE2 terminal for SSE delivery.")
