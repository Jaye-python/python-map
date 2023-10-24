const sample_payload = {
    "message":{  
     "temperature": 0.7,
     "pressure": 0.3,
     "steam_injection": 0.3,
     "sensor_id": 9,
    }
 };

const socket = new WebSocket('ws://localhost:8000/ws/livesignals/');

function sendSignal(payload) {

    socket.onopen = function(event) {

    socket.send(JSON.stringify(payload));
    console.log('sendSignal data:', payload);

}};