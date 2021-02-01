class Reinitializer:

	#need to know the type of cell to reinitialize to ( Data  or RegList (data or value (list) ) ) 
	def __init__( self , cell_offset , cell_type , num_elements ):
		self.cell_offset = cell_offset + 4096 #pointers relative to start of first hbin?
		self.cell_type = cell_type
		self.num_elements = num_elements

	def __str__(self):
		string = ( "\n---Reinitializer" +
				   "\nCell's offset : " +str(self.cell_offset) +
				   "\nCell's type : " + self.cell_type +
				   "\nNumber of elements : "+str(self.num_elements) +"\n" )
		return string