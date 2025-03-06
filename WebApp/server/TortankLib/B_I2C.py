#!/usr/bin/python3

from types import *

import smbus2, time

bus = smbus2.SMBus(1)

class I2C : 
    device_addr : bytes
    def __init__(self, device_addr : bytes) -> None:
        self.device_addr = device_addr
        pass

    def read8(self, reg : bytes) -> int: 
         return bus.read_byte_data(self.device_addr, reg)
    
    def readBit(self, reg : bytes, bit : bytes) -> bool:
        v = self.read8(reg)
        mask = 1 << bit
        return ( (v & mask) > 0 )
    
    def readBits(self, reg : bytes, startBit : bytes, size : bytes) -> int:
        v = self.read8(reg)

        mask = 0

        for i in range(size):
            mask = 1 + ( mask << 1 )

        mask = mask << startBit

        return ( (v & mask) >> startBit )


    def write8(self, reg : bytes, val : bytes) -> int :
        return bus.write_byte_data(self.device_addr, reg, val)
    
    def writeBit(self, reg : bytes, bit : bytes, value : bool):
        v = self.read8(reg)

        if(value) : 
            v |= (1 << bit)
        else :
            v &= ~(1 << bit)
        
        self.write8(reg, value)

    def writeBits(self, reg : bytes, startBit : bytes, size : bytes, value : bytes) : 

        read = self.read8(reg)

        print(f"writeBits start : {read}, value : {value}, startbit : {startBit}, size : {size}")

        mask = 0

        for i in range(size):
            mask = 1 + ( mask << 1 )

        mask = ( ~( mask << startBit ) ) & 0b11111111

        print(f"mask : {mask} ")

        read = read & mask

        read += ( value << startBit )

        print(f"writeBits end : {read}")

        self.write8(reg, read)

    def read16(self, reg : bytes) -> int :
        data1 = self.read8(reg)
        data2 = self.read8(reg + 1)
        print(f"data1 : {data1}")
        print(f"data2 : {data2}")
        return ( (data1 << 8 ) | data2 )
    
    def readBitsW(self, reg : bytes, startBit : int, size : int) -> int:
        v = self.read16(reg)

        mask = 0

        for i in range(size):
            mask = 1 + ( mask << 1 )

        mask = mask << startBit

        return ( (v & mask) >> startBit )
    
    def readBitW(self, reg : bytes, bit : int) -> bool:
        v = self.read16(reg)
        mask = 1 << bit
        return ( (v & mask) > 0 )
    
    def write16(self, reg : bytes, val : int) -> int :
        return bus.write_workd_data(self.device_addr, reg, val)
    
    def writeBitW(self, reg : bytes, bit : int, value : bool):
        v = self.read16(reg)

        if(value) : 
            v |= (1 << bit)
        else :
            v &= ~(1 << bit)
        
        self.write16(reg, value)


    def writeBitsW(self, reg : bytes, startBit : bytes, size : bytes, value : int) : 

        read = self.read16(reg)

        print(f"writeBits start : {read}, value : {value}, startbit : {startBit}, size : {size}")

        mask = 0

        for i in range(size):
            mask = 1 + ( mask << 1 )

        mask = ( ~( mask << startBit ) ) & 0b11111111

        print(f"mask : {mask} ")

        read = read & mask

        read += ( value << startBit )

        print(f"writeBits end : {read}")

        self.write16(reg, read)
