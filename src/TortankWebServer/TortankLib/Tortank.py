from gpiozero import Motor
import board
from busio import I2C
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.analog_in import AnalogIn
# DEPRECATED
# from TortankWebServer.TortankLib.ADS1115 import ADS1115, ADS1115_MODE, ADS1115_PGA
# from TortankWebServer.TortankLib.bad_ADS1115 import ADS1115

class Tortank(object):

	TORTANK_WATER_LEVEL_MAX = 0.95

	_motor1 : Motor
	_motor2 : Motor

	_motor1Speed : int = 0
	_motor2Speed : int = 0

	i2c : I2C

	ads : ADS1115
	chan0 : AnalogIn
	chan1 : AnalogIn
	chan2 : AnalogIn

	def __init__(self):
		self._motor1 = Motor(17, 27)
		self._motor2 = Motor(23, 24)

		# Verifier si la lib Board marche avec le pi 5 sinon changer par les bonnes pins à la mano
		self.i2c = I2C(board.SCL, board.SDA) 

		self.ads = ADS1115(self.i2c)
		self.chan0 = AnalogIn(self.ads, ADS.P0)
		self.chan1 = AnalogIn(self.ads, ADS.P1)
		self.chan2 = AnalogIn(self.ads, ADS.P2)


		# PGA Settings :
		# 2/3 = +-6.144v
		# 1 = +-4.069v
		# 2 = +-2.048v
		# 4 = +-1.024v
		# 8 = +-0.512v
		# 16 = +-0.256v
		self.ads.gain = 1

		# self.ads = ADS1115()s
		# self.ads.setMode(ADS1115_MODE.SINGLESHOT)
		# self.ads.setGain(ADS1115_PGA.ADS1115_PGA_4P096)
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

		# Si la uint16 est interprété en tant que int et qu'elle n'a pas été convertie au préalable,
		# il faut alors le convertir, en rendant le nombre positif en ajoutant 32.767
		# rawADC += 0x7FFF # Décommenter cette ligne si on récupère des nombres négatifs

		# Divisé par 65535 car on veut un nombre entre 0 et 1.
		return rawADC / 65535

	def GetWaterLevelCuve1(self) -> int:
		# return self.ads.getConversionP0GND() / 32768 / 4.096
		# return self.chan0.voltage   # raw data not affected by the gain
		# return self.chan0.value  / 65535  / 4.096   # data affected by the gain
		return self.ConvertRawWaterValue(self.chan0.value)

	def GetWaterLevelCuve2(self) -> int:
		# return self.ads.getConversionP1GND() / 32768 / 4.096
		# return self.chan1.value  / 65535  / 4.096
		return self.ConvertRawWaterValue(self.chan1.value)
	
	def GetWaterLevelCuve3(self) -> int:
		# return self.ads.getConversionP2GND() / 32768 / 4.096
		# return self.chan2.value  / 65535  / 4.096
		return self.ConvertRawWaterValue(self.chan2.value)