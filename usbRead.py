import usb.core
import usb.util
import string 
import struct

def main():
    device = usb.core.find(idVendor=0x0547, idProduct=0x1002)

    # use the first/default configuration
    device.set_configuration()

    # first endpoint
    endpoint = device[0][(0,0)][0]

    # read a data packet
    #data_packet = device.read(0x86,512,1000)
    #for n in range(512):
	#byte_data = data_packet[n]
        #bit_string =  int2base(byte_data,2)
        #print bit_string
        

    while True:
        try:
            data_packet = device.read(0x86,512,1000)
            for n in range(512):
        	byte_data = data_packet[n]
        	bit_string =  int2base(byte_data,2)
        	print bit_string
		if bit_string[0] == '1' and bit_string[1] == '0' and bit_string[2] == '1' and bit_string[3] == '0':
			print "invalid frame****************************************************"
		if bit_string == '00000000':
			print "null value ******************************************************"

        except usb.core.USBError as e:
            data = None
            if e.args == ('Operation timed out',):

                continue


def int2base(x, base):
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


if __name__ == '__main__':
  main()
