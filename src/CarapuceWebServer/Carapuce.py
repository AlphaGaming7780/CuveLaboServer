from gpiozero import Motor
from gpiozero import LED

from Common.LaboBase import LaboBase

# https://github.com/chandrawi/ADS1x15-ADC
from ADS1x15 import ADS1115

class Carapuce(LaboBase):

	NUMBER_OF_CUVE = 1

	ads : ADS1115

	def __init__(self):
		super().__init__(self.NUMBER_OF_CUVE, [ Motor(17, 27) ], waterMaxLevel=0.8 )

		self.ads = ADS1115(1)
		self.ads.setGain(self.ads.PGA_0_256V)
		self.ads.setMode(self.ads.MODE_SINGLE)
		pass
	
	def GetWaterLevels(self) -> list[float]:
		return [self.GetWaterLevel1()]
	
	def GetWaterLevel1(self) -> float : 
		val = self.ads.readADC_Differential_0_1()
		return self.ConvertADCValue(val)

