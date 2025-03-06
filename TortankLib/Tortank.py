from gpiozero import Motor

class Tortank(object):
    
    _motor1 : Motor
    _motor2 : Motor

    _motor1Speed : int
    _motor2Speed : int

    def __init__(self):
        self._motor1 = Motor(17, 27)
        self._motor2 = Motor(23, 24)
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

    def GetWaterLevel(self) -> int:
        pass

    pass