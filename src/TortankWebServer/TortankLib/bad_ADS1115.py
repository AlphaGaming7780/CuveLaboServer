import smbus2
import time

# Adresse I2C par défaut de l'ADS1115 (modifiable selon le câblage)
ADS1115_ADDR = 0x48

# Pointeurs de registres
REG_CONVERSION = 0x00
REG_CONFIG = 0x01

# Configuration du gain (FSR = 4.096V)
GAIN = 0x0200  # ±4.096V

# Configuration du mode et de la fréquence d'échantillonnage
MODE_SINGLE_SHOT = 0x0100  # Mode single-shot
SPS_128 = 0x0080  # 128 échantillons par seconde

# Configuration du canal d'entrée (canal AIN0)
MUX_AIN0 = 0x4000  # AIN0 par rapport à GND

# Bus I2C
bus = smbus2.SMBus(1)

class ADS1115(object):
	def read_adc(self, channel=0):
		"""Lit une valeur analogique sur le canal spécifié de l'ADS1115"""
		if channel == 0:
			mux = MUX_AIN0
		elif channel == 1:
			mux = 0x5000  # AIN1
		elif channel == 2:
			mux = 0x6000  # AIN2
		elif channel == 3:
			mux = 0x7000  # AIN3
		else:
			raise ValueError("Canal invalide. Choisir entre 0 et 3.")

		# Configuration du registre
		config = (
			0x8000 |  # Bit de départ
			mux |  # Sélection du canal
			GAIN |  # Gain
			MODE_SINGLE_SHOT |  # Mode single-shot
			SPS_128 |  # Vitesse d'échantillonnage
			0x0003  # Mode de lecture (comparateur désactivé)
		)

		# Écriture de la configuration
		config_bytes = [(config >> 8) & 0xFF, config & 0xFF]
		bus.write_i2c_block_data(ADS1115_ADDR, REG_CONFIG, config_bytes)

		# Attente de la conversion (8ms suffisent pour 128SPS)
		time.sleep(0.01)

		# Lecture de la conversion
		data = bus.read_i2c_block_data(ADS1115_ADDR, REG_CONVERSION, 2)
		raw_adc = (data[0] << 8) | data[1]

		# Gestion du signe (valeur sur 16 bits, en complément à 2)
		if raw_adc > 0x7FFF:
			raw_adc -= 0x10000

		# Calcul de la tension (FSR de ±4.096V -> résolution de 0.125 mV/bit)
		voltage = raw_adc / 32768.0 * 4.096
		return voltage
	
	def getConversionP0GND(self) -> int :
		return self.read_adc(0)

	def getConversionP1GND(self) -> int :
		return self.read_adc(1)

	def getConversionP2GND(self) -> int :
		return self.read_adc(2)

