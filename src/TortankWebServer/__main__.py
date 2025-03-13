from array import array
import threading
import time
import json
import random
from flask import Flask, Response, jsonify, request
from TortankWebServer.TortankLib.Tortank import Tortank

tortank : Tortank = Tortank()
app = Flask(__name__, static_url_path='')

waterLevels = [0.0, 0.0, 0.0]

motor1Speed : float = 0.0
motor2Speed : float = 0.0


@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/event', methods=["GET"])  
def event():
    # @stream_with_context
    def generate():
            while True:

                obj = {
                    'time': time.strftime("%H:%M:%S", time.localtime()), # Pas vraiment bon, il peut dcp y avoir un décalage
                    'WaterLevel': waterLevels, 
                    'MotorSpeed': [
                        tortank.GetMotor1Speed(), 
                        tortank.GetMotor2Speed(),
                        # random.random(), random.random()
                        # motor1Speed, motor2Speed
                    ]
                }

                v = json.dumps(obj)

                yield f"data:{v}\n\n"
            
                time.sleep(1)

    return Response( generate(), mimetype='text/event-stream', content_type='text/event-stream', headers={ "Cache-Control": "no-cache", "Connection": "keep-alive" })

@app.route('/GetWaterLevel', methods=["GET"])
def GetWaterLevel():
    rep = jsonify(waterLevels)
    rep.status_code = 200
    return rep

@app.route('/GetMotorSpeed', methods=["GET"])
def GetMotorSpeed():
    rep = jsonify( 
        [ 
            # random.random(), random.random()
            tortank.GetMotor1Speed(), 
            tortank.GetMotor2Speed() 
            # motor1Speed, motor2Speed
        ] 
    )
    rep.status_code = 200
    return rep

@app.route('/SetMotorsSpeed', methods=["POST"])
def SetMotorsSpeed():

    obj = {"Motor1Speed": -1.0, "Motor2Speed": -1.0}
    obj = request.json

    # canRunMotor = tortank.CanMotorRun(waterLevels)
    canRunMotor = True

    if(obj["Motor1Speed"] >= 0 and canRunMotor) :
        tortank.SetMotor1Speed(obj["Motor1Speed"])
        # motor1Speed = obj["Motor1Speed"]
        pass
    
    if(obj["Motor2Speed"] >= 0 and canRunMotor) :
        tortank.SetMotor2Speed(obj["Motor2Speed"])
        # motor2Speed = obj["Motor1Speed"]
        pass
    
    return Response(status=200)

def main():
    webServerThread = threading.Thread(target=lambda: app.run(host='0.0.0.0', debug=True, use_reloader=False))
    # webServerThread = threading.Thread(target=lambda: app.run(debug=True, use_reloader=False))
    webServerThread.start()
    # app.run(use_reloader=True)

    # tortank.SetMotor1Speed(1)
    # tortank.SetMotor2Speed(1)

    # hitTheLimit = False
    # motorSpeedBeforHitTheLimit = [0,0]

    while(True):

        waterLevels[0] = tortank.GetWaterLevelCuve1()
        waterLevels[1] = tortank.GetWaterLevelCuve2()
        waterLevels[2] = tortank.GetWaterLevelCuve3()

        # waterLevels[0] = random.random()
        # waterLevels[1] = random.random()
        # waterLevels[2] = random.random()

        # print(f"WaterLevel : {waterLevels}")

        # rawValue = [tortank.ads.readADC(0), tortank.ads.readADC(1), tortank.ads.readADC(2)]
        # print(f"RawValue : {rawValue}")

        # voltage = [tortank.ads.toVoltage(rawValue[0]), tortank.ads.toVoltage(rawValue[1]), tortank.ads.toVoltage(rawValue[2])]
        # print(f"Voltage : {voltage}")


        if( not tortank.CanMotorRun(waterLevels) ) :
            if( not hitTheLimit ) : motorSpeedBeforHitTheLimit = [ tortank.GetMotor1Speed(), tortank.GetMotor2Speed() ]
            hitTheLimit = True
            tortank.SetMotor1Speed(0)
            tortank.SetMotor2Speed(0)
        elif ( hitTheLimit ) : 
            tortank.SetMotor1Speed(motorSpeedBeforHitTheLimit[0])
            tortank.SetMotor2Speed(motorSpeedBeforHitTheLimit[1])
        pass

if __name__ == "__main__":
    main()