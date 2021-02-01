import regutils
from Hive import *
from DataRecord import *
from Data import *
import random

class ValueRecord:

	def __init__(self):
		string = "poop"

	def initialize( self , binary , offset , hive):
		self.hive = hive
		self.binary = binary
		self.length = len( self.binary )
		self.magic_number = self.binary[0:2]
		self.name_length = self.binary[2:4] #if length = 0, value=(default)
		self.data_size = self.binary[4:8]
		#if the length = 0 then the value is not set
		#if the MSB is set, the data is actualy stored in the data_offset 
		self.data_offset = self.binary[8:12] #relative to start of hbin data
		self.data_type = self.binary[12:16]
		self.flags = self.binary[16:18]
		self.unknown = self.binary[18:20]
		self.value_name = self.binary[20:20+self.get_name_length()]
		if self.get_name_length() == 0:
			self.value_name = "(default)("+str(random.randint(0,101))+")"
		self.padding = self.binary[20+self.get_name_length():self.length]
		self.types = {  0 : "REG_NONE" ,
  						1 : "REG_SZ" ,
					    2 : "REG_EXPAND_SZ" ,
					    3 : "REG_BINARY" ,
					    4 : "REG_DWORD" ,
					    5 : "REG_DWORD_BIG_ENDIAN" ,
			    		6 : "REG_LINK" ,
					    7 : "REG_MULTI_SZ" ,
					    8 : "REG_RESOURCE_LIST" ,
			    		9 : "REG_FULL_RESOURCE_DESCRIPTOR" ,
						10 : "REG_RESOURCE_REQUIREMENTS_LIST" ,
			    		11 : "REG_QWORD" }

	def get_magic_number(self):
		return regutils.bytes_to_string( self.magic_number )

	def get_name_length(self):
		length = regutils.bytes_to_int( self.name_length )
		return length

	def data_is_local(self):
		return regutils.isNegative( self.data_size )

	def get_data_size(self):
		stored_locally = self.data_is_local()
		size = -1
		if stored_locally:
			size = regutils.remove_MSB( self.data_size )
		else:
			size = regutils.bytes_to_int( self.data_size )
		return size

	def get_data_size_string( self ):
		return regutils.bytes_to_hexstring( self.data_size ) + " ("+str(self.get_data_size())+")"+", (MSB set means stored in vk)" 

	def has_data(self):
		if self.get_data_size() == 0:
			return False
		return True

	#how do i fix this if the data is large and fragmented?
	def get_data_offset(self):
		return regutils.bytes_to_int( self.data_offset )

	def get_data_offset_string(self):
		return regutils.bytes_to_hexstring( self.data_offset ) + " ("+str(self.get_data_offset())+")"

	def get_data_type(self):
		number = regutils.bytes_to_int( self.data_type )
		return self.types.get( number , "Who knows" )

	def get_flags(self):
		return regutils.bytes_to_int( self.flags )

	def name_encoding(self):
		number = self.get_flags()
		if number == 1:
			return "ascii"
		else:
			return "UTF-16-le"

	def get_unknown(self):
		return regutils.bytes_to_hexstring( self.unknown ) + " ("+str(regutils.bytes_to_int( self.unknown ))+")"

	def get_name( self ):
		if self.get_name_length() == 0:
			return self.value_name
		encoding = self.name_encoding()
		return self.value_name.decode( encoding )

	def get_padding( self ):
		return str( self.padding )

	def get_data(self):
		if self.has_data():
			if self.data_is_local():
				return self.parseLocalData() #uh probably want to move parsing methods to regutils from data object
			else:
				data_cell = self.hive.find_cell( self.get_data_offset() + 4096 ).cell_type
				if isinstance(data_cell , type(DataRecord()) ):
					return "Sorry, i havent parsed big data records"
				else:
					return data_cell.get_data()
		else:
			return "Null"

	def parseLocalData(self):
		data = Data( self.data_offset , 1 , self.get_data_type() , 4 ).get_data()
		return data

	def __str__(self):
		string = (  "--------------Value Record--------------"+
					"\nMagic Number : " + self.get_magic_number() + 
					"\nName size : " + str(self.get_name_length()) + " ( 0 means (default) )" +
					"\nData size : " + self.get_data_size_string() +
					"\nHas data : " + str( self.has_data() ) +
					"\nData offset : " + self.get_data_offset_string() + " (if MSB = 1, this is the data, else = relative offset from start of hbin)"+
					"\nData type :" + self.get_data_type() +
					"\nFlags : " + str( self.get_flags() ) +
					"\nName encoding : " + self.name_encoding() +
					"\nUnknown : " + self.get_unknown() +
					"\nName : "+ self.get_name() +
					"\nPadding : "+ self.get_padding() )
		return string
