import usb.core
import usb.util
import string 
import struct
import logging
import logging.handlers
from logging.handlers import RotatingFileHandler
from logging import StreamHandler, Formatter

class usbRead():
	def __init__(self):
    		self._loggerInit()
		self.logg = logging.getLogger('')
		self.logg.info('PolyU Camera capture log file')

		self.device = usb.core.find(idVendor=0x0547, idProduct=0x1002)

		# use the first/default configuration
		self.device.set_configuration()

		# first endpoint
		self.endpoint = self.device[0][(0,0)][0]

		self.waitForFrameValid = False
		self.frameData = []
		self.data_buff = []
		self.buffSize = 8192
		#self.readBitString()
		self.getDataBuff()
		self.readDataBuff()

	def getDataBuff(self):
		#buffer twice the data frame for 1024*1024*16bit/512Byte
                for n in range (self.buffSize):
                        data = self.device.read(0x86,512,0)
                        #print data[0]
			self.data_buff.append(data)

		#print self.data_buff[0]
		#print self.data_buff[0][0]
		print "total data buff size: ",len(self.data_buff)
		print "each data packet size: ",len(self.data_buff[0])
   
	def readDataBuff(self):
		for n in range (len(self.data_buff)):
			for m in range (len(self.data_buff[n])):
				byte_data = self.data_buff[n][m]
				bit_string = self.int2base(byte_data,2)
				#print "bit string: ",bit_string

				if bit_string[0] == '1' and bit_string[1] == '0' and bit_string[2] == '1' and bit_string[3] == '0':
					self.waitForFrameValid = True
					#print "***invalid frame***"

				if bit_string[0] == '1' and bit_string[1] == '0' and bit_string[2] == '1' and bit_string[3] == '1':
					if self.waitForFrameValid:
						#print "***valid frame start***"
						nextBit_string = self.int2base(self.data_buff[n][m+1],2)
						self.frameData.append(bit_string[6:]+nextBit_string[0:])
						#print "appended bit string: ", bit_string[6:]+nextBit_string[0:]
						#print self.frameData
						#self.logg.info(bit_string[6:]+nextBit_string[0:])
						#self.logg.info(self.frameData)
						try:
							next2Bit_string = self.int2base(self.data_buff[n][m+2],2)
							#print "next2Bit_string: ", next2Bit_string
							if next2Bit_string[0] == '1' and next2Bit_string[1] == '0' and next2Bit_string[2] == '1' and next2Bit_string[3] == '0':
								print "***end of frame***"
								print "length of valid frame: ", len(self.frameData)
								self.logg.info("***end of frame***")
								self.logg.info(len(self.frameData))
								self.waitForFrameValid = False
								self.frameData = []

						except:
							#print "***end of 512 byte data packet***"
							#print "no. of byte of this packet: ", m
							#self.logg.info("***end of 512 byte data packet***")
							pass
							
				#else:
				#	print "Not the first byte data"		

	   


	def int2base(self,x, base):
		digs = string.digits + string.letters

		if x < 0:
			sign = -1
		elif x == 0:
			#return digs[0]
			return '00000000'
		else:
			sign = 1

		x *= sign
		digits = []

		while x:
			digits.append(digs[x % base])
			x /= base

		if sign < 0:
			digits.append('-')

		#digits.reverse()
		#print len(digits)
		add_zero_no = 8 - len(digits)
		for n in range (add_zero_no):
			digits.append(digs[0 % base])

		return ''.join(digits)

	def _loggerInit(self,file_name = 'debugLog.log'):
		folder = 'log'
		try:
			os.makedirs(folder)
		except Exception as e:
			pass   # pass if log folder exists
		logg = logging.getLogger('')
		logg.setLevel(logging.DEBUG)
		handler = RotatingFileHandler(folder +'/'+ file_name, backupCount=200, maxBytes=1024*500)
		handler.setFormatter(Formatter('%(asctime)s %(filename)s[line:%(lineno)d] [%(levelname)s] %(message)s'))
		logg.addHandler(handler)


if __name__ == '__main__':
	usbcyRead = usbRead()
