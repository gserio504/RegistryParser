from bitstring import BitArray
import regutils

class RegHeader:

	def __init__( self , binary ):
		self.offset = 0
		self.length = 4096
		self.time_stamp_bytes = binary[12:20]
		self.root_key_off = binary[36:40]
		self.last_hbin_off_bytes = binary[40:44]
		self.hive_name_bytes = binary[48:112]

		self.time_stamp = regutils.getFiletime (  self.time_stamp_bytes  )
		self.first_record = regutils.bytes_to_int( self.root_key_off )
		self.last_hbin_off = regutils.bytes_to_int( self.last_hbin_off_bytes )
		self.hive_name = regutils.bytes_to_string( self.hive_name_bytes )

	def get_root_offset(self):
		return regutils.bytes_to_int( self.root_key_off )

	def __str__( self ):
		string = "-------Registry Header--------"
		string += "Hive name: "+self.hive_name
		string +="\nTime stamp: "+self.time_stamp
		string +="\nRoot record offset relative to first hbin: "+ str( self.first_record )
		string += "\nLast hbin offset: "+ str( self.last_hbin_off )
		return string