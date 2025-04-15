import threading
import time
import json
from typing import List, TypedDict
import socket
from flask import Flask, Response, jsonify, request
from Common.LaboBase import LaboBase

class WebServerBase:

	class Client(TypedDict):
		Ip : str
		Name : str
		lastPing : float

	def __init__(self, labo: LaboBase):
		self._labo = labo
		self._waterLevels = [0.0, 0.0, 0.0]
		self._app = Flask(__name__, static_url_path='')

		self._Ip = self.get_local_ip()
		print(f"IP : {self._Ip}")
		self._defaultClient : WebServerBase.Client = {"Ip": self._Ip, "Name": "WebPage"}
		self._ActiveClient : WebServerBase.Client = self._defaultClient
		self._ClientList : List[WebServerBase.Client] = []
		self._ClientEnable = False
		self._ClientAreDirty = False

		# Bind routes to the correct app instance (self._app)
		self._app.add_url_rule('/', view_func=self.home)
		self._app.add_url_rule('/RegisterClient', view_func=self.RegisterClient, methods=["POST"])
		self._app.add_url_rule('/UnregisterClient', view_func=self.UnregisterClient, methods=["POST"])
		self._app.add_url_rule('/ClientsDataUpdate', view_func=self.ClientsDataUpdate, methods=["GET"])
		self._app.add_url_rule('/GetClientsData', view_func=self.SendClientsData, methods=["GET"])
		self._app.add_url_rule('/ClientIsStillActive', view_func=self.SetClientIsStillActive, methods=["POST"])
		self._app.add_url_rule('/ResetActiveClient', view_func=self.ResetActiveClient, methods=["POST"])
		self._app.add_url_rule('/ChangeClientMode', view_func=self.ChangeClientMode, methods=["POST"])
		self._app.add_url_rule('/DataStream', view_func=self.DataStream, methods=["GET"])
		self._app.add_url_rule('/GetBaseData', view_func=self.send_base_data, methods=["GET"])
		self._app.add_url_rule('/GetWaterLevel', view_func=self.get_water_level, methods=["GET"])
		self._app.add_url_rule('/GetWaterLevels', view_func=self.get_water_levels, methods=["GET"])
		self._app.add_url_rule('/GetMotorSpeed', view_func=self.get_motor_speed, methods=["GET"])
		self._app.add_url_rule('/SetMotorSpeed', view_func=self.set_motor_speed, methods=["POST"])
		self._app.add_url_rule('/GetMotorsSpeed', view_func=self.get_motors_speed, methods=["GET"])
		self._app.add_url_rule('/SetMotorsSpeed', view_func=self.set_motors_speed, methods=["POST"])
		
	def get_local_ip(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		try:
			# Connexion bidon juste pour récupérer l’IP locale assignée
			s.connect(("8.8.8.8", 80))
			ip = s.getsockname()[0]
		finally:
			s.close()
		return ip

	def home(self):
		return self._app.send_static_file('index.html')

	def RegisterClient(self):
		data = request.get_json()
		ip = request.remote_addr
		name = data.get("Name", ip)

		isAlreadyInList = False
		i : int = 0
		for i in range(0, self._ClientList.__len__()):
			if(self._ClientList[i]["Ip"] == ip): 
				isAlreadyInList = True
				break

		if(isAlreadyInList):
			self._ClientList[i]["Name"] = name
			self._ClientList[i]["lastPing"] = time.time()
		
		else:
			self._ClientList.append({"Ip": ip, "Name": name, "lastPing": time.time()})

		self._ClientAreDirty = True

		return jsonify(), 200
	
	def UnregisterClient(self):

		ip = request.remote_addr

		isInList = False
		i : int = 0
		for i in range(0, self._ClientList.__len__()):
			if(self._ClientList[i]["Ip"] == ip): 
				isInList = True
				break
		
		if(self._ActiveClient["Ip"] == ip):
			self._labo.Reset()
			self._ActiveClient = self._defaultClient
			self._ClientAreDirty = True

		if(not isInList):  return jsonify(), 200

		self._ClientList.pop(i)

		self._ClientAreDirty = True
		
		return jsonify(), 200

	def SetClientIsStillActive(self):
		ip = request.remote_addr

		isInList = False
		i : int = 0
		for i in range(0, self._ClientList.__len__()):
			if(self._ClientList[i]["Ip"] == ip): 
				isInList = True
				self._ClientList[i]["lastPing"] = time.time()
				break

		if(not isInList): return jsonify(), 403
		return jsonify(), 200

	def ClientsDataUpdate(self):
		def generate():
			while True:
				time.sleep(1)

				t = time.time()
				for client in self._ClientList:
					if(t - client["lastPing"] > 2):
						print(f"Client : {client['Name']} didn't ping the last two second.")
						self._ClientList.remove(client)
						if(self._ActiveClient["Ip"] == client["Ip"]):
							print("Client was the active one, reseting.")
							self._labo.Reset()
							self._ActiveClient == self._defaultClient
						self._ClientAreDirty = True

				if self._ClientEnable and self._ActiveClient == self._defaultClient and len(self._ClientList) > 0:
					self._labo.Reset()
					self._ActiveClient = self._ClientList[0]
					self._ClientAreDirty = True

				if not self._ClientAreDirty:
					continue

				self._ClientAreDirty = False

				obj = self.GetClientsData()
				# IMPORTANT : espace après "data:"
				yield f"data: {json.dumps(obj)}\n\n"

		return Response(generate(), mimetype='text/event-stream', headers={
			"Cache-Control": "no-cache",
			"Connection": "keep-alive"
		})
	
	def SendClientsData(self) :
		return jsonify(self.GetClientsData()), 200
	
	def GetClientsData(self) : 
		activeIp = ""
		if(self._ActiveClient != None):
			activeIp = self._ActiveClient["Ip"]

		obj = {
			'ClientEnabled': self._ClientEnable,
			'ActiveClient': activeIp,
			'ClientList': self._ClientList
		}
		return obj

	def ResetActiveClient(self):
		ip = request.remote_addr
		if(self._Ip != ip):
			print(f"Request IP: {ip}, self IP: {self._Ip}")
			return jsonify(), 403

		self._ClientEnable = False
		self._labo.Reset()
		self._ActiveClient = self._defaultClient
		self._ClientAreDirty = True
		return jsonify(), 200
	
	def ChangeClientMode(self):
		ip = request.remote_addr
		data = request.get_json()
		value = data.get("ClientEnabled", not self._ClientEnable)

		if(self._Ip != ip):
			print(f"Request IP: {ip}, self IP: {self._Ip}")
			return jsonify(), 403

		self._ClientEnable = value
		self._labo.Reset()
		self._ActiveClient = self._defaultClient
		self._ClientAreDirty = True

		return jsonify(), 200

	def DataStream(self):
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

	def send_base_data(self):
		data = {
			"numberOfCuve": self._labo._NbCuve,
			"numberOfMotor": self._labo._NbMotor
		}
		return jsonify(data), 200

	def get_water_level(self):
		cuveIndex = request.args.get("CuveIndex", -1, type=int)
		if (cuveIndex < 0 or cuveIndex >= self._labo._NbCuve) : return jsonify(-1), 200
		return jsonify(self._waterLevels[cuveIndex]), 200

	def get_water_levels(self):
		return jsonify(self._waterLevels), 200

	def get_motor_speed(self):
		motor_index = request.args.get("MotorIndex", -1, type=int)
		return jsonify(self._labo.GetMotorSpeed(motor_index)), 200

	def set_motor_speed(self):

		if(not self.CanSet()):  return jsonify(), 403

		data = request.get_json()
		motor_index = data.get("MotorIndex", -1)
		motor_speed = data.get("MotorSpeed", -1)

		can_run_motor = self._labo.CanMotorRun(self._waterLevels)

		if can_run_motor:
			self._labo.SetMotorSpeed(motor_index, motor_speed)

		return Response(status=200)
	
	def get_motors_speed(self):
		return jsonify(self._labo._MotorsCurrentSpeed), 200

	def set_motors_speed(self):

		if(not self.CanSet()):  return jsonify(), 403

		data = request.get_json()  # attend une liste de dictionnaires

		can_run_motor = self._labo.CanMotorRun(self._waterLevels)

		if can_run_motor and isinstance(data, list):
			for motor in data:
				motor_index = motor.get("MotorIndex", -1)
				motor_speed = motor.get("MotorSpeed", -1)
				self._labo.SetMotorSpeed(motor_index, motor_speed)

		return Response(status=200)

	def CanSet(self) -> bool :
		ip = request.remote_addr
		value = self._ActiveClient["Ip"] == ip
		
		if(not value):
			print(f"Request IP: {ip}, Active IP: {self._ActiveClient['Ip']}")

		return value

	def Run(self):
		def flask_thread():
			self._app.run(host='0.0.0.0', debug=True, use_reloader=False)

		web_server_thread = threading.Thread(target=flask_thread, daemon=True)
		web_server_thread.start()

		while web_server_thread.is_alive():
			self._waterLevels = self._labo.GetWaterLevels()
			print(f"Final value: {self._waterLevels[0]}")

			if not self._labo.CanMotorRun(self._waterLevels):
				self._labo.StopAllMotors()

			# Enlever ce timer pour maximisé les mise a jour.
			time.sleep(1)
