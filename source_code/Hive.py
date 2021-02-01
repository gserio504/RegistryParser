from bitstring import BitArray
import regutils
from RegHeader import *
from HiveBin import *
from Reinitializer import *
from Cell import *
from RegList import *
from KeyRecord import *
from DataRecord import *
from ValueRecord import *

class Hive:

	def __init__( self , hive_file ):
		self.reinit_table = { "db" : "dummy" ,
							  "vk" : "dummy" , 
							  "nk" : "dummy" }
		self.reinit_list = []
		self.binary = self.get_binary( hive_file )
		self.reg_header = RegHeader( self.binary[0:4096] )
		#print( self.reg_header )
		self.hbin_list = self.get_hbins()
		#print( "wow" )
		self.reinit_cells()

	def get_root(self):
		if self.reg_header.get_root_offset() == 32:
			root =  self.hbin_list[0].cells[0].cell_type
		else:
			root = self.find_cell( 4096+self.reg_header.get_root_offset() ).cell_type
		return root


	def find_hbin( self, offset ):
		bins = self.hbin_list
		first = 0
		last = len(bins) - 1
		while first <= last:
			middle = int( (first+last)/2 )
			hbin = bins[middle]
			if offset >= hbin.offset() and offset <= ( hbin.offset() + hbin.length() - 1 ):
				return middle
			elif offset < hbin.offset():
				last = middle - 1
			else:
				first = middle + 1
		return -1

	def find_cell( self , offset ):
		index = self.find_hbin( offset )
		hbin = self.hbin_list[ index ]

		index = hbin.find_cell( offset )
		return hbin.cells[ index ]


	def hbin_info( self ):
		for hbin in self.hbin_list:
			hbin_end = (hbin.offset() + hbin.length() )-1
			print( "-----Hbin"+str(hbin.hbin_number)+"-----") 
			print( "Hbin's last byte : "+str( hbin_end ) )
			print( "Offset : " + str(hbin.beg_offset) )
			print( "Length : "  + str( hbin.hive_bin_size ) )
			print( "binary length : "+str(len(hbin.binary)))

	def get_last_cell( self , hbin_number ):
		hbin = self.hbin_list[hbin_number]
		last_cell = hbin.cells[len(hbin.cells)-1]
		print( last_cell )

	
	def get_binary( self , filename ):
		try:
			file = open( filename , "rb" )
			binary = file.read()
		except:
			print( "File not found.  Exiting." )
			quit()
		return binary

	#called from hbin, which has a reference to this hive lol
	def mark_for_reinitialization( self , cell ):

		if cell.isAllocated() and (cell.get_magic_number() in self.reinit_table):
			mag_num = cell.get_magic_number()
			cell_type = cell.cell_type

			if mag_num == "nk" and cell_type.get_value_count() > 0:
				self.reinit_list.append( Reinitializer( cell_type.get_value_list_off() , "value_list" , cell_type.get_value_count() ) )
			elif mag_num == "db":
				self.reinit_list.append( Reinitializer( cell_type.get_data_list_offset() , "data_list" , cell_type.get_num_data() ) )
			elif mag_num == "vk":
				if cell_type.get_data_size() <= 16344 and (not cell_type.data_is_local() ): #then the vk record 
					self.reinit_list.append( Reinitializer( cell_type.get_data_offset() , cell_type.get_data_type() , cell_type.get_data_size() ) ) #the one here is dummy



	def get_hbins( self ):
		hbin_list = []
		current_offset = 4096
		count = 0

		while current_offset <= self.reg_header.last_hbin_off:
			hbin_length =  regutils.bytes_to_int( self.binary[current_offset+8:current_offset+12] )
			current_hbin = HiveBin( self.binary[current_offset:(current_offset+hbin_length)] , current_offset , count , self )
			hbin_list.append( current_hbin )
			current_offset = current_offset + hbin_length
			count+=1
		return hbin_list

	def reinit_cells( self ):
		for x in range( len( self.reinit_list ) ):
			reinitializer = self.reinit_list[x]
			cell_type = reinitializer.cell_type
			cell_offset = reinitializer.cell_offset
			num_elements = reinitializer.num_elements

			cell = self.find_cell( cell_offset )

			if cell_type == "value_list":
				cell.init_val_or_data_list( num_elements , "value" )
			elif cell_type == "data_list":
				cell.init_val_or_data_list( num_elements , "data")
			else: # was a data cell
				cell.init_data( cell_type , num_elements ) #here num of elements is actually the data size
	

	def print_cell_type(self , class_type ):
		print(type(class_type))
		for hbin in self.hbin_list:
			for cell in hbin.cells:
				if isinstance( cell.cell_type , class_type):
					print( "Hbin "+str(hbin.number())+" Cell: "+ str(cell.get_number()) )
					try:
						print( cell )
					except:
						print( "Cell at offset :" + str(cell.offset) + " couldnt be decoded properly")

	def print_reg_header(self):
		print( self.reg_header )

	def print_hbins(self):
		for hbin in self.hbin_list:
			print( hbin )

	def print(self):
		print( str(self.reg_header) +"\n")
		for hbin in self.hbin_list:
			print( str(hbin) )
			cells = hbin.cells
			for cell in cells:
				try:
					print(cell)
				except:
					print( "-----------------------Cell "+ str( cell.get_number() ) +"------------------------\n" )
					print( "Offset : "+ str( cell.offset ) + "\nAllocated: "+ str( cell.allocated ) )
					print( "Cell length: " + str( cell.length_int ) )
					print("Wasnt properly decoded")


