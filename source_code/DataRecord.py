import regutils
from Hive import *

class DataRecord:

	def __init__(self):
		string = "poop"

	def initialize( self , binary , offset , hive):
		self.hive = hive
		self.binary = binary
		self.offset = offset
		self.magic_number = self.binary[0:2]
		self.num_of_data = self.binary[2:4]
		self.data_list_offset = self.binary[4:8]
		self.unknown = self.binary[8:12]

	def get_offset( self ):
		return self.offset

	def get_magic_number( self ):
		return regutils.bytes_to_string( self.magic_number )

	def get_num_data( self ):
		return regutils.bytes_to_int( self.num_of_data )

	def get_data_list_offset( self ):
		return regutils.bytes_to_int( self.data_list_offset )

	def get_unknown( self ):
		return regutils.bytes_to_hexstring( self.unknown ) + " (" + str( regutils.bytes_to_int(self.unknown) ) + ")"

	def __str__( self ):
		string = (  "\n--------------Big Data Record--------------" +
					"\nMagic Number : " + self.get_magic_number() +
					"\nNumber of data fragments in list : " + str( self.get_num_data() ) +
					"\nData list offset : " + regutils.bytes_to_hexstring( self.num_of_data ) + " (" + str( self.get_num_data() ) + ")" +
					"\nUnknown : " + self.get_unknown()
				 )
		return string 
