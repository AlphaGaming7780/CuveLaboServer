from gpiozero import Motor

# https://github.com/chandrawi/ADS1x15-ADC
from ADS1x15 import ADS1115

# import adafruit_ads1x15.ads1115 as ADS
# from adafruit_ads1x15.ads1115 import ADS1115
# from adafruit_ads1x15.analog_in import AnalogIn

class Tortank(object):

	TORTANK_WATER_LEVEL_MAX = 0.95

	_motor1 : Motor
	_motor2 : Motor

	_motor1Speed : int = 0
	_motor2Speed : int = 0

	ads : ADS1115

	CUVE_1_MIN = 620
	CUVE_1_MAX = 21228

	CUVE_2_MIN = 500 #1275
	CUVE_2_MAX = 22367

	CUVE_3_MIN = 1900 #1900
	CUVE_3_MAX = 23107

	def __init__(self):
		self._motor1 = Motor(17, 27)
		self._motor2 = Motor(23, 24)

		self.ads = ADS1115(1)
		self.ads.setGain(0)
		self.ads.setMode(self.ads.MODE_SINGLE)
		pass
	
	def SetMotor1Speed(self, speed : int):
		"""
		Set the speed of the motor 1.\n
		`speed` : int, take a number between 0 and 1. 0 stop, 1 full speed.
		"""
		self._motor1Speed = speed
		self._motor1.forward(speed)
		pass

	def GetMotor1Speed(self) -> int:
		"""
		Return the speed of the motor 1.\n
		`return` : int, a number between 0 and 1. 0 stop, 1 full speed.
		"""
		return self._motor1Speed

	def SetMotor2Speed(self, speed : int):
		"""
		Set the speed of the motor 2.\n
		`speed` : int, take a number between 0 and 1. 0 stop, 1 full speed.
		"""
		self._motor2Speed = speed
		self._motor2.forward(speed)
		pass
	
	def GetMotor2Speed(self) -> int:
		"""
		Return the speed of the motor 2.\n
		`return` : int, a number between 0 and 1. 0 stop, 1 full speed.
		"""
		return self._motor2Speed

	def ConvertRawWaterValue(self, rawADC : int) : 

		# Gestion du signe (valeur sur 16 bits, en complément à 2)
		if rawADC > 0x7FFF:
			rawADC -= 0x10000
			# rawADC = 0

		return rawADC / 32767
	

	def GetWaterLevelCuve1(self) -> int:
		# return self.ConvertRawWaterValue(self.cuve1.value)
		return ( self.ads.readADC(0) - self.CUVE_1_MIN) / ( self.CUVE_1_MAX - self.CUVE_1_MIN ) 

	def GetWaterLevelCuve2(self) -> int:
		# return self.ConvertRawWaterValue(self.cuve2.value)
		return ( self.ads.readADC(1) - self.CUVE_2_MIN) / ( self.CUVE_2_MAX - self.CUVE_2_MIN ) 
	
	def GetWaterLevelCuve3(self) -> int:
		# return self.ConvertRawWaterValue(self.cuve3.value)
		return ( self.ads.readADC(2) - self.CUVE_3_MIN) / ( self.CUVE_3_MAX - self.CUVE_3_MIN ) 
	
	# def GetGainInTension(self) -> float:

	# 	# PGA Settings :
	# 	# 2/3 = +-6.144v
	# 	# 1 = +-4.069v
	# 	# 2 = +-2.048v
	# 	# 4 = +-1.024v
	# 	# 8 = +-0.512v
	# 	# 16 = +-0.256v
	# 	match(self.ads.gain):
	# 		case 2/3 : // <--- Fonctionne pas
	# 			return 6.144
	# 		case 1 :
	# 			return 4.069
	# 		case 2 :
	# 			return 2.048
	# 		case 4 :
	# 			return 1.024
	# 		case 8 :
	# 			return 0.512
	# 		case 16 :
	# 			return 0.256
	# 		case _ :
	# 			return 1