import threading
import time
import json
from flask import Flask, Response, jsonify, request
from Common.LaboBase import LaboBase

class WebServerBase:
    def __init__(self, labo: LaboBase):
        self._labo = labo
        self._waterLevels = [0.0, 0.0, 0.0]
        self._app = Flask(__name__, static_url_path='')

        # Bind routes to the correct app instance (self._app)
        self._app.add_url_rule('/', view_func=self.home)
        self._app.add_url_rule('/GetBaseData', view_func=self.send_base_data, methods=["GET"])
        self._app.add_url_rule('/event', view_func=self.event, methods=["GET"])
        self._app.add_url_rule('/GetWaterLevel', view_func=self.get_water_level, methods=["GET"])
        self._app.add_url_rule('/GetMotorSpeed', view_func=self.get_motor_speed, methods=["GET"])
        self._app.add_url_rule('/SetMotorsSpeed', view_func=self.set_motors_speed, methods=["POST"])

    def home(self):
        return self._app.send_static_file('index.html')

    def send_base_data(self):
        data = {
            "numberOfCuve": self._labo._NbCuve,
            "numberOfMotor": self._labo._NbMotor
        }
        return jsonify(data), 200

    def event(self):
        def generate():
            while True:
                obj = {
                    'time': time.strftime("%H:%M:%S", time.localtime()),
                    'WaterLevel': self._waterLevels,
                    'MotorSpeed': self._labo.GetMotorsSpeed()
                }
                yield f"data:{json.dumps(obj)}\n\n"
                time.sleep(1)

        return Response(generate(), mimetype='text/event-stream', headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        })

    def get_water_level(self):
        return jsonify(self._waterLevels), 200

    def get_motor_speed(self):
        return jsonify(self._labo.GetMotorSpeed()), 200

    def set_motors_speed(self):
        data = request.get_json()
        motor_index = data.get("MotorIndex", -1)
        motor_speed = data.get("MotorSpeed", -1)

        can_run_motor = self._labo.CanMotorRun(self._waterLevels)

        if can_run_motor:
            self._labo.SetMotorSpeed(motor_index, motor_speed)

        return Response(status=200)

    def Run(self):
        def flask_thread():
            self._app.run(host='0.0.0.0', debug=True, use_reloader=False)

        web_server_thread = threading.Thread(target=flask_thread)
        web_server_thread.start()

        while web_server_thread.is_alive():
            self._waterLevels = self._labo.GetWaterLevels()
            print(f"Final value: {self._waterLevels[0]}")

            if not self._labo.CanMotorRun(self._waterLevels):
                self._labo.StopAllMotors()

            time.sleep(1)
