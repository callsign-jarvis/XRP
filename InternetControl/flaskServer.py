from flask import Flask, request, render_template_string
import paho.mqtt.client as mqtt

# Flask App Initialization
app = Flask(__name__)

# --- MQTT Configuration ---
MQTT_BROKER = "mqttbroker url"
MQTT_PORT = 8883
MQTT_USER = "temps"
MQTT_PASSWORD = "password"
MQTT_TOPIC = "test/topic"

# HTML Template (Joystick Interface with "+" Layout and Styled Buttons)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Joystick Control</title>
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
        }
        .joystick-container {
            display: grid;
            grid-template-rows: 1fr 1fr 1fr;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 10px;
        }
        .button {
            width: 100px;
            height: 100px;
            font-size: 18px;
            font-weight: bold;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            background-color: #007bff;
            color: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .button:hover {
            background-color: #0056b3;
        }
        .button:active {
            transform: translateY(2px);
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }
        .empty {
            visibility: hidden;
        }
    </style>
</head>
<body>
    <div class="joystick-container">
        <div class="empty"></div>
        <button class="button" onclick="sendCommand('F')">Forward</button>
        <div class="empty"></div>
        <button class="button" onclick="sendCommand('L')">Left</button>
        <div class="empty"></div>
        <button class="button" onclick="sendCommand('R')">Right</button>
        <div class="empty"></div>
        <button class="button" onclick="sendCommand('B')">Backward</button>
        <div class="empty"></div>
    </div>

    <script>
        function sendCommand(direction) {
            fetch('/move', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ direction: direction })
            })
            .then(response => response.text())
            .then(data => console.log(data))
            .catch(error => console.error('Error:', error));
        }
    </script>
</body>
</html>
"""

# MQTT Client Setup
def init_mqtt_client():
    client = mqtt.Client()
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    client.tls_set()  # Enable TLS for secure communication
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    return client

def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"Connected to MQTT broker with reason code {reason_code}")

def on_disconnect(client, userdata, reason_code, properties=None):
    print(f"Disconnected from MQTT broker with reason code {reason_code}")

mqtt_client = init_mqtt_client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT)

# Flask Routes
@app.route('/')
def home():
    """Render the joystick interface."""
    return render_template_string(HTML_TEMPLATE)

@app.route('/move', methods=['POST'])
def move():
    """Handle joystick commands and publish them to the MQTT topic."""
    data = request.get_json()
    direction = data.get("direction")
    if direction in ['F', 'B', 'L', 'R']:
        mqtt_client.publish(MQTT_TOPIC, direction)
        print(f"Published: {direction}")
        return f"Sent {direction} command!", 200
    else:
        return "Invalid command", 400

if __name__ == "__main__":
    # Start the MQTT loop in a background thread
    mqtt_client.loop_start()

    # Run the Flask app
    app.run(host="0.0.0.0", port=8080)
