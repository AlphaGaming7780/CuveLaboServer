# Tuto : Flask with React
# https://nitratine.net/blog/post/how-to-serve-a-react-app-from-a-python-server/ 

from flask import Flask, jsonify, render_template, request

app = Flask(__name__, static_url_path='') ## Changer le __name__ en un vrais non ?

@app.route('/')
def home():
    return app.send_static_file('index.html')

if __name__ == '__main__':


    # webServerThread = threading.Thread(target=lambda: app.run(host='0.0.0.0', debug=True, use_reloader=False))
    # webServerThread.start()

    app.run()