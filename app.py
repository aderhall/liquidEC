import time
import serial, threading # For reading arduino data asynchronously
from flask import Flask # Web server
from flask_socketio import SocketIO, emit # Websockets
import random

# Run "ls /dev/cu*" to find the port, then paste it here
serial_path = "/dev/cu.usbmodem14101"

demo_mode = True # True to generate fake "arduino" data
if not demo_mode:
    # Open the serial channel
    ser = serial.Serial(serial_path)
    def serial_get():
        return ser.readline().strip().decode("utf-8")
else:
    # Make up fake data
    p = 512
    def serial_get():
        global p
        p += 0.1 * (2 * random.random() - 1)
        if p > 1024: p = 1024
        if p < 0: p = 0
        return int(p)

# Global variable storing the most recent data from the arduino
mostRecentSerialInput = None
def read_serial():
    """Continually read the serial data, storing the most recent data in shared memory"""
    global mostRecentSerialInput
    while True:
        if not demo_mode and not ser.isOpen():
            mostRecentSerialInput = None
        else:
            mostRecentSerialInput = serial_get()
# Create and start the thread so that reading the serial won't block the server
thread = threading.Thread(target=read_serial)
thread.start()

# Server state
app = Flask(__name__)

# Route for main (index) page
@app.route("/")
def hello_world():
    # Load and deliver the index.html file
    with open("index.html", "r") as f:
        html = f.read()
    return html
    
# I'm skeptical that we need this
app.config['SECRET_KEY'] = 'secret!'
app.logger.disabled = True

# Websockets wrapper
socketio = SocketIO(app)

# Receive messages
@socketio.on('connected')
def handle_message(status):
    print(f"Client connected with status: {status}")
    
@socketio.on('requestdatastream')
def handle_message():
    while True:
        time.sleep(0.02)
        emit("newdata", str(mostRecentSerialInput))

# Start the server
if __name__ == '__main__':
    socketio.run(app, log_output=False)
