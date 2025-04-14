from abc import *
from gpiozero import Motor
from gpiozero import LED

# https://github.com/chandrawi/ADS1x15-ADC
from ADS1x15 import ADS1115

class LaboBase(object):

	_WaterMaxLevel : float
	_NbCuve : int
	_NbMotor : int
	_Motors : list[Motor]
	_MotorsCurrentSpeed : list[float] = []

	def __init__(self, nbCuve : int, motors : list[Motor], waterMaxLevel : float = 0.95, useOldCapteur : bool = False):
		self._NbCuve = nbCuve
		self._Motors = motors
		self._NbMotor = motors.__len__()
		self._WaterMaxLevel = waterMaxLevel
		self._UseOldCapteur = useOldCapteur

		for i in range(0, motors.__len__()):
			self._MotorsCurrentSpeed.append(0)

		pass
	
	@abstractmethod
	def GetWaterLevels(self) -> list[float]:
		raise NotImplementedError("Subclass must implement abstract method")
	
	def CanMotorRun(self, waterLevels : list[float]) -> bool :
		maxValue = max(waterLevels)
		return maxValue < self._WaterMaxLevel

	def GetMotorsSpeed(self) -> list[float]:

		data : list[float]	= []
		for i in range(0, self._NbMotor):
			data.append(self._MotorsCurrentSpeed[i])

		return data

	def SetMotorSpeed(self, motorIdx : int, speed : float):
		if(motorIdx < 0 or motorIdx >= self._NbMotor): return

		if(speed > 1) : speed = 1
		if(speed < 0) : speed = 0

		self._Motors[motorIdx].forward(speed)
		self._MotorsCurrentSpeed[motorIdx] = speed

		pass

	def GetMotorSpeed(self, motorIdx : int) -> float :
		if(motorIdx < 0 or motorIdx >= self._NbMotor): return -1
		return self._MotorsCurrentSpeed[motorIdx]
	
	def StopAllMotors(self):
		for i in range(0, self._NbMotor):
			self._Motors[i].stop()
			self._MotorsCurrentSpeed[i] = 0

	def Reset(self):
		self.StopAllMotors()

	def ConvertADCValue(self, val : float) -> float:
		if(self._UseOldCapteur) : 
			return val / (60 * 73 * ( 32767 / 4096 ) )
		else: 
			return val / (5.8838 * 2.5 * ( 32767 / 256 ) )