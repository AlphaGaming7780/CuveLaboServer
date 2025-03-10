import threading
import time
import json
import random
from flask import Flask, Response, jsonify
from TortankWebServer.TortankLib.Tortank import Tortank

tortank : Tortank = Tortank()
app = Flask(__name__, static_url_path='')

waterLevel = [0.0, 0.0, 0.0]

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
                    'WaterLevel': waterLevel, 
                    'MotorSpeed': [
                        tortank.GetMotor1Speed(), 
                        tortank.GetMotor2Speed(),
                        # random.random(), random.random()
                    ]
                }

                v = json.dumps(obj)

                yield f"data:{v}\n\n"
            
                time.sleep(1)

    return Response( generate(), mimetype='text/event-stream', content_type='text/event-stream', headers={ "Cache-Control": "no-cache", "Connection": "keep-alive" })

@app.route('/GetUpdatedValue', methods=["GET"])
def SendGetUpdatedValue():
    rep = jsonify(  
        {
            "WaterLevel": waterLevel, 
            "MotorSpeed": [ 
                # random.random(), random.random()
                tortank.GetMotor1Speed(), 
                tortank.GetMotor2Speed()
            ]
        }
    )
    rep.status_code = 200
    return rep

@app.route('/GetWaterLevel', methods=["GET"])
def SendWaterLevel():
    rep = jsonify(waterLevel)
    rep.status_code = 200
    return rep

@app.route('/GetMotorSpeed', methods=["GET"])
def SendMotorSpeed():
    rep = jsonify( 
        [ 
            # random.random(), random.random()
            tortank.GetMotor1Speed(), 
            tortank.GetMotor2Speed() 
        ] 
    )
    rep.status_code = 200
    return rep

def main():
    webServerThread = threading.Thread(target=lambda: app.run(host='0.0.0.0', debug=True, use_reloader=False))
    # webServerThread = threading.Thread(target=lambda: app.run(debug=True, use_reloader=False))
    webServerThread.start()
    # app.run(use_reloader=True)

    tortank.SetMotor1Speed(1)
    tortank.SetMotor2Speed(1)

    while(True):

        waterLevel[0] = tortank.GetWaterLevelCuve1()
        waterLevel[1] = tortank.GetWaterLevelCuve2()
        waterLevel[2] = tortank.GetWaterLevelCuve3()

        # waterLevel[0] = random.random()
        # waterLevel[1] = random.random()
        # waterLevel[2] = random.random()

        print(f"WaterLevel : {waterLevel}")

        rawValue = [tortank.ads.readADC(0), tortank.ads.readADC(1), tortank.ads.readADC(2)]
        print(f"RawValue : {rawValue}")

        voltage = [tortank.ads.toVoltage(rawValue[0]), tortank.ads.toVoltage(rawValue[1]), tortank.ads.toVoltage(rawValue[2])]
        print(f"Voltage : {voltage}")

        waterLevelMax = max(waterLevel)
        voltageMax = max( voltage )

        if( waterLevelMax >= tortank.TORTANK_WATER_LEVEL_MAX or voltageMax >= 4 ) :
            tortank.SetMotor1Speed(0)
            tortank.SetMotor2Speed(0)
        pass

if __name__ == "__main__":
    main()