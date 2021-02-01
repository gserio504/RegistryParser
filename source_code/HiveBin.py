import regutils
from Cell import *
from bitstring import BitArray

class HiveBin:

	def __init__( self , binary , beg_offset , hbin_number , hive):
		self.hive = hive
		self.hbin_number = hbin_number
		self.binary = binary
		self.beg_offset = beg_offset
		self.magic_number = regutils.bytes_to_string( binary[0:4] )
		self.dist_first_hbin = regutils.bytes_to_int( binary[4:8] )
		self.hive_bin_size = regutils.bytes_to_int( binary[8:12] )
		self.next_hbin_offset = regutils.bytes_to_int( binary[28:32] ) #relative to start of this hbin
		self.first_cell_offset = 32 + self.beg_offset 
		self.cells = self.find_cells()

	def number(self):
		return self.hbin_number

	def find_cell( self, offset ):
		first = 0
		last = len(self.cells) - 1
		while first <= last:
			middle = int( (first+last)/2 )
			cell = self.cells[middle]
			if offset == cell.get_offset():
				return middle
			elif offset < cell.get_offset():
				last = middle - 1
			else:
				first = middle + 1
		return -1

	def offset(self):
		return self.beg_offset

	def length( self ):
		return self.hive_bin_size


	def find_cells(self):
		cells = []
		abs_offset = self.first_cell_offset
		relative_offset = 32 #the first cell starts at hbin_off + 32
		end_of_hbin = self.beg_offset + self.hive_bin_size
		count = 0

		while abs_offset < end_of_hbin: #both here are relative to the start of the hbin
			length_bytes = self.binary[ relative_offset : (relative_offset+4) ] #the length of the cell is in its first 4 bytes
			if regutils.isNegative( length_bytes ): #then the cell is allocated
				cell_length = regutils.negate_signed( length_bytes ) #get the length by taking the abolute value of the number
			else:
				cell_length = regutils.bytes_to_int( length_bytes )
			cells.append(  Cell(self.binary[ relative_offset : relative_offset+cell_length] , abs_offset , count , self.hive)  )#create a new cell with its binary, and its absolute offset
			self.hive.mark_for_reinitialization( cells[count] ) # if the cell is a data cell, a value list or data list
			#then it has no magic number... scan the cells containing information about these cells and add to a list
			#their offsets, type, and optionally the number of elements.... then in hive when hbins are done parsing
			#the cells, go through the list and reinitialize them to their proper class by calling the appropriate
			#reinitialization method in the cell class
			relative_offset += cell_length
			abs_offset += cell_length
			count+=1

		return cells


	def print_cells( self ):
		print("------Cells------\n")
		for cell in self.cells:
			print( str(cell) +"\n")


	def __str__( self ):
		string = "--------------Hbin "+ str(self.hbin_number)+"--------------"
		string += "\n" 
		string += "Offset: "+ str( self.beg_offset )
		string += "\nMagic Number: " + self.magic_number
		string += "\nDistance from first hbin: " + str( self.dist_first_hbin )
		string += "\nHbin size: " + str( self.hive_bin_size )
		string += "\nRelative offset of next hbin: " + str( self.next_hbin_offset )
		string += "\nFirst cell offset: " + str( self.first_cell_offset )
		
		return string


