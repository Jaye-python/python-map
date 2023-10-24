from __future__ import absolute_import, unicode_literals
from celery import shared_task
import websocket
import json
import websocket

ws = websocket.WebSocket()
websocket_url = "ws://localhost:8000/ws/livesignals/"

# HERE I SEND TEST LIVE MESSAGE TO THE ENDPOINT USING CELERY
websocket_url = "ws://localhost:8000/ws/livesignals/"

payload = {
    "message": {
        "temperature": 0.7,
        "pressure": 0.3,
        "steam_injection": 0.3,
        "sensor_id": 8
    }
}

payload_json = json.dumps(payload)

@shared_task(name='send_live_signal')
def send_live_signal():
    ws.connect(websocket_url)
    ws.send(payload_json)
    


# celery
# celery -A pdo_project worker --loglevel=INFO
# celery -A pdo_project beat --loglevel=INFO
