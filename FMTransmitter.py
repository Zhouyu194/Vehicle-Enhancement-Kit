import smbus
import time
import os


class FMTransmitter(object):
	def __init__(self):
		self.bus = smbus.SMBus(1)
		self.addr = 0x3e
		self.gainDict = {
			0b11111 : 12,
			0b11110 : 11,
			0b11101 : 10,
			0b11100 : 9,
			0b11011 : 8,
			0b11010 : 7,
			0b11001 : 6,
			0b11000 : 5,
			0b10111 : 4,
			0b10110 : 3,
			0b10101 : 2,
			0b10100 : 1,
			0b10011 : 0,
			0b10010 : 0,
			0b10001 : 0,
			0b10000 : 0,
			0b00000 : 0,
			0b00001 : -1,
			0b00010 : -2,
			0b00011 : -3,
			0b00100 : -4,
			0b00101 : -5,
			0b00110 : -6,
			0b00111 : -7,
			0b01000 : -8,
			0b01001 : -9,
			0b01010 : -10,
			0b01011 : -11,
			0b01100 : -12,
		}
		self.codeDict = {
			12 : 0b11111,
			11 : 0b11110,
			10 : 0b11101,
			9 : 0b11100,
			8 : 0b11011,
			7 : 0b11010,
			6 : 0b11001,
			5 : 0b11000,
			4 : 0b10111,
			3 : 0b10110,
			2 : 0b10101,
			1 : 0b10100,
			0 : 0b10011,
			-1 : 0b00001,
			-2 : 0b00010,
			-3 : 0b00011,
			-4 : 0b00100,
			-5 : 0b00101,
			-6 : 0b00110,
			-7 : 0b00111,
			-8 : 0b01000,
			-9 : 0b01001,
			-10 : 0b01010,
			-11 : 0b01011,
			-12 : 0b01100,
		}
		os.system("sudo sh -c '/bin/echo Y > /sys/module/i2c_bcm2708/parameters/combined'")
		# self.address = 0x3E
		# self.registers = [0x00, 0x01, 0x02, 0x04, 0x0B, 0x0C, 0x0E, 0x0F, 0x10, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x1E, 0x26, 0x27]
		# self.default =   [0x5C, 0xC3, 0x40, 0x04, 0x00, 0x00, 0x02, 0x0F, 0xA8, 0x80, 0x80, 0x00, 0xE0, 0x00, 0x00, 0x00, 0xA0, 0x00]
		# for i in range(0,11):
		# bus.write_byte_data(0x3E,registers[i], default[i])

	def write_to_register(self, register, data):
		return self.bus.write_byte_data(self.addr, register, data)

	def read_from_register(self, register):
		return self.bus.read_byte_data(self.addr,register)

	def set_freq(self, freq):
		freq *= 20
		freq = int(freq)
		freq &= 0x0fff
		reg0 = self.read_from_register(0x02)
		reg9_11 = self.read_from_register(0x01)
		
		if freq&0x01 > 0:
			reg0 |= 0x80
		else:
			reg0 &= ~0x80
		
		reg1_8 = (freq >> 1) & 0xff
		reg9_11 = (reg9_11&0xF8) | ((freq >> 9) & 0xff)
		
		self.write_to_register(0x02, reg0)
		self.write_to_register(0x01, reg9_11)
		self.write_to_register(0x00, reg1_8)

	def read_freq(self):
		chsel1_8 = self.read_from_register(0x00) << 1
		chsel0 = (self.read_from_register(0x02) & 0x80) >> 7
		chsel9_11 = (self.read_from_register(0x01) & 0x07) << 9
		chsel = chsel0 + chsel1_8 + chsel9_11
		freq = chsel/20.
		return freq
	
	def read_gain(self):
		PGA = self.read_from_register(0x01) >> 3
		PGA = PGA & 0x07
		PGA_LSB = self.read_from_register(0x04) >> 4
		PGA_LSB = PGA_LSB & 0x03
		Code = PGA << 2 | PGA_LSB
		return self.gainDict[Code]
		
	def set_gain(self, gain):
		Code = self.codeDict[gain]
		PGA = Code >> 2
		PGA_LSB = Code & 0x03
		reg04 = PGA_LSB << 4
		reg04 = reg04 | (self.read_from_register(0x04) & 0xcf)
		reg01 = PGA << 3
		reg01 = reg01 | (self.read_from_register(0x01) & 0xc7)
		self.write_to_register(0x01, reg01)
		self.write_to_register(0x04, reg04)
		
	def read_mute(self):
		reg02 = self.read_from_register(0x02)
		mute = (reg02 >> 3) & 0x01
		return mute
		
		
	def set_mute(self, enable):
		reg02 = self.read_from_register(0x02)
		if enable:
			reg02 = reg02 | 0x08
		else:
			reg02 = reg02 & 0xf7
		self.write_to_register(0x02, reg02)
		