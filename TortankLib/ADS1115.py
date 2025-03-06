from B_I2C import I2C

ADS1115_ADDRESS_ADDR_GND	= 0x48 # address pin low (GND)
ADS1115_ADDRESS_ADDR_VDD	= 0x49 # address pin high (VCC)
ADS1115_ADDRESS_ADDR_SDA	= 0x4A # address pin tied to SDA pin
ADS1115_ADDRESS_ADDR_SCL	= 0x4B # address pin tied to SCL pin
ADS1115_DEFAULT_ADDRESS		= ADS1115_ADDRESS_ADDR_GND

ADS1115_RA_CONVERSION       = 0x00
ADS1115_RA_CONFIG           = 0x01
ADS1115_RA_LO_THRESH        = 0x02
ADS1115_RA_HI_THRESH        = 0x03

ADS1115_CFG_OS_BIT          = 15
ADS1115_CFG_MUX_BIT         = 14
ADS1115_CFG_MUX_LENGTH      = 3
ADS1115_CFG_PGA_BIT         = 11
ADS1115_CFG_PGA_LENGTH      = 3
ADS1115_CFG_MODE_BIT        = 8
ADS1115_CFG_DR_BIT          = 7
ADS1115_CFG_DR_LENGTH       = 3
ADS1115_CFG_COMP_MODE_BIT 	= 4
ADS1115_CFG_COMP_POL_BIT	= 3
ADS1115_CFG_COMP_LAT_BIT	= 2
ADS1115_CFG_COMP_QUE_BIT	= 1
ADS1115_CFG_COMP_QUE_LENGTH = 2

ADS1115_MUX_P0_N1	= 0x00 # default
ADS1115_MUX_P0_N3	= 0x01
ADS1115_MUX_P1_N3	= 0x02
ADS1115_MUX_P2_N3	= 0x03
ADS1115_MUX_P0_NG	= 0x04
ADS1115_MUX_P1_NG	= 0x05
ADS1115_MUX_P2_NG	= 0x06
ADS1115_MUX_P3_NG	= 0x07

ADS1115_PGA_6P144	= 0x00
ADS1115_PGA_4P096	= 0x01
ADS1115_PGA_2P048	= 0x02 # default
ADS1115_PGA_1P024	= 0x03
ADS1115_PGA_0P512	= 0x04
ADS1115_PGA_0P256	= 0x05
ADS1115_PGA_0P256B	= 0x06
ADS1115_PGA_0P256C	= 0x07

ADS1115_MV_6P144	= 0.187500
ADS1115_MV_4P096	= 0.125000
ADS1115_MV_2P048	= 0.062500 # default
ADS1115_MV_1P024	= 0.031250
ADS1115_MV_0P512	= 0.015625
ADS1115_MV_0P256	= 0.007813
ADS1115_MV_0P256B	= 0.007813 
ADS1115_MV_0P256C	= 0.007813

ADS1115_MODE_CONTINUOUS	= 0x00
ADS1115_MODE_SINGLESHOT	= 0x01 # default

ADS1115_RATE_8		= 0x00
ADS1115_RATE_16		= 0x01
ADS1115_RATE_32		= 0x02
ADS1115_RATE_64		= 0x03
ADS1115_RATE_128	= 0x04 # default
ADS1115_RATE_250	= 0x05
ADS1115_RATE_475	= 0x06
ADS1115_RATE_860	= 0x07

ADS1115_COMP_MODE_HYSTERESIS	= 0x00 # default
ADS1115_COMP_MODE_WINDOW		= 0x01

ADS1115_COMP_POL_ACTIVE_LOW		= 0x00 # default
ADS1115_COMP_POL_ACTIVE_HIGH	= 0x01

ADS1115_COMP_LAT_NON_LATCHING	= 0x00 # default
ADS1115_COMP_LAT_LATCHING		= 0x01

ADS1115_COMP_QUE_ASSERT1		= 0x00
ADS1115_COMP_QUE_ASSERT2		= 0x01
ADS1115_COMP_QUE_ASSERT4		= 0x02
ADS1115_COMP_QUE_DISABLE		= 0x03 # default

I2CDEV_DEFAULT_READ_TIMEOUT		= 1000



class ADS1115 :

	devAddr : bytes
	# buffer 	= [int, int]
	devMode : bool
	muxMode : bytes
	pgaMode : bytes

	i2c : I2C

	def __init__(self, device_adress = ADS1115_DEFAULT_ADDRESS):
		self.devAddr = device_adress
		self.i2c = I2C(device_adress)
		self.setMultiplexer(ADS1115_MUX_P0_N1)
		self.setGain(ADS1115_PGA_2P048)
		self.setMode(ADS1115_MODE_SINGLESHOT)
		self.setRate(ADS1115_RATE_128)
		self.setComparatorMode(ADS1115_COMP_MODE_HYSTERESIS)
		self.setComparatorPolarity(ADS1115_COMP_POL_ACTIVE_LOW)
		self.setComparatorLatchEnabled(ADS1115_COMP_LAT_NON_LATCHING)
		self.setComparatorQueueMode(ADS1115_COMP_QUE_DISABLE)

	def testConnection(self) -> bool :
		return self.i2c.read16(ADS1115_RA_CONVERSION) > 0
	
	def pollConversion(self, max_retries : int) -> bool : 
		for x in range(max_retries) : 
			if (self.isConversionReady()) :
				return True
		return False
	
	# Read differential value based on current MUX configuration.
	# The default MUX setting sets the device to get the differential between the
	# AIN0 and AIN1 pins. There are 8 possible MUX settings, but if you are using
	# all four input pins as single-end voltage sensors, then the default option is
	# not what you want; instead you will need to set the MUX to compare the
	# desired AIN# pin with GND. There are shortcut methods (getConversion#) to do
	# this conveniently, but you can also do it manually with setMultiplexer()
	# followed by this method.
	#
	# In single-shot mode, this register may not have fresh data. You need to write
	# a 1 bit to the MSB of the CONFIG register to trigger a single read/conversion
	# before this will be populated with fresh data. This technique is not as
	# effortless, but it has enormous potential to save power by only running the
	# comparison circuitry when needed.
	#
	# @param triggerAndPoll If true (and only in singleshot mode) the conversion trigger 
	#        will be executed and the conversion results will be polled.
	# @return 16-bit signed differential value
	# @see getConversionP0N1();
	# @see getConversionPON3();
	# @see getConversionP1N3();
	# @see getConversionP2N3();
	# @see getConversionP0GND();
	# @see getConversionP1GND();
	# @see getConversionP2GND();
	# @see getConversionP3GND);
	# @see setMultiplexer();
	# @see ADS1115_RA_CONVERSION
	# @see ADS1115_MUX_P0_N1
	# @see ADS1115_MUX_P0_N3
	# @see ADS1115_MUX_P1_N3
	# @see ADS1115_MUX_P2_N3
	# @see ADS1115_MUX_P0_NG
	# @see ADS1115_MUX_P1_NG
	# @see ADS1115_MUX_P2_NG
	# @see ADS1115_MUX_P3_NG

	def getConversion(self, triggerAndPoll : bool) -> int :
		if (triggerAndPoll & self.devMode == ADS1115_MODE_SINGLESHOT) :
			self.triggerConversion()
			self.pollConversion(I2CDEV_DEFAULT_READ_TIMEOUT) 
		return self.i2c.read16(ADS1115_RA_CONVERSION)
	
	# Get AIN0/N1 differential.
	# This changes the MUX setting to AIN0/N1 if necessary, triggers a new
	# measurement (also only if necessary), then gets the differential value
	# currently in the CONVERSION register.
	# @return 16-bit signed differential value
	# @see getConversion()

	def getConversionP0N1(self) -> int :
		if (self.muxMode != ADS1115_MUX_P0_N1) : 
			self.setMultiplexer(ADS1115_MUX_P0_N1)
		return self.getConversion()
	
	# Get AIN0/N3 differential.
	# This changes the MUX setting to AIN0/N3 if necessary, triggers a new
	# measurement (also only if necessary), then gets the differential value
	# currently in the CONVERSION register.
	# @return 16-bit signed differential value
	# @see getConversion()

	def getConversionP0N3(self) -> int :
		if (self.muxMode != ADS1115_MUX_P0_N3) : 
			self.setMultiplexer(ADS1115_MUX_P0_N3)
		return self.getConversion()

	# Get AIN1/N3 differential.
	# This changes the MUX setting to AIN1/N3 if necessary, triggers a new
	# measurement (also only if necessary), then gets the differential value
	# currently in the CONVERSION register.
	# @return 16-bit signed differential value
	# @see getConversion()

	def getConversionP1N3(self) -> int :
		if (self.muxMode != ADS1115_MUX_P1_N3) : 
			self.setMultiplexer(ADS1115_MUX_P1_N3)
		return self.getConversion()
	
	# Get AIN2/N3 differential.
	# This changes the MUX setting to AIN2/N3 if necessary, triggers a new
	# measurement (also only if necessary), then gets the differential value
	# currently in the CONVERSION register.
	# @return 16-bit signed differential value
	# @see getConversion()

	def getConversionP2N3(self) -> int :
		if (self.muxMode != ADS1115_MUX_P2_N3) :
			self.setMultiplexer(ADS1115_MUX_P2_N3)
		return self.getConversion()
	
	# Get AIN0/GND differential.
	# This changes the MUX setting to AIN0/GND if necessary, triggers a new
	# measurement (also only if necessary), then gets the differential value
	# currently in the CONVERSION register.
	# @return 16-bit signed differential value
	# @see getConversion()

	def getConversionP0GND(self) -> int :
		if (self.muxMode != ADS1115_MUX_P0_NG) :
			self.setMultiplexer(ADS1115_MUX_P0_NG)
		return self.getConversion()
	
	# Get AIN1/GND differential.
	# This changes the MUX setting to AIN1/GND if necessary, triggers a new
	# measurement (also only if necessary), then gets the differential value
	# currently in the CONVERSION register.
	# @return 16-bit signed differential value
	# @see getConversion()

	def getConversionP1GND(self) -> int :
		if (self.muxMode != ADS1115_MUX_P1_NG) : 
			self.setMultiplexer(ADS1115_MUX_P1_NG)
		return self.getConversion()
	
	# Get AIN2/GND differential.
	# This changes the MUX setting to AIN2/GND if necessary, triggers a new
	# measurement (also only if necessary), then gets the differential value
	# currently in the CONVERSION register.
	# @return 16-bit signed differential value
	# @see getConversion()

	def getConversionP2GND(self) -> int :
		if (self.muxMode != ADS1115_MUX_P2_NG) :
			self.setMultiplexer(ADS1115_MUX_P2_NG)
		return self.getConversion()
	
	# Get AIN3/GND differential.
	# This changes the MUX setting to AIN3/GND if necessary, triggers a new
	# measurement (also only if necessary), then gets the differential value
	# currently in the CONVERSION register.
	# @return 16-bit signed differential value
	# @see getConversion()

	def getConversionP3GND(self) -> int :
		if (self.muxMode != ADS1115_MUX_P3_NG) :
			self.setMultiplexer(ADS1115_MUX_P3_NG)
		return self.getConversion()
	
	# Get the current voltage reading
	# Read the current differential and return it multiplied
	# by the constant for the current gain.  mV is returned to
	# increase the precision of the voltage
	# @param triggerAndPoll If true (and only in singleshot mode) the conversion trigger 
	#        will be executed and the conversion results will be polled.

	def getMilliVolts(self, triggerAndPoll : bool) -> float :
		if(self.pgaMode == ADS1115_PGA_6P144) :
			return (self.getConversion(triggerAndPoll) * ADS1115_MV_6P144)
		elif(self.pgaMode == ADS1115_PGA_4P096) :
			return (self.getConversion(triggerAndPoll) * ADS1115_MV_4P096)
		elif(self.pgaMode == ADS1115_PGA_2P048) :
			return (self.getConversion(triggerAndPoll) * ADS1115_MV_2P048)
		elif(self.pgaMode == ADS1115_PGA_1P024) :
			return (self.getConversion(triggerAndPoll) * ADS1115_MV_1P024)
		elif(self.pgaMode == ADS1115_PGA_0P512) :
			return (self.getConversion(triggerAndPoll) * ADS1115_MV_0P512)
		elif(self.pgaMode == ADS1115_PGA_0P256 | self.pgaMode == ADS1115_PGA_0P256B | self.pgaMode == ADS1115_PGA_0P256C) :
			return (self.getConversion(triggerAndPoll) * ADS1115_MV_0P256)

	# Return the current multiplier for the PGA setting.
	# 
	# This may be directly retreived by using getMilliVolts(),
	# but this causes an independent read.  This function could
	# be used to average a number of reads from the getConversion()
	# getConversionx() functions and cut downon the number of 
	# floating-point calculations needed.

	def getMvPerCount(self) -> float :
		if(self.pgaMode == ADS1115_PGA_6P144) :
			return ADS1115_MV_6P144
		elif(self.pgaMode == ADS1115_PGA_4P096) :
			return  ADS1115_MV_4P096
		elif(self.pgaMode == ADS1115_PGA_2P048) :
			return ADS1115_MV_2P048
		elif(self.pgaMode == ADS1115_PGA_1P024) :
			return ADS1115_MV_1P024
		elif(self.pgaMode == ADS1115_PGA_0P512) :
			return ADS1115_MV_0P512
		elif(self.pgaMode == ADS1115_PGA_0P256 | self.pgaMode == ADS1115_PGA_0P256B | self.pgaMode == ADS1115_PGA_0P256C) :
			return ADS1115_MV_0P256
		
	# CONFIG register

	# Get operational status.
	# @return Current operational status (false for active conversion, true for inactive)
	# @see ADS1115_RA_CONFIG
	# @see ADS1115_CFG_OS_BIT

	def isConversionReady(self) -> bool :
		return self.i2c.readBitW(ADS1115_RA_CONFIG, ADS1115_CFG_OS_BIT)
	
	# Trigger a new conversion.
	# Writing to this bit will only have effect while in power-down mode (no conversions active).
	# @see ADS1115_RA_CONFIG
	# @see ADS1115_CFG_OS_BIT

	def triggerConversion(self) :
		self.i2c.writeBitW(ADS1115_RA_CONFIG, ADS1115_CFG_OS_BIT, 1)

	# Get multiplexer connection.
	# @return Current multiplexer connection setting
	# @see ADS1115_RA_CONFIG
	# @see ADS1115_CFG_MUX_BIT
	# @see ADS1115_CFG_MUX_LENGTH

	def getMultiplexer(self) -> int :
		return self.i2c.readBitsW(ADS1115_RA_CONFIG, ADS1115_CFG_MUX_BIT, ADS1115_CFG_MUX_LENGTH)

	# Set multiplexer connection.  Continous mode may fill the conversion register
	# with data before the MUX setting has taken effect.  A stop/start of the conversion
	# is done to reset the values.
	# @param mux New multiplexer connection setting
	# @see ADS1115_MUX_P0_N1
	# @see ADS1115_MUX_P0_N3
	# @see ADS1115_MUX_P1_N3
	# @see ADS1115_MUX_P2_N3
	# @see ADS1115_MUX_P0_NG
	# @see ADS1115_MUX_P1_NG
	# @see ADS1115_MUX_P2_NG
	# @see ADS1115_MUX_P3_NG
	# @see ADS1115_RA_CONFIG
	# @see ADS1115_CFG_MUX_BIT
	# @see ADS1115_CFG_MUX_LENGTH

	def setMultiplexer(self, mux) :
		# if (I2Cdev::writeBitsW(devAddr, ADS1115_RA_CONFIG, ADS1115_CFG_MUX_BIT, ADS1115_CFG_MUX_LENGTH, mux)) {
		self.i2c.writeBitsW(ADS1115_RA_CONFIG, ADS1115_CFG_MUX_BIT, ADS1115_CFG_MUX_LENGTH, mux)
		self.muxMode = mux
		if (self.devMode == ADS1115_MODE_CONTINUOUS) :
        #  Force a stop/start
			self.setMode(ADS1115_MODE_SINGLESHOT)
			self.getConversion()
			self.setMode(ADS1115_MODE_CONTINUOUS)
    
	# Get programmable gain amplifier level.
	# @return Current programmable gain amplifier level
	# @see ADS1115_RA_CONFIG
	# @see ADS1115_CFG_PGA_BIT
	# @see ADS1115_CFG_PGA_LENGTH

	def getGain(self) -> bytes :
		self.pgaMode = self.i2c.readBitsW(ADS1115_RA_CONFIG, ADS1115_CFG_PGA_BIT, ADS1115_CFG_PGA_LENGTH)
		return self.pgaMode

	# Set programmable gain amplifier level.  
	# Continous mode may fill the conversion register
	# with data before the gain setting has taken effect.  A stop/start of the conversion
	# is done to reset the values.
	# @param gain New programmable gain amplifier level
	# @see ADS1115_PGA_6P144
	# @see ADS1115_PGA_4P096
	# @see ADS1115_PGA_2P048
	# @see ADS1115_PGA_1P024
	# @see ADS1115_PGA_0P512
	# @see ADS1115_PGA_0P256
	# @see ADS1115_RA_CONFIG
	# @see ADS1115_CFG_PGA_BIT
	# @see ADS1115_CFG_PGA_LENGTH

	def setGain(self, gain : bytes) :
		self.i2c.writeBitsW(ADS1115_RA_CONFIG, ADS1115_CFG_PGA_BIT, ADS1115_CFG_PGA_LENGTH, gain)
		self.pgaMode = gain
		if (self.devMode == ADS1115_MODE_CONTINUOUS) :
            # Force a stop/start
			self.setMode(ADS1115_MODE_SINGLESHOT)
			self.getConversion()
			self.setMode(ADS1115_MODE_CONTINUOUS)

	# Get device mode.
	# @return Current device mode
	# @see ADS1115_MODE_CONTINUOUS
	# @see ADS1115_MODE_SINGLESHOT
	# @see ADS1115_RA_CONFIG
	# @see ADS1115_CFG_MODE_BIT

	def getMode(self) -> bool :
		self.devMode = self.i2c.readBitW(ADS1115_RA_CONFIG, ADS1115_CFG_MODE_BIT)
		return self.devMode

	#  Set device mode.
	# @param mode New device mode
	# @see ADS1115_MODE_CONTINUOUS
	# @see ADS1115_MODE_SINGLESHOT
	# @see ADS1115_RA_CONFIG
	# @see ADS1115_CFG_MODE_BIT

	def setMode(self, mode : bool) :
		self.i2c.writeBitW(ADS1115_RA_CONFIG, ADS1115_CFG_MODE_BIT, mode)
		self.devMode = mode

	#  Get data rate.
	# @return Current data rate
	# @see ADS1115_RA_CONFIG
	# @see ADS1115_CFG_DR_BIT
	# @see ADS1115_CFG_DR_LENGTH

	def getRate(self) -> bytes :
		return self.i2c.readBitsW(ADS1115_RA_CONFIG, ADS1115_CFG_DR_BIT, ADS1115_CFG_DR_LENGTH)

	# Set data rate.
	# @param rate New data rate
	# @see ADS1115_RATE_8
	# @see ADS1115_RATE_16
	# @see ADS1115_RATE_32
	# @see ADS1115_RATE_64
	# @see ADS1115_RATE_128
	# @see ADS1115_RATE_250
	# @see ADS1115_RATE_475
	# @see ADS1115_RATE_860
	# @see ADS1115_RA_CONFIG
	# @see ADS1115_CFG_DR_BIT
	# @see ADS1115_CFG_DR_LENGTH

	def setRate(self, rate : bytes) :
		self.i2c.writeBitsW(ADS1115_RA_CONFIG, ADS1115_CFG_DR_BIT, ADS1115_CFG_DR_LENGTH, rate)

	# Get comparator mode.
	# @return Current comparator mode
	# @see ADS1115_COMP_MODE_HYSTERESIS
	# @see ADS1115_COMP_MODE_WINDOW
	# @see ADS1115_RA_CONFIG
	# @see ADS1115_CFG_COMP_MODE_BIT

	def getComparatorMode(self) -> bool :
		return self.i2c.readBitW(ADS1115_RA_CONFIG, ADS1115_CFG_COMP_MODE_BIT)

	# Set comparator mode.
	# @param mode New comparator mode
	# @see ADS1115_COMP_MODE_HYSTERESIS
	# @see ADS1115_COMP_MODE_WINDOW
	# @see ADS1115_RA_CONFIG
	# @see ADS1115_CFG_COMP_MODE_BIT

	def setComparatorMode(self, mode : bool) :
		self.i2c.writeBitW(ADS1115_RA_CONFIG, ADS1115_CFG_COMP_MODE_BIT, mode)

	# Get comparator polarity setting.
	# @return Current comparator polarity setting
	# @see ADS1115_COMP_POL_ACTIVE_LOW
	# @see ADS1115_COMP_POL_ACTIVE_HIGH
	# @see ADS1115_RA_CONFIG
	# @see ADS1115_CFG_COMP_POL_BIT

	def getComparatorPolarity(self) -> bool :
		return self.i2c.readBitW(ADS1115_RA_CONFIG, ADS1115_CFG_COMP_POL_BIT)

	# Set comparator polarity setting.
	# @param polarity New comparator polarity setting
	# @see ADS1115_COMP_POL_ACTIVE_LOW
	# @see ADS1115_COMP_POL_ACTIVE_HIGH
	# @see ADS1115_RA_CONFIG
	# @see ADS1115_CFG_COMP_POL_BIT

	def setComparatorPolarity(self, polarity : bool) :
		self.i2c.writeBitW(ADS1115_RA_CONFIG, ADS1115_CFG_COMP_POL_BIT, polarity)

	# Get comparator latch enabled value.
	# @return Current comparator latch enabled value
	# @see ADS1115_COMP_LAT_NON_LATCHING
	# @see ADS1115_COMP_LAT_LATCHING
	# @see ADS1115_RA_CONFIG
	# @see ADS1115_CFG_COMP_LAT_BIT

	def getComparatorLatchEnabled(self) -> bool :
		return self.i2c.readBitW(ADS1115_RA_CONFIG, ADS1115_CFG_COMP_LAT_BIT)

	# Set comparator latch enabled value.
	# @param enabled New comparator latch enabled value
	# @see ADS1115_COMP_LAT_NON_LATCHING
	# @see ADS1115_COMP_LAT_LATCHING
	# @see ADS1115_RA_CONFIG
	# @see ADS1115_CFG_COMP_LAT_BIT

	def setComparatorLatchEnabled(self, enabled : bool) :
		self.i2c.writeBitW(ADS1115_RA_CONFIG, ADS1115_CFG_COMP_LAT_BIT, enabled)

	# Get comparator queue mode.
	# @return Current comparator queue mode
	# @see ADS1115_COMP_QUE_ASSERT1
	# @see ADS1115_COMP_QUE_ASSERT2
	# @see ADS1115_COMP_QUE_ASSERT4
	# @see ADS1115_COMP_QUE_DISABLE
	# @see ADS1115_RA_CONFIG
	# @see ADS1115_CFG_COMP_QUE_BIT
	# @see ADS1115_CFG_COMP_QUE_LENGTH

	def getComparatorQueueMode(self) -> bytes :
		return self.i2c.readBitsW(ADS1115_RA_CONFIG, ADS1115_CFG_COMP_QUE_BIT, ADS1115_CFG_COMP_QUE_LENGTH)

	# Set comparator queue mode.
	# @param mode New comparator queue mode
	# @see ADS1115_COMP_QUE_ASSERT1
	# @see ADS1115_COMP_QUE_ASSERT2
	# @see ADS1115_COMP_QUE_ASSERT4
	# @see ADS1115_COMP_QUE_DISABLE
	# @see ADS1115_RA_CONFIG
	# @see ADS1115_CFG_COMP_QUE_BIT
	# @see ADS1115_CFG_COMP_QUE_LENGTH

	def setComparatorQueueMode(self, mode : bytes) :
		self.i2c.writeBitsW(ADS1115_RA_CONFIG, ADS1115_CFG_COMP_QUE_BIT, ADS1115_CFG_COMP_QUE_LENGTH, mode)


	# *_THRESH registers

	# Get low threshold value.
	# @return Current low threshold value
	# @see ADS1115_RA_LO_THRESH

	def getLowThreshold(self) -> int :
		return self.i2c.read16(ADS1115_RA_LO_THRESH)

	# Set low threshold value.
	# @param threshold New low threshold value
	# @see ADS1115_RA_LO_THRESH

	def setLowThreshold(self, threshold : int) :
		self.i2c.write16(ADS1115_RA_LO_THRESH, threshold)

	# Get high threshold value.
	# @return Current high threshold value
	# @see ADS1115_RA_HI_THRESH

	def getHighThreshold(self) -> int :
		return self.i2c.read16(ADS1115_RA_HI_THRESH)

	# Set high threshold value.
	# @param threshold New high threshold value
	# @see ADS1115_RA_HI_THRESH

	def setHighThreshold(self, threshold : int) :
		self.i2c.write16(ADS1115_RA_HI_THRESH, threshold)


	#  Configures ALERT/RDY pin as a conversion ready pin.
	#  It does this by setting the MSB of the high threshold register to '1' and the MSB 
	#  of the low threshold register to '0'. COMP_POL and COMP_QUE bits will be set to '0'.
	#  Note: ALERT/RDY pin requires a pull up resistor.

	def setConversionReadyPinMode(self) :
		self.i2c.writeBitW(ADS1115_RA_HI_THRESH, 15, 1)
		self.i2c.writeBitW(ADS1115_RA_LO_THRESH, 15, 0)
		self.setComparatorPolarity(0)
		self.setComparatorQueueMode(0)

	# Create a mask between two bits
	def createMask(a : int, b : int) -> int :
		mask : int = 0
		for x in range (a, b) :
			mask |= 1 << x
		return mask

	def shiftDown(extractFrom : int, places : int) -> int :
		return (extractFrom >> places)

	def getValueFromBits(self, extractFrom : int, high : int, length : int) -> int :
		low : int = high-length +1
		mask : int = self.createMask(low ,high)
		return self.shiftDown(extractFrom & mask, low)

	# Show all the config register settings

	def showConfigRegister(self) :
		uconfigRegister : int = self.i2c.read16(ADS1115_RA_CONFIG)
     
    # #ifdef ADS1115_SERIAL_DEBUG
	# 	Serial.print("Register is:");
	# 	Serial.println(configRegister,BIN);

	# 	Serial.print("OS:\t");
	# 	Serial.println(getValueFromBits(configRegister, 
	# 	ADS1115_CFG_OS_BIT,1), BIN);
	# 	Serial.print("MUX:\t");
	# 	Serial.println(getValueFromBits(configRegister,  
	# 	ADS1115_CFG_MUX_BIT,ADS1115_CFG_MUX_LENGTH), BIN);

	# 	Serial.print("PGA:\t");
	# 	Serial.println(getValueFromBits(configRegister, 
	# 	ADS1115_CFG_PGA_BIT,ADS1115_CFG_PGA_LENGTH), BIN);

	# 	Serial.print("MODE:\t");
	# 	Serial.println(getValueFromBits(configRegister,
	# 	ADS1115_CFG_MODE_BIT,1), BIN);

	# 	Serial.print("DR:\t");
	# 	Serial.println(getValueFromBits(configRegister, 
	# 	ADS1115_CFG_DR_BIT,ADS1115_CFG_DR_LENGTH), BIN);

	# 	Serial.print("CMP_MODE:\t");
	# 	Serial.println(getValueFromBits(configRegister, 
	# 	ADS1115_CFG_COMP_MODE_BIT,1), BIN);

	# 	Serial.print("CMP_POL:\t");
	# 	Serial.println(getValueFromBits(configRegister, 
	# 	ADS1115_CFG_COMP_POL_BIT,1), BIN);

	# 	Serial.print("CMP_LAT:\t");
	# 	Serial.println(getValueFromBits(configRegister, 
	# 	ADS1115_CFG_COMP_LAT_BIT,1), BIN);

	# 	Serial.print("CMP_QUE:\t");
	# 	Serial.println(getValueFromBits(configRegister, 
	# 	ADS1115_CFG_COMP_QUE_BIT,ADS1115_CFG_COMP_QUE_LENGTH), BIN);
    # #endif
