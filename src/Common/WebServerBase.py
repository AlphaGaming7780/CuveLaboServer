import threading
import time
import json
from typing import List, TypedDict
import socket
from flask import Flask, Response, jsonify, request
from Common.LaboBase import LaboBase

class WebServerBase:

	MDP : str = "admin"
	MinimumWaterLevel : float = 0.05 # Le niveau d'eau minimum pour activer le (prochain) client, 5%.

	class Client(TypedDict):
		Ip : str
		Name : str
		lastPing : float
		isAdmin : bool

	def __init__(self, labo: LaboBase):
		self._labo = labo
		self._waterLevels = [0.0, 0.0, 0.0]
		self._app = Flask(__name__, static_url_path='')

		self._Ip = self.get_local_ip()
		print(f"IP : {self._Ip}")
		self._defaultClient : WebServerBase.Client = WebServerBase.Client(Ip=self._Ip, Name="WebPage", lastPing=time.time(), isAdmin=True)
		self._ActiveClient : WebServerBase.Client = self._defaultClient
		self._ClientList : List[WebServerBase.Client] = []
		self._AdminClientList : List[WebServerBase.Client] = [] # Peut être ajouter le default client dedans ?
		self._ClientEnable = False
		self._ClientAreDirty = False

		# Bind routes to the correct app instance (self._app)
		self._app.add_url_rule('/', view_func=self.home)
		self._app.add_url_rule('/RegisterClient', view_func=self.RegisterClient, methods=["POST"])
		self._app.add_url_rule('/UnregisterClient', view_func=self.UnregisterClient, methods=["POST"])
		self._app.add_url_rule('/RegisterAdmin', view_func=self.RegisterAdmin, methods=["POST"])
		self._app.add_url_rule('/ClientsDataUpdate', view_func=self.ClientsDataUpdate, methods=["GET"])
		self._app.add_url_rule('/GetClientsData', view_func=self.SendClientsData, methods=["GET"])
		self._app.add_url_rule('/ClientIsStillActive', view_func=self.SetClientIsStillActive, methods=["POST"])
		self._app.add_url_rule('/ResetActiveClient', view_func=self.ResetActiveClient, methods=["POST"])
		self._app.add_url_rule('/ChangeClientMode', view_func=self.ChangeClientMode, methods=["POST"])
		self._app.add_url_rule('/TakeControl', view_func=self.TakeControl, methods=["POST"])
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
			self._ClientList.append(WebServerBase.Client(Name=name, Ip=ip, lastPing=time.time(), isAdmin=False))

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

	def RegisterAdmin(self):
		data = request.get_json()
		ip = request.remote_addr
		mdp = data.get("Password", None)
		name = data.get("Name", ip)

		if(mdp != self.MDP): 
			print(f"Client {name} didn't enter the right password : {mdp}.")
			return jsonify(), 403

		client = self.ClientByIP(ip)
		if(client == None):
			client = WebServerBase.Client(Name=name, Ip=ip, lastPing=time.time(), isAdmin=False)

		if(client["isAdmin"] == True and self.GetAdminClient(ip) != None):
			print(f"Client {client['Name']} is already admin.")
		else:
			client["isAdmin"] = True
			self._AdminClientList.append(client)
			print(f"Client {client['Name']} is now admin.")

		return jsonify(), 200

	def SetClientIsStillActive(self):
		ip = request.remote_addr

		if(self._ActiveClient["Ip"] == ip):
			self._ActiveClient["lastPing"] = time.time()
			return jsonify(), 200

		i : int = 0
		for i in range(0, self._ClientList.__len__()):
			if(self._ClientList[i]["Ip"] == ip): 
				isInList = True
				self._ClientList[i]["lastPing"] = time.time()
				return jsonify(), 200

		return jsonify(), 403

	def ClientsDataUpdate(self):
		def generate():
			while True:

				t = time.time()

				if(self._ActiveClient != None and self._ActiveClient["isAdmin"] == False and t - self._ActiveClient["lastPing"] > 2):
					print(f"Active client {self._ActiveClient['Name']} didn't ping the last two second. Resetting.")
					self._labo.Reset()
					self._ActiveClient == self._defaultClient
					self._ClientAreDirty = True

				for client in self._ClientList:
					if(t - client["lastPing"] > 2):
						print(f"Client : {client['Name']} didn't ping the last two second.")
						self._ClientList.remove(client)
						self._ClientAreDirty = True


				if self._ClientEnable and self._ActiveClient == self._defaultClient and len(self._ClientList) > 0 and max(self._waterLevels) < self.MinimumWaterLevel :
					self._labo.Reset()
					self._ActiveClient = self._ClientList.pop(0)
					self._ClientAreDirty = True

				# Disabled the dirty check because it look like some event are ignored if they aren't sent continusly.
				# if not self._ClientAreDirty:
				# 	continue
				
				# This should do an instant data send when the client is dirty.
				timeNow = time.time()
				while not self._ClientAreDirty:
					if time.time() - timeNow > 1: # 1 second delay to avoid flooding the client with data.
						break
					time.sleep(0.05) # Sleep a bit to avoid busy waiting and recheck the while condition.

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

		obj = {
			'ClientEnabled': self._ClientEnable,
			'ActiveClient': self._ActiveClient,
			'ClientList': self._ClientList
		}
		return obj

	def ResetActiveClient(self):
		ip = request.remote_addr

		if(self.IsAdmin(ip) == False):
			return jsonify(), 403

		self._ClientEnable = False
		self._labo.Reset()
		self._ActiveClient = self._defaultClient
		self._ClientList = []
		self._ClientAreDirty = True
		return jsonify(), 200
	
	def ChangeClientMode(self):
		ip = request.remote_addr
		data = request.get_json()
		value = data.get("ClientEnabled", not self._ClientEnable)

		if(self.IsAdmin(ip) == False):
			return jsonify(), 403

		self._ClientEnable = value
		self._labo.Reset()
		self._ActiveClient = self._defaultClient
		self._ClientAreDirty = True

		return jsonify(), 200
	
	def SetActiveClient(self, client : Client):
		self._ClientEnable = False
		self._labo.Reset()
		self._ActiveClient = client
		self._ClientAreDirty = True

	def TakeControl(self):
		ip = request.remote_addr

		client = self.GetAdminClient(ip)
		if(client == None or client["isAdmin"] == False):
			return jsonify(), 403

		self.SetActiveClient(client)

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
	
	def IsAdmin(self, ip : str) -> bool:
		for client in self._AdminClientList:
			if(client["Ip"] == ip):
				print(f"Client {ip} is admin : {client['isAdmin']}.")
				return client["isAdmin"]

		return False

	def ClientByIP(self, ip : str) -> Client | None:
		for client in self._ClientList:
			if(client["Ip"] == ip):
				return client
			
		for client in self._AdminClientList:
			if(client["Ip"] == ip):
				return client

		return None
	
	def GetAdminClient(self, ip : str) -> Client | None:
		for client in self._AdminClientList:
			if(client["Ip"] == ip):
				return client

		return None

	def Run(self):
		def flask_thread():
			self._app.run(host='0.0.0.0', debug=True, use_reloader=False)

		web_server_thread = threading.Thread(target=flask_thread, daemon=True)
		web_server_thread.start()

		while web_server_thread.is_alive():
			self._waterLevels = self._labo.GetWaterLevels()
			# print(f"Water levels : {self._waterLevels}")

			if not self._labo.CanMotorRun(self._waterLevels):
				self._labo.StopAllMotors()

			# Enlever ce timer pour maximisé les mise a jour.
			# time.sleep(1)