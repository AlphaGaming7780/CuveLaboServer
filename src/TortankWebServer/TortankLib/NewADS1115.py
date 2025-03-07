from enum import Enum
from TortankWebServer.TortankLib.I2C import I2C
import time

ADS1115_ADDRESS_ADDR_GND	= 0x48 # address pin low (GND)
ADS1115_ADDRESS_ADDR_VDD	= 0x49 # address pin high (VCC)
ADS1115_ADDRESS_ADDR_SDA	= 0x4A # address pin tied to SDA pin
ADS1115_ADDRESS_ADDR_SCL	= 0x4B # address pin tied to SCL pin
ADS1115_DEFAULT_ADDRESS		= ADS1115_ADDRESS_ADDR_GND

class ADS1115_RA(Enum) :
	CONVERSION       = 0x00
	CONFIG           = 0x01
	LO_THRESH        = 0x02
	HI_THRESH        = 0x03

class ADS1115_CFG(Enum) :
	OS_BIT          = 15
	MUX_BIT         = 14
	MUX_LENGTH      = 3
	PGA_BIT         = 11
	PGA_LENGTH      = 3
	MODE_BIT        = 8
	DR_BIT          = 7
	DR_LENGTH       = 3
	COMP_MODE_BIT 	= 4
	COMP_POL_BIT	= 3
	COMP_LAT_BIT	= 2
	COMP_QUE_BIT	= 1
	COMP_QUE_LENGTH = 2

class ADS1115_MUX(Enum):
	P0_N1	= 0x00 # default
	P0_N3	= 0x01
	P1_N3	= 0x02
	P2_N3	= 0x03
	P0_NG	= 0x04
	P1_NG	= 0x05
	P2_NG	= 0x06
	P3_NG	= 0x07

class ADS1115_PGA(Enum):
	ADS1115_PGA_6P144	= 0x00
	ADS1115_PGA_4P096	= 0x01
	ADS1115_PGA_2P048	= 0x02 # default
	ADS1115_PGA_1P024	= 0x03
	ADS1115_PGA_0P512	= 0x04
	ADS1115_PGA_0P256	= 0x05
	ADS1115_PGA_0P256B	= 0x06
	ADS1115_PGA_0P256C	= 0x07

class ADS1115_MV(Enum) :
	MV_6P144	= 0.187500
	MV_4P096	= 0.125000
	MV_2P048	= 0.062500 # default
	MV_1P024	= 0.031250
	MV_0P512	= 0.015625
	MV_0P256	= 0.007813
	MV_0P256B	= 0.007813 
	MV_0P256C	= 0.007813

class ADS1115_MODE(Enum) :
	CONTINUOUS	= 0x00
	SINGLESHOT	= 0x01 # default

class ADS1115_RATE(Enum) : 
	RATE_8		= 0x00
	RATE_16		= 0x01
	RATE_32		= 0x02
	RATE_64		= 0x03
	RATE_128	= 0x04 # default
	RATE_250	= 0x05
	RATE_475	= 0x06
	RATE_860	= 0x07

class ADS1115_COMP_MODE(Enum) :
	HYSTERESIS	= 0x00 # default
	WINDOW		= 0x01

class ADS1115_COMP_POL_ACTIVE(Enum) :
	LOW		= 0x00 # default
	HIGH	= 0x01

class ADS1115_COMP_LAT(Enum) :
	NON_LATCHING	= 0x00 # default
	LATCHING		= 0x01

class ADS1115_COMP_QUE(Enum) :
	ASSERT1		= 0x00
	ASSERT2		= 0x01
	ASSERT4		= 0x02
	DISABLE		= 0x03 # default
	

