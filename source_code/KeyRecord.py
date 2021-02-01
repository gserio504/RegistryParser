import regutils
from Hive import *
from bitstring import BitArray

class KeyRecord:

	def __init__( self ):
		self.binary = bytes([1,0,1,0])
		self.offset = 0

	def initialize( self , binary , offset , hive):
		self.binary = binary
		self.hive = hive
		self.offset = offset
		self.magic_number = self.binary[0:2]
		self.flags = self.binary[2:4]
		self.timestamp = self.binary[4:12]
		self.unknown0 = self.binary[12:16]
		self.parent_off = self.binary[16:20] #relative to start of hbin data
		self.num_sk_stable = self.binary[20:24] #set to 0 if deleted
		self.num_sk_volative = self.binary[24:28] 
		self.stable_sk_list_off = self.binary[28:32]# relative to start of hbin data,set 0xFFFFFFFF if deleted
		self.vol_sk_list_off = self.binary[32:36]
		self.num_values = self.binary[36:40]
		self.value_list_off = self.binary[40:44] #what if there are no values?
		self.sec_rec_off = self.binary[44:48] #set to 0xFFFFFFFF if deleted
		self.class_name_off = self.binary[48:52]
		self.max_sk = self.binary[52:56] #set to 0 if deleted
		self.max_sk_class = self.binary[56:60] #set unkowns to 0 too
		self.max_value_name = self.binary[60:64]
		self.max_value_data = self.binary[64:68]
		self.unknown4 = self.binary[68:72] #eek
		self.name_length = self.binary[72:74]#eek
		self.class_name_length = self.binary[74:76]
		self.name = self.binary[76 : 76+regutils.bytes_to_int(self.name_length) ]
		self.subkeys = []
		self.value_records = []

	def get_name(self):
		return regutils.bytes_to_string( self.name )

	def get_timestamp(self):
		return regutils.getFiletime( self.timestamp  )

	def get_magic_number(self):
		return regutils.bytes_to_string( self.magic_number )

	def get_offset(self):
		return self.offset

	def get_subkey_count(self):
		return regutils.bytes_to_int( self.num_sk_stable )

	def get_value_count(self):
		return regutils.bytes_to_int( self.num_values )

	def get_value_list_off(self):
		return regutils.bytes_to_int( self.value_list_off )

	def get_stable_sk_off(self):
		return regutils.bytes_to_int( self.stable_sk_list_off )

	def get_volatile_sk_off(self):
		return regutils.bytes_to_int( self.vol_sk_list_off )

	def get_subkey_records(self):
		subkey_list = self.hive.find_cell( self.get_stable_sk_off() + 4096 ).cell_type
		self.subkeys = subkey_list.get_subkeys()

	def get_value_records(self):
		if self.get_value_count() > 0:
			value_list = self.hive.find_cell( self.get_value_list_off() + 4096 ).cell_type
			self.value_records = value_list.get_value_records()
		return self.value_records

	def list_values(self):
		values = []
		if self.get_value_count() > 0:
			if len( self.value_records ) == 0:
				self.get_value_records()
			for value in self.value_records:
				values.append( value.get_name() )
		return values

	def get_value(self , value_name ):
		for value_record in self.value_records:
			if value_record.get_name() == value_name:
				return value_record
		return None


	def get_path(self , path_string ):
		path = path_string.split("\\")
		return path
		#if full_path == True:
		#	return path_string.replace("\\","/").split("/")
		#else:
		#	path = [path_string]
		#	return path

	def find_subkey(self, subkey):
		if self.get_subkey_count() > 0:
			if len( self.subkeys ) == 0:
				self.get_subkey_records()
			for sk in self.subkeys:
				if sk.get_name() == subkey:
					return sk
		else:
			return self #didnt have a subkey by that name, return myself

	def get_subkey(self,path):
		subkeys = self.get_path(path)
		#print( "get subkey: "+str(subkeys) )
		key = self
		for sk in subkeys:
			#print( "in loop: "+key.get_name() +"  - trying to find "+str(subkeys))
			key = key.find_subkey(sk)
		return key

	def list_subkeys(self):
		the_list = []
		if self.get_subkey_count() > 0:
			if len( self.subkeys ) == 0:
				self.get_subkey_records()
			for sk in self.subkeys:
				#try:
					the_list.append( sk.get_name() )
				#except:
				#	pass
		return the_list



	def __str__( self ):
		string = (  "--------------KeyRecord-----------"  +
					"\nMagic Number: " + regutils.bytes_to_string( self.magic_number) + 
				    "\nFlags : " + str( self.flags ) + 
				    "\nTimestamp : " + regutils.getFiletime( self.timestamp  ) +
				    "\nUnknown : "+ regutils.bytes_to_hexstring( self.unknown0 ) + " (" + str(regutils.bytes_to_int( self.unknown0)) + ")" +
					"\nParent key's offset : " + regutils.bytes_to_hexstring( self.parent_off ) + " ("+str( regutils.bytes_to_int( self.parent_off ) ) +")"+
					"\nNum of stable subkeys : " + str( regutils.bytes_to_int( self.num_sk_stable ) ) + 
				    "\nNum of volative subkeys : " + str( regutils.bytes_to_int( self.num_sk_volative) ) +
					"\nStable subkey list offset : "+regutils.bytes_to_hexstring(self.stable_sk_list_off)+" ("+str( regutils.bytes_to_int( self.stable_sk_list_off ) ) +")"+
					"\nVolatile subkey list offset : "+regutils.bytes_to_hexstring(self.vol_sk_list_off)+" ("+str( regutils.bytes_to_int( self.vol_sk_list_off ) ) +")"+
					"\n# of Values : "+ str(regutils.bytes_to_int( self.num_values ))+
					"\nValue list offset : "+ regutils.bytes_to_hexstring( self.value_list_off )+" (" +str( regutils.bytes_to_int( self.value_list_off ) ) + ")"+
					"\nSecurity Record offset : "+ regutils.bytes_to_hexstring( self.sec_rec_off )+" ("+str(regutils.bytes_to_int( self.sec_rec_off))+")"+
					"\nClass name offset : "+ regutils.bytes_to_hexstring( self.class_name_off )+" ("+str(regutils.bytes_to_int( self.class_name_off))+")"+
					"\nMax characters in subkey name : "+str( regutils.bytes_to_int( self.max_sk ) )+
					"\nMax chars in subkey class name : "+ str(regutils.bytes_to_int( self.max_sk_class))+
					"\nMax chars value name : "+ str(regutils.bytes_to_int( self.max_value_name))+
					"\nMax chars in data name : "+ str(regutils.bytes_to_int( self.max_value_data))+
					"\nUnknown : "+ regutils.bytes_to_hexstring( self.unknown4 )+" ("+str(regutils.bytes_to_int( self.unknown4))+")"+
					"\nName.length : " + str( regutils.bytes_to_int( self.name_length) ) +
					"\nClass name length : "+str( regutils.bytes_to_int( self.class_name_length) )+
					"\nName : " + regutils.bytes_to_string( self.name) 
				    #"\n\n"+str(self.binary)+"\n\n"
				)
		return string


