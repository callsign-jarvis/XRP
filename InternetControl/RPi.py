# Raspberry Pi side code
import serial
import time
import paho.mqtt.client as mqtt

# Set up the serial connection to Pico (adjust port and settings if needed)
try:
    s = serial.Serial(port="/dev/ttyACM0", baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1)
    print("Connected to Pico via USB Serial.")
except serial.SerialException as e:
    print(f"Failed to connect to Pico: {e}")
    s = None

# Function to send a message to Pico
def send_msg_pico(data):
    if not s:
        print("Serial connection not established.")
        return
    try:
        s.reset_input_buffer()  # Clear any existing data in the input buffer
        s.write(data.encode('utf-8'))
        print("Sent data to Pico:", data)
    except Exception as e:
        print(f"Error sending data to Pico: {e}")

# MQTT configuration
MQTT_BROKER = "your mqtt server URL"
MQTT_PORT = 8883
MQTT_TOPIC = "test/topic"
MQTT_USER = "temps"
MQTT_PASSWORD = "password"

# Define the MQTT callback when a message is received
def on_message(client, userdata, msg):
    try:
        # Decode the received message
        command = msg.payload.decode('utf-8')
        print(f"Received command: {command}")

        # Send the command to Pico via serial
        send_msg_pico(command+'\n')# XRP expects command in this format
        time.sleep(0.5)  # Delay to ensure command is processed (optional)
    except Exception as e:
        print(f"Error handling received message: {e}")

# Set up MQTT client
client = mqtt.Client()

# Set up TLS for secure communication with HiveMQ
client.tls_set()  # Consider specifying CA certificates if required by the broker

# Set username and password
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

# Assign the message callback function
client.on_message = on_message

# Connect to the MQTT broker
try:
    client.connect(MQTT_BROKER, MQTT_PORT)
    print(f"Connected to MQTT Broker: {MQTT_BROKER}")
except Exception as e:
    print(f"Failed to connect to MQTT Broker: {e}")
    exit()

# Subscribe to the command topic
client.subscribe(MQTT_TOPIC)

# Start the MQTT client loop to listen for messages
client.loop_start()

# Main loop to keep the program running
try:
    while True:
        time.sleep(1)  # Keep the main loop alive
except KeyboardInterrupt:
    print("Exiting...")
finally:
    client.loop_stop()  # Stop the MQTT client loop
    client.disconnect()  # Disconnect from MQTT broker
    if s:
        s.close()  # Close the serial connection properly
        print("Serial connection closed.")

