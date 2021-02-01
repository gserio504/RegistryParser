import regutils
from KeyRecord import *
from ValueRecord import *
from SecurityRecord import *
from SubkeyList import *
from DataRecord import *
from RegList import *
from Data import *
from bitstring import BitArray

class Cell:

	def __init__( self , binary , offset , number, hive):
		self.hive = hive
		self.number = number
		self.magic_numbers = { "nk" : KeyRecord() , #key record 
					  	       "vk" : ValueRecord() , #value record
					           "sk" : SecurityRecord() , #security record
					           "lf" : SubkeyList() , #early version of windows subkey-lists where the hash in each element is calculated simply by taking the first four characters of the associated subkey’s name.
					           "lh" : SubkeyList() , #subkey-lists where elements stored as hash in Appendix C
					           "ri" : SubkeyList() , #subkey_list which stores pointers to additional subkey lists (tree structure)  
					           "li"	: SubkeyList() ,
					           "db" : DataRecord() }#same as ri except they reference keys instead of additonal lists   
					       #magic_numbers.get( blah )

					       #values lists

					       #binary includes only that of this cell
		self.binary = binary
		self.offset = offset
		self.length = binary[0:4] #check sign bit, Negative if allocated, positive if free.  The length is then 
		#the two's complement of the negative value (absolute value)
		self.magic_number = binary[4:6]
		
		self.allocated = regutils.isNegative( self.length ) 
		if self.allocated == True:
			self.length_int = regutils.negate_signed( self.length ) 
		else:
			self.length_int = regutils.bytes_to_int( self.length )

		self.cell_data = self.binary[4:self.length_int]
		self.cell_type = self.assign_cell_type()

		if type( self.cell_type ) == type(SubkeyList()):
			self.cell_type.initialize( self.cell_data , self.offset , self.isAllocated() , self.hive)
		elif type( self.cell_type ) != type( "None" ):
			self.cell_type.initialize( self.cell_data , self.offset , self.hive)

		#if no magic number then wait to be initialized later ( value or data fragment list)

	def get_number( self ):
		return self.number

	def init_val_or_data_list(self , num_elements , list_type ):
		self.cell_type = RegList( self.cell_data , self.offset , num_elements , list_type , self.hive)

	def init_data( self , data_type , data_size):
		self.cell_type = Data( self.cell_data , self.offset , data_type , data_size )

	def get_magic_number(self):
		return regutils.bytes_to_string( self.magic_number )

	def get_offset(self):
		return self.offset

	def get_length(self):
		return self.length_int

	def isAllocated(self):
		return self.allocated

	#get cell type and pass the binary 
	def assign_cell_type( self ): #what about value-lists
		number = self.get_magic_number()
		return self.magic_numbers.get( number , "None" )

	def __str__( self ): 
		string = "-----------------------Cell "+ str( self.get_number()) +"------------------------\n"
		string += "\nOffset : "+ str( self.offset ) + "\nAllocated: "+ str( self.allocated )
		string+="\nCell length: " + str( self.length_int )
		#print( str(type(self.cell_type)))
		if type( self.cell_type ) == type("abc") :
			string+="\nLength: "+str(self.length )
			string+= "\nMagic Number: "+ str( self.cell_type )+"\n"
		else:
			string+="\n"+str( self.cell_type ) + "\n"

		return string


