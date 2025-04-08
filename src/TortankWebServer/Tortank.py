from gpiozero import Motor
from gpiozero import LED

# https://github.com/chandrawi/ADS1x15-ADC
from ADS1x15 import ADS1115

from Common.LaboBase import LaboBase


class Tortank(LaboBase):

	_motor1 : Motor
	_motor2 : Motor


	ads1 : ADS1115
	ads2 : ADS1115

	def __init__(self):
		super().__init__(3, [ Motor(17, 27), Motor(23, 24) ])

		self.ads1 = ADS1115(1)
		self.ads1.setGain(self.ads1.PGA_0_256V)
		self.ads1.setMode(self.ads1.MODE_SINGLE)

		self.ads2 = ADS1115(1, 0x49)
		self.ads2.setGain(self.ads2.PGA_0_256V)
		self.ads2.setMode(self.ads2.MODE_SINGLE)
		pass

	def GetWaterLevels(self) -> list[float]:
		return [self.GetWaterLevel1(), self.GetWaterLevel2(), self.GetWaterLevel3()]
	
	def GetWaterLevel1(self) -> float : 
		val = self.ads1.readADC_Differential_0_1()
		print(f"Raw value : {val}")
		return val / (5.8838 * 2.5 * ( 32767 / 256 ) )
	
	def GetWaterLevel2(self) -> float : 
		val = self.ads1.readADC_Differential_2_3()
		print(f"Raw value : {val}")
		return val / (5.8838 * 2.5 * ( 32767 / 256 ) )
	
	def GetWaterLevel3(self) -> float : 
		val = self.ads2.readADC_Differential_0_1()
		print(f"Raw value : {val}")
		return val / (5.8838 * 2.5 * ( 32767 / 256 ) )
