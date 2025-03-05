# Tuto : Flask with React
# https://nitratine.net/blog/post/how-to-serve-a-react-app-from-a-python-server/ 

from flask import Flask, jsonify, render_template, request

app = Flask(__name__, static_url_path='') ## Changer le __name__ en un vrais nom ?

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/GetWaterLevel', methods=["GET"])
def SendWaterLevel():

    waterLevel = []

    # Envoyer les données de Tortank
    waterLevel.append(0.5)
    waterLevel.append(0.05)
    waterLevel.append(0.975)
    
    rep = jsonify(waterLevel)
    rep.status_code = 200
    return rep

if __name__ == '__main__':


    # webServerThread = threading.Thread(target=lambda: app.run(host='0.0.0.0', debug=True, use_reloader=False))
    # webServerThread.start()

    app.run(use_reloader=True)