from gpiozero import Motor
from gpiozero import LED

# https://github.com/chandrawi/ADS1x15-ADC
from ADS1x15 import ADS1115

# import adafruit_ads1x15.ads1115 as ADS
# from adafruit_ads1x15.ads1115 import ADS1115
# from adafruit_ads1x15.analog_in import AnalogIn

class Tortank(object):

	WATER_LEVEL_MAX = 0.95

	_motor1 : Motor
	_motor2 : Motor

	_motor1Speed : float = 0
	_motor2Speed : float = 0

	Output1 : LED

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

		self.Output1 = LED(26)
		self.Output1.on

		self.ads = ADS1115(1)
		# self.ads.setGain(0)
		self.ads.setGain(self.ads.PGA_0_256V)
		self.ads.setMode(self.ads.MODE_SINGLE)
		pass
	
	def SetMotor1Speed(self, speed : float):
		"""
		Set the speed of the motor 1.\n
		`speed` : int, take a number between 0 and 1. 0 stop, 1 full speed.
		"""

		if(speed > 1) : speed = 1
		if(speed < 0) : speed = 0

		self._motor1Speed = speed
		self._motor1.forward(speed)
		pass

	def GetMotor1Speed(self) -> float:
		"""
		Return the speed of the motor 1.\n
		`return` : int, a number between 0 and 1. 0 stop, 1 full speed.
		"""
		return self._motor1Speed

	def SetMotor2Speed(self, speed : float):
		"""
		Set the speed of the motor 2.\n
		`speed` : int, take a number between 0 and 1. 0 stop, 1 full speed.
		"""

		if(speed > 1) : speed = 1
		if(speed < 0) : speed = 0

		self._motor2Speed = speed
		self._motor2.forward(speed)
		pass
	
	def GetMotor2Speed(self) -> float:
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
	

	# def GetWaterLevelCuve1(self) -> int:
	# 	# return self.ConvertRawWaterValue(self.cuve1.value)
	# 	return ( self.ads.readADC(0) - self.CUVE_1_MIN) / ( self.CUVE_1_MAX - self.CUVE_1_MIN ) 
	
	def GetWaterLevelCuve1(self) -> float:
		# return self.ConvertRawWaterValue(self.cuve1.value)
		# Le 5.8838 vient de la conversion 60cm d'eau en kPa, 1 cm d'eau c 0.058838 bar.
		val = self.ads.readADC_Differential_0_1()
		print(f"Raw value : {val}")
		return val / (5.8838 * 25 * ( 32767 / 256 ) )

	def GetWaterLevelCuve2(self) -> float:
		# return self.ConvertRawWaterValue(self.cuve2.value)
		return ( self.ads.readADC(1) - self.CUVE_2_MIN) / ( self.CUVE_2_MAX - self.CUVE_2_MIN ) 
	
	def GetWaterLevelCuve3(self) -> float:
		# return self.ConvertRawWaterValue(self.cuve3.value)
		return ( self.ads.readADC(2) - self.CUVE_3_MIN) / ( self.CUVE_3_MAX - self.CUVE_3_MIN ) 
	

	def CanMotorRun(self, waterLevels : list[float]) : 
		maxValue = max(waterLevels)
		return maxValue < self.WATER_LEVEL_MAX

