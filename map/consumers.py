from channels.generic.websocket import JsonWebsocketConsumer
from .models import SensorReadings

#channels
class SignalConsumer(JsonWebsocketConsumer):
    
    '''
    :socket: 'ws://localhost:8000/ws/livesignals/'
    :sample Python Code:
        import json
        payload = {
            "message": {
                "temperature": 0.2,
                "pressure": 0.2,
                "steam_injection": 0.2,
                "sensor_id": 11
            }
        }
        payload_json = json.dumps(payload)
        import websocket
        ws = websocket.WebSocket()
        websocket_url = "ws://localhost:8000/ws/livesignals/"
        ws.connect(websocket_url)
        ws.send(payload_json)
        ws.close()
    
    :parameters:
        payload = {
            "message": {
                "temperature": 0.2,
                "pressure": 0.2,
                "steam_injection": 0.2,
                "sensor_id": 11
            }
        }
    
    :returns:
        None
        
    :sample JavaScript Code:
        const socket = new WebSocket('ws://localhost:8000/ws/livesignals/');

        function sendSignal(payload) {
            socket.onopen = function(event) {
            socket.send(JSON.stringify(payload));
            console.log('sendSignal data:', payload);
            }};
    :parameters:
        const sample_payload = {
        "message":{  
        "temperature": 0.7,
        "pressure": 0.3,
        "steam_injection": 0.3,
        "sensor_id": 9,
        }
        };
    '''
    
    def connect(self):
        self.accept()
    
    def receive_json(self, content):
        message = content['message']
        # print(message)
        
        received_message = SensorReadings(
            sensor_id = message['sensor_id'],
            temperature = message['temperature'],
            pressure = message['pressure'],
            steam_injection = message['steam_injection']
            )
        received_message.save()
        self.send_json({'message': message})