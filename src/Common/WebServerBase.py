from array import array
import threading
import time
import json
import random
from flask import Flask, Response, jsonify, request
from Common.LaboBase import LaboBase

class WebServerBase(object) :

    labo : LaboBase
    app : Flask
    waterLevels : array[float]

    def __init__(self, labo : LaboBase):
        self.labo = labo
        self.app = Flask(__name__, static_url_path='')
        self.waterLevels = [0.0, 0.0, 0.0]

    @app.route('/')
    def home(self):
        return self.app.send_static_file('index.html')

    @app.route('/event', methods=["GET"])  
    def event(self):
        # @stream_with_context
        def generate():
                while True:

                    obj = {
                        'time': time.strftime("%H:%M:%S", time.localtime()), # Pas vraiment bon, il peut dcp y avoir un décalage
                        'WaterLevel': self.waterLevels, 
                        'MotorSpeed': self.labo.GetMotorSpeed()
                    }

                    v = json.dumps(obj)

                    yield f"data:{v}\n\n"
                
                    time.sleep(1)

        return Response( generate(), mimetype='text/event-stream', content_type='text/event-stream', headers={ "Cache-Control": "no-cache", "Connection": "keep-alive" })

    @app.route('/GetWaterLevel', methods=["GET"])
    def GetWaterLevel(self):
        rep = jsonify(self.waterLevels)
        rep.status_code = 200
        return rep

    @app.route('/GetMotorSpeed', methods=["GET"])
    def GetMotorSpeed(self):
        rep = jsonify( self.labo.GetMotorSpeed() )
        rep.status_code = 200
        return rep

    @app.route('/SetMotorsSpeed', methods=["POST"])
    def SetMotorsSpeed(self):

        obj = {"idx": -1.0, "speed": -1.0}
        obj = request.json

        canRunMotor = self.labo.CanMotorRun(self.waterLevels)

        if(canRunMotor):
            self.labo.SetMotorSpeed(obj["idx"], obj["speed"])
        
        return Response(status=200)

    def Run(self):
        webServerThread = threading.Thread(target=lambda: self.app.run(host='0.0.0.0', debug=True, use_reloader=False))
        webServerThread.start()

        while(webServerThread.is_alive()):

            waterLevels = self.labo.GetWaterLevels()
            print(f"Final value: {waterLevels[0]}")

            if( not self.labo.CanMotorRun(waterLevels) ) :
                self.labo.StopAllMotors()

            pass