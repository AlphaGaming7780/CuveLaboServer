# from types import *
from smbus2 import SMBus

class I2C : 

    device_addr : bytes
    bus : SMBus

    def __init__(self, device_addr : bytes, bus_id : int = 1) -> None:
        self.device_addr = device_addr
        self.bus = SMBus(bus_id)

    def read8(self, reg : int) -> int: 
        return self.bus.read_byte_data(self.device_addr, reg)
    
    def write8(self, reg : int, val : int) -> None :
        self.bus.write_byte_data(self.device_addr, reg, val)
    
    def readBit(self, reg : int, bit : int) -> bool:
        return (self.read8(reg) & (1 << bit)) != 0
        # v = self.read8(reg)
        # mask = 1 << bit
        # return ( (v & mask) > 0 )

    def writeBit(self, reg : int, bit : int, value : bool) -> None:
        v = self.read8(reg)
        v = (v | (1 << bit)) if value else (v & ~(1 << bit))
        self.write8(reg, v)
        # if(value) : 
        #     v |= (1 << bit)
        # else :
        #     v &= ~(1 << bit)
        
        # self.write8(reg, value)
    
    def readBits(self, reg : int, startBit : int, size : int) -> int:
        v = self.read8(reg)
        mask = (1 << size) - 1
        return (v >> startBit) & mask
        # mask = 0

        # for i in range(size):
        #     mask = 1 + ( mask << 1 )

        # mask = mask << startBit

        # return ( (v & mask) >> startBit )

    def writeBits(self, reg : int, startBit : int, size : int, value : int) -> None: 
        read = self.read8(reg)
        mask = (1 << size) - 1
        read = (read & ~(mask << startBit)) | ((value & mask) << startBit)
        self.write8(reg, read)
        # mask = 0

        # for i in range(size):
        #     mask = 1 + ( mask << 1 )

        # mask = ( ~( mask << startBit ) ) & 0b11111111

        # read = read & mask

        # read += ( value << startBit )

        # self.write8(reg, read)

    def read16(self, reg : int) -> int :
        data1 = self.read8(reg)
        data2 = self.read8(reg + 1)
        return ( (data1 << 8 ) | data2 )

        # data = self.bus.read_word_data(self.device_addr, reg)
        # return ((data & 0xFF) << 8) | (data >> 8) # Conversion big endian

    def write16(self, reg : int, val : int) -> None :
        self.bus.write_word_data(self.device_addr, reg, ((val & 0xFF) << 8) | (val >> 8))

    def readBitW(self, reg : int, bit : int) -> bool:
        return (self.read16(reg) & (1 << bit)) != 0
        # v = self.read16(reg)
        # mask = 1 << bit
        # return ( (v & mask) > 0 )

    def writeBitW(self, reg : int, bit : int, value : bool) -> None:
        v = self.read16(reg)
        v = (v | (1 << bit)) if value else (v & ~(1 << bit))
        self.write16(reg, v)
        # if(value) : 
        #     v |= (1 << bit)
        # else :
        #     v &= ~(1 << bit)
        
        # self.write16(reg, value)
    
    def readBitsW(self, reg : int, startBit : int, size : int) -> int:
        v = self.read16(reg)
        mask = (1 << size) - 1
        return (v >> startBit) & mask
        # mask = 0

        # for i in range(size):
        #     mask = 1 + ( mask << 1 )

        # mask = mask << startBit

        # return ( (v & mask) >> startBit )

    def writeBitsW(self, reg : bytes, startBit : bytes, size : bytes, value : int) : 
        read = self.read16(reg)
        mask = (1 << size) - 1
        read = (read & ~(mask << startBit)) | ((value & mask) << startBit)
        self.write16(reg, read)
        # mask = 0

        # for i in range(size):
        #     mask = 1 + ( mask << 1 )

        # mask = ( ~( mask << startBit ) ) & 0b11111111

        # read = read & mask

        # read += ( value << startBit )

        # self.write16(reg, read)

    def close(self) -> None :
        self.bus.close()
