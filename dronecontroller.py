from djitellopy import Tello
from flask import Flask, request, jsonify
import time



class DroneController:
    def __init__(self):
        self.drone = Tello()
        self.connected = False

    def connect(self):
        """Connect to the drone and handle connection errors."""
        try:
            self.drone.connect()
            self.connected = True
            return "Drone connected successfully."
        except Exception as e:
            self.connected = False
            return f"Error connecting to the drone: {e}"

    def get_battery(self):
        """Get the battery level."""
        if self.connected:
            return f"Battery: {self.drone.get_battery()}%"
        else:
            return "Drone not connected."

    def takeoff(self):
        """Take off the drone."""
        if self.connected:
            self.drone.takeoff()
            return "Drone is taking off."
        return "Drone not connected."

    def land(self):
        """Land the drone."""
        if self.connected:
            self.drone.land()
            return "Drone is landing."
        return "Drone not connected."

    def move(self, direction, distance=50):
        """Move the drone in a specified direction."""
        if not self.connected:
            return "Drone not connected."

        try:
            if direction == 'forward':
                self.drone.move_forward(distance)
            elif direction == 'back':
                self.drone.move_back(distance)
            elif direction == 'left':
                self.drone.move_left(distance)
            elif direction == 'right':
                self.drone.move_right(distance)
            elif direction == 'up':
                self.drone.move_up(distance)
            elif direction == 'down':
                self.drone.move_down(distance)
            return f"Drone moved {direction} by {distance} cm."
        except Exception as e:
            return f"Error moving the drone: {e}"

    def rotate(self, angle):
        """Rotate the drone by a specific angle."""
        if not self.connected:
            return "Drone not connected."

        try:
            self.drone.rotate_clockwise(angle)
            return f"Drone rotated {angle} degrees."
        except Exception as e:
            return f"Error rotating the drone: {e}"

    def end(self):
        """Safely end the drone connection."""
        self.drone.end()
        self.connected = False
        return "Connection to the drone ended."

# Initialize the drone controller
drone_controller = DroneController()

# Flask web server setup
app = Flask(__name__)

@app.route('/connect', methods=['GET'])
def connect():
    """Connect to the drone."""
    response = drone_controller.connect()
    return jsonify({"status": response})

@app.route('/battery', methods=['GET'])
def battery():
    """Get battery status."""
    response = drone_controller.get_battery()
    return jsonify({"status": response})

@app.route('/takeoff', methods=['POST'])
def takeoff():
    """Take off the drone."""
    response = drone_controller.takeoff()
    return jsonify({"status": response})

@app.route('/land', methods=['POST'])
def land():
    """Land the drone."""
    response = drone_controller.land()
    return jsonify({"status": response})

@app.route('/move', methods=['POST'])
def move():
    """Move the drone in a specific direction."""
    data = request.json
    direction = data.get('direction', 'forward')
    distance = data.get('distance', 50)
    response = drone_controller.move(direction, distance)
    return jsonify({"status": response})

@app.route('/rotate', methods=['POST'])
def rotate():
    """Rotate the drone by a specific angle."""
    data = request.json
    angle = data.get('angle', 90)
    response = drone_controller.rotate(angle)
    return jsonify({"status": response})

@app.route('/end', methods=['POST'])
def end():
    """End the drone connection."""
    response = drone_controller.end()
    return jsonify({"status": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
