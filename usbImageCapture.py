import ctypes
from ctypes import *


#hl = c_void_p()
#buf = c_ubyte()
#transferred = c_int()
class USB_OBJ(Structure):
	_fields_ =[
		('hl', c_void_p),
		('transferred', c_int),
		('buf', c_ubyte)
		]

usb_obj = USB_OBJ()
 
libusb = ctypes.CDLL("/home/pi/testCode/libcyusb.so", mode=ctypes.RTLD_GLOBAL)

device_no = libusb._Z10cyusb_openv()
if device_no >=1:
	print device_no, "device open success"
else:
	print "Device open fail"

usb_obj.hl = libusb._Z15cyusb_gethandlei(0)
hl= usb_obj.hl

usb_vendor =  libusb._Z15cyusb_getvendorP20libusb_device_handle(hl)
print "VID: ", hex(usb_vendor)

usb_active = libusb._Z26cyusb_kernel_driver_activeP20libusb_device_handlei(hl, 0)
if usb_active != 0:
	print "kernal already taken"
	libusb._Z11cyusb_closev()	
else:
	print "ready to claim interface"

usb_interface = libusb._Z21cyusb_claim_interfaceP20libusb_device_handlei(hl, 0)
if usb_interface != 0:
	print "Claiming interface fail"
	libusb._Z11cyusb_closev()	
else:
	print "Claiming interface success"


#bulk_transfer = libusb._Z19cyusb_bulk_transferP20libusb_device_handlehPhiPii(hl, 0x83, buf, 512, transfered, 1000)

libusb._Z19cyusb_bulk_transferP20libusb_device_handlehPhiPii.argtypes = [c_void_p,c_ubyte,c_ubyte,c_int,c_int,c_int]
libusb._Z19cyusb_bulk_transferP20libusb_device_handlehPhiPii.restype = c_int

#print type(hl)
result = libusb._Z19cyusb_bulk_transferP20libusb_device_handlehPhiPii(usb_obj.hl, 0x86, usb_obj.buf, 512, usb_obj.transferred, 1000)
print result
#RxData = ''.join([chr(x) for x in result])
#print RxData
