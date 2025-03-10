from gpiozero import Motor
from busio import I2C

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

	i2c : I2C

	ads : ADS1115
	# cuve1 : AnalogIn
	# cuve2 : AnalogIn
	# cuve3 : AnalogIn

	def __init__(self):
		self._motor1 = Motor(17, 27)
		self._motor2 = Motor(23, 24)

		# Verifier si la lib Board marche avec le pi 5 sinon changer par les bonnes pins à la mano
		self.i2c = I2C(5, 3) 

		self.ads = ADS1115(self.i2c)
		# self.cuve1 = AnalogIn(self.ads, ADS.P0)
		# self.cuve2 = AnalogIn(self.ads, ADS.P1)
		# self.cuve3 = AnalogIn(self.ads, ADS.P2)

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
		if raw_adc > 0x7FFF:
			raw_adc -= 0x10000
			# raw_adc = 0

		return rawADC / 32767

	def GetWaterLevelCuve1(self) -> int:
		# return self.ConvertRawWaterValue(self.cuve1.value)
		return self.ConvertRawWaterValue(self.ads.readADC(0))

	def GetWaterLevelCuve2(self) -> int:
		# return self.ConvertRawWaterValue(self.cuve2.value)
		return self.ConvertRawWaterValue(self.ads.readADC(1))
	
	def GetWaterLevelCuve3(self) -> int:
		# return self.ConvertRawWaterValue(self.cuve3.value)
		return self.ConvertRawWaterValue(self.ads.readADC(2))
	
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