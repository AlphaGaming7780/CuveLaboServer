import threading
from flask import Flask, jsonify, render_template, request
from TortankWebServer.TortankLib.Tortank import Tortank

tortank : Tortank = Tortank()
app = Flask(__name__, static_url_path='') ## Changer le __name__ en un vrais nom ?

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/GetWaterLevel', methods=["GET"])
def SendWaterLevel():

    waterLevel = []

    # v1 = tortank.GetWaterLevelCuve1()
    # v2 = tortank.GetWaterLevelCuve1()
    # v3 = tortank.GetWaterLevelCuve1()

    # print(f"Value start : {[v1, v2, v3]}")

    # # Envoyer les données de Tortank
    # waterLevel.append(tortank.GetWaterLevelCuve1() / 32768 / 4.096)
    # waterLevel.append(tortank.GetWaterLevelCuve2() / 32768 / 4.096)
    # waterLevel.append(tortank.GetWaterLevelCuve3() / 32768 / 4.096)

    # print(f"Value end : {waterLevel}")

    waterLevel.append(tortank.GetWaterLevelCuve1() / 4.096)
    waterLevel.append(tortank.GetWaterLevelCuve2() / 4.096)
    waterLevel.append(tortank.GetWaterLevelCuve3() / 4.096)
    print(f"Value end : {waterLevel}")
    # waterLevel.append(0.5)
    # waterLevel.append(0.05)
    # waterLevel.append(0.975)
    
    rep = jsonify(waterLevel)
    rep.status_code = 200
    return rep

def main():
    webServerThread = threading.Thread(target=lambda: app.run(host='0.0.0.0', debug=True, use_reloader=False))
    # webServerThread = threading.Thread(target=lambda: app.run(debug=True, use_reloader=False))
    webServerThread.start()
    # app.run(use_reloader=True)

    tortank.SetMotor1Speed(1)

    while(True):

        waterLevel = tortank.GetHeigestWaterLevel() / 4.096

        if(waterLevel >= tortank.TORTANK_WATER_LEVEL_MAX) :
            tortank.SetMotor1Speed(0)
            tortank.SetMotor2Speed(0)
        pass

if __name__ == "__main__":
    main()