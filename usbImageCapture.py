import ctypes
from ctypes import *

libusb = ctypes.CDLL("/home/pi/testCode/libcyusb.so", mode=ctypes.RTLD_GLOBAL)
device_no = libusb._Z10cyusb_openv()
if device_no >=1:
	print device_no, "device open success"
else:
	print "Device open fail"

hl = libusb._Z15cyusb_gethandlei(0)

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

buf = []
transfered = 0

libusb._Z19cyusb_bulk_transferP20libusb_device_handlehPhiPii.argtypes() 
bulk_transfer = libusb._Z19cyusb_bulk_transferP20libusb_device_handlehPhiPii(hl, 0x83, buf, 512, POINTER(transfered), 1000)
