import regutils
from Hive import *
class SecurityRecord:

	def __init__(self):
		string = "poop"

	def initialize( self , binary , offset , hive):
		self.hive =  hive
		self.binary = binary
		self.length = len( self.binary )
		self.offset = offset
		self.magic_number = self.binary[0:2]
		self.unknown = self.binary[2:4]
		self.prev_sk_off = self.binary[4:8] #these are relative to the start of the hbin
		self.next_sk_off = self.binary[8:12]
		self.ref_count = self.binary[12:16]
		self.sec_disc_size = self.binary[16:20]
		self.sec_desc = self.binary[20:20+regutils.bytes_to_int(self.sec_disc_size)]
		self.padding = self.binary[20+regutils.bytes_to_int(self.sec_disc_size):self.length]

	def get_length(self):
		return self.length		

	def get_offset(self):
		return offset

	def get_magic_number(self):
		return regutils.bytes_to_string( self.magic_number )

	def get_unknown(self):
		return regutils.bytes_to_hexstring( self.unknown )+ " ("+str(regutils.bytes_to_int(self.unknown))+")"

	def get_prev_sk_off(self):
		return regutils.bytes_to_hexstring( self.prev_sk_off )+ " ("+str( regutils.bytes_to_int(self.prev_sk_off) )+")"

	def get_next_sk_off(self):
		return regutils.bytes_to_hexstring( self.next_sk_off )+ " ("+str( regutils.bytes_to_int(self.next_sk_off) )+")"

	def get_ref_count(self):
		return regutils.bytes_to_int( self.ref_count )

	def get_descriptor_size(self):
		return regutils.bytes_to_int( self.sec_disc_size )

	def get_descriptor(self):
		return str( self.sec_desc )

	def get_padding(self):
		return str( self.padding )

	def __str__(self):
		string = (  "--------------SecurityRecord-----------"+
					"\nMagic number : " + str( self.get_magic_number() ) +
					"\nUnknown : " + self.get_unknown() + 
					"\nPrevious SecRecord offset : " + self.get_prev_sk_off() +
					"\nNext SecRecord offset : " + self.get_next_sk_off() + 
					"\nReference count : " + str( self.get_ref_count() ) +
					"\nSecurity Descriptor Size : " + str( self.get_descriptor_size() ) +
					"\nSecurity Descriptor : " + self.get_descriptor() +
					"\nPadding : " + self.get_padding() )
		return string

					
					#print("--------------SecurityRecord-----------")
					#print("Magic number : " + str( self.get_magic_number() ) )
					#print("Unknown : " + self.get_unknown() )
					#print("Previous SecRecord offset : " + self.get_prev_sk_off() )
					#print("Next SecRecord offset : " + self.get_next_sk_off() )
					#print("Reference count : " + str( self.get_ref_count() ) )
					#print("Security Descriptor Size : " + str( self.get_descriptor_size() ) )
					#print("Security Descriptor : " + self.get_descriptor() )
					#print("Padding : " + self.get_padding() )

