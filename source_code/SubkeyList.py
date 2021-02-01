import regutils
from Hive import *
#this needs to be cleaned up immensely.... particularly in the spots dealing with whether or not the subkey list is
#allocated... ri records go crazy cause the number of elements field is wrng
#lh lists have sometimes 0 or a number when deallocated... whats going on there
class SubkeyList:

	def __init__(self):
		string = "poop"

	def initialize(self , binary , offset , allocated , hive):
		self.hive = hive
		self.binary = binary
		self.offset = offset
		self.length = len(self.binary)
		self.magic_number = self.binary[0:2]
		self.num_elements = self.binary[2:4]
		self.allocated = allocated
		if not allocated and self.get_magic_number() == "ri":
			self.num_elements = bytes( [0 , 0 , 0 , 0] )

		self.types = { "lf" : self.init_LF_LH,
					   "lh" : self.init_LF_LH,
					   "li" : self.init_LI,
					   "ri" : self.init_RI }
		func = self.types.get( self.get_magic_number() )
		func()
		#func() #call appropriate initialization based on magic number (type of subkeylist)
		self.toString = { "lf" : self.LF_LH_toString ,
						  "lh" : self.LF_LH_toString ,
						  "li" : self.LI_toString ,
						  "ri" : self.RI_toString }

	#i dont think we have any of these... only versions of windows older than NT have this type?
	def init_LF_LH(self):
		#the elements are 0-4 ( offset of subkey rel to hbin), 4-8 the (hash?) first 4 chars of subkey name
		self.sk_offs = []
		self.sk_hashes = []

		for x in range( self.get_num_elements() ):
			offset = self.binary[ 4 + 8 * x : 8 + 8 * x ]
			self.sk_offs.append( regutils.bytes_to_int( offset)  ) 
			self.sk_hashes.append(  self.binary[ 8 + 8 * x : 12 + 8 * x ]   )

		self.padding = self.binary[ 4 + 8*self.get_num_elements() : self.get_length() ]

	def LF_LH_toString(self):
		string =  "\n( contains pointers to subkeys relative to start of hbin )"
		for index in range( self.get_num_elements() ):
			offset = self.sk_offs[index]
			string += "\nHash of Subkey's Name  : " + str( self.sk_hashes[index] )
			string += "\nOffset : " + str( hex(offset) ) + " (" + str( offset ) + ")"
			string += "\n"
		string += "\nPadding : "+str( self.padding )
		return string

	def init_LI( self ):
		self.sk_offs = []
		for x in range( self.get_num_elements() ):
			offset = self.binary[ 4 + 4 * x : 8 + 4 * x ]
			self.sk_offs.append( regutils.bytes_to_int( offset ) )
			end_of_elements = 4 + 4 * x
		self.padding = self.binary[ 4 + 4 * self.get_num_elements() : self.get_length() ]


	def LI_toString( self ):
		string =  "\n( contains pointers to subkeys relative to start of hbin )"
		for index in range( len(self.get_num_elements() ) ):
			offset = self.sk_offs[index]
			string += "\nOffset : " + str( hex(offset) ) + " (" + str( offset ) + ")"
		string += "\nPadding : "+str( self.padding )

		return string


	def init_RI(self):
		#seems to be the only subkey list that does weird shit when not allocated
		self.sk_offs = []
		for index in range( self.get_num_elements() ):
			offset = self.binary[ 4 + 4 * index : 8 + 4 * index ]
			self.sk_offs.append( regutils.bytes_to_int(offset) )
		if self.allocated:
			self.padding = self.binary[ 4 + 4*self.get_num_elements() : self.get_length() ]
		else:
			self.padding = self.binary[ 4 : self.get_length()]


	def RI_toString(self):
		string = "\n( Pointers to additional subkey lists relative to start of hbin)"
		for x in range( self.get_num_elements() ):
			offset = self.sk_offs[x]
			string += "\nOffset : " + str( hex(offset) ) + " (" + str( offset ) + ")"
		string += "\nPadding : " + str( self.padding)
		return string

	def get_magic_number(self):
		return regutils.bytes_to_string( self.magic_number )

	def get_length(self):
		return self.length

	def get_offset(self):
		return self.offset

	def get_num_elements(self):
		return regutils.bytes_to_int( self.num_elements )

	def get_padding(self):
		return str( self.padding )

	def get_subkeys(self):
		key_records = []
		for x in range (self.get_num_elements()):
			sk = self.hive.find_cell(self.sk_offs[x]+4096).cell_type #cause offset was relative to start of first hbin 
			key_records.append( sk )
		return key_records

	def get_subkeys2(self):
		key_records = []
		if self.get_magic_number() == "ri":
			pass


	def __str__(self):
		string = ( "--------------SubkeyList--------------" +
					"\nMagic Number : " + self.get_magic_number() +
					"\nNumber of Elements : " + str( self.get_num_elements() ) +
					"\n----Elements----"
				 ) 
		function = self.toString.get( self.get_magic_number() )
		string += function() #calls the tostring of each type
		return string