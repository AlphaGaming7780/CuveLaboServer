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
		
        # On peut pas utiliser le gain de 4.069v car la valeur max des capteurs dépasse 4.069v
		# ---------->Verifier si les calculs de maximums sont toujours correctes<-------------
		self.ads.gain = 2/3

        # DEPRECATED
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
		# il faut alors le convertir, en rendant le nombre positif en ajoutant 32.767 ---> Techniquement incorrecte
		# rawADC += 0x7FFF # Décommenter cette ligne si on récupère des nombres négatifs

		# Divisé par 65535 car on veut un nombre entre 0 et 1. ---> Incorrecte aussi
		# return rawADC / 65535
		
        # Bon, je suis allé lire la datasheet du composant et Texas Instrument nous dit qu'en positif uniquement la valeur max est 7FFFh
		
		# EXTRAIT DE LA DOC traduit de l'anglais
		# Les ADS111x fournissent des données sur 16 bits au format complément à deux (binary 2’s-complement).
        # Une entrée correspondant à l’échelle pleine positive (+FS) produit un code de sortie de 7FFFh.
        # Une entrée correspondant à l’échelle pleine négative (–FS) produit un code de sortie de 8000h.
        # La sortie se bloque à ces valeurs lorsque le signal dépasse l’échelle maximale.
		
        # Les mesures de signaux en mode entrée simple (single-ended), 
		# où VAINN = 0V et VAINP varie de 0V à +FS, 
		# n'utilisent que la plage de codes positifs, allant de 0000h à 7FFFh. 
        # Cependant, en raison du décalage (offset) interne du dispositif, 
		# l'ADS111x peut encore générer des codes négatifs lorsque VAINP est proche de 0V.
        # FIN DE L'EXTRAIT
		
		# En fait en positif, l'ADS1115 compte de 0 à 32 767
		# En négatif, l'ADS1115 décompte de 65 535 à 32 768
		# L'ADC peut donc envoyer des données négative random si l'entrée analogique est trop proche de 0 -> Data saute de 0 à 65 535
		# Dans notre cas on utilise une seule entrée donc on a seulement la plage positive
		# Donc la bonne formule serait (divisé par 32 767 car on souhaite obtenir une valeur comprise entre 0 et 1)
		return rawADC / 32767
        # Pour avoir des valeurs négatives, il faut utiliser le mode différentiel avec deux entrées 

	def GetWaterLevelCuve1(self) -> int:
		# return self.chan0.voltage   # raw data not affected by the gain
		# return self.chan0.value     # data affected by the gain
		return self.ConvertRawWaterValue(self.chan0.value)
	
        # DEPRECATED
        # return self.ads.getConversionP0GND() / 32768 / 4.096

	def GetWaterLevelCuve2(self) -> int:

		return self.ConvertRawWaterValue(self.chan1.value)
	
        # DEPRECATED
        # return self.ads.getConversionP1GND() / 32768 / 4.096
	
	def GetWaterLevelCuve3(self) -> int:
		return self.ConvertRawWaterValue(self.chan2.value)
	
        # DEPRECATED
		# return self.ads.getConversionP2GND() / 32768 / 4.096