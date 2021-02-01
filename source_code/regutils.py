import datetime
from bitstring import BitArray

def bytes_to_string( byte_list ):
	string=""
	for byte in byte_list:
		string+=chr(byte)
	return string

def bytes_to_int( byte_list ):
	integer = 0
	shift_ammt = 0
	for byte in byte_list:
		integer|=byte<<(shift_ammt*8)
		shift_ammt+=1
	return integer

def bytes_to_hexstring( byte_list ):
	#swapped = bytes( [ byte_list[3] , byte_list[2] , byte_list[1] , byte_list[0] ] )
	#return "0x"+swapped.hex()
	string = ""
	for byte in byte_list:
		string=bytes([byte]).hex()+string
	return "0x"+string

def int_to_bytes( value ):
	binary = bytes( [ (value & 0xFF) , ( (value>>8) & 0xFF), ( (value>>16) & 0xFF), ( (value>>24) & 0xFF) ] )
	return binary

# could probably just make this if greater than a certain value ( largest signed value ) then negative
def isNegative( byte_list ):
	unsigned_value = bytes_to_int( byte_list )
	max_signed_value = 2147483647
	if unsigned_value > max_signed_value: #then the first bit must be set
		return True
	return False

def negate_signed( byte_list ):
	#perform two's complement lol( in a funky way )
	unsigned_value = bytes_to_int( byte_list )
	uns_max = 4294967295
	return (uns_max - unsigned_value) + 1

def getFiletime(dt):
	try:
		dt = BitArray( reverse_endian( dt ) ).hex

		us = int(dt,16) / 10.
		time = datetime.datetime(1601,1,1) + datetime.timedelta(microseconds=us)
		return str( time )
	except:
		return "Invalid Literal for int() with base 16 ( in getFiltime )"


def reverse_endian( byte_list ):
	new_list = bytearray( byte_list )
	new_list.reverse()
	return bytes( new_list )

def remove_MSB( byte_list ):
	num = bytes_to_int( byte_list )
	return num - 2147483648

