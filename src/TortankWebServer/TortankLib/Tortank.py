from gpiozero import Motor
from TortankWebServer.TortankLib.ADS1115 import ADS1115, ADS1115_MODE, ADS1115_PGA

class Tortank(object):
    
    TORTANK_WATER_LEVEL_MAX = 0.95

    _motor1 : Motor
    _motor2 : Motor

    _motor1Speed : int
    _motor2Speed : int
    
    ads : ADS1115

    def __init__(self):
        self._motor1 = Motor(17, 27)
        self._motor2 = Motor(23, 24)
        self.ads = ADS1115()
        self.ads.setMode(ADS1115_MODE.SINGLESHOT)
        self.ads.setGain(ADS1115_PGA.ADS1115_PGA_4P096)
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

    def GetWaterLevelCuve1(self) -> int:
        return self.ads.getConversionP0GND()
    
    def GetWaterLevelCuve2(self) -> int:
        return self.ads.getConversionP1GND()
    
    def GetWaterLevelCuve3(self) -> int:
        return self.ads.getConversionP2GND()
    
    def GetHeigestWaterLevel(self) -> int:

        v1 = self.GetWaterLevelCuve1()
        v2 = self.GetWaterLevelCuve2()
        v3 = self.GetWaterLevelCuve3()
        
        return max(v1, v2, v3)

    pass