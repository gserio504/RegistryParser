import regutils
from Hive import *

class RegList:

	def __init__( self , binary , offset , num_elements, list_type , hive):
		self.hive = hive
		self.type = list_type
		self.binary = binary
		self.offset = offset
		self.length = len(binary)
		self.num_elements = num_elements
		self.elements = []
		for x in range( self.num_elements ):
			self.elements.append( self.binary[ 4 * x : 4 + 4 * x] )
		self.padding = self.binary[ 4 * self.num_elements : self.length ]

	def get_offset(self):
		return self.offset

	def get_length(self):
		return self.length

	def get_size(self):
		return self.num_elements

	def get_elements(self):
		return self.elements

	def get_padding(self): 
		return self.padding

	def get_value_records(self):
		records = []
		for x in range( self.get_size() ):
			records.append(  self.hive.find_cell( regutils.bytes_to_int(self.elements[x]) + 4096 ).cell_type   )
		return records

	def get_type(self):
		if self.type == "data":
			return "Data Fragment List"
		elif self.type == "value":
			return "Value List"

	def __str__(self):
		string = (  "\n--------------"+self.get_type()+"--------------"
					"\nNumber of Elements : " + str( self.get_size() ) +
					"\n----Elements----"
				 )
		for element in self.elements:
			string+= "\nOffset : "+regutils.bytes_to_hexstring( element )+" ("+str(regutils.bytes_to_int(element))+")"
		string+="\nPadding : "+str( self.get_padding() )
		return string