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
		
		self.readBitString()
        
	def readBitString(self): 
		while True:
			try:
				data_packet = self.device.read(0x86,512,1000)
				for n in range(512):
					byte_data = data_packet[n]
					bit_string =  self.int2base(byte_data,2)
					print bit_string
	
					#looking for new frame
					if bit_string[0] == '1' and bit_string[1] == '0' and bit_string[2] == '1' and bit_string[3] == '0':
						print "invalid frame******************"
						self.logg.info("invalid frame **************")
						if bit_string[0] == '1' and bit_string[1] == '0' and bit_string[2] == '1' and bit_string[3] == '1':
							print "new frame started #################################"
							self.logg.info("new frame started ##########################")
						else:
							print "waiting for new frame to start *****************"
							self.logg.info("waiting for new frame to start *****************")
                   

			except usb.core.USBError as e:
				data_packet = None
				self.logg.error("USB ERROR. %s"%(e.message))
				if e.args == ('Operation timed out',):	
					continue


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
	read = usbRead()
