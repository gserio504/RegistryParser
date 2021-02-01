import regutils

class Data:


	def __init__( self , binary , offset , data_type , data_size): #MAYBE MAKE LENGTH FROM THE FIELD IN VALUE RECORD
		self.binary = binary
		self.offset = offset
		self.data_type = data_type
		self.length = data_size
		

	#based on data type return the data as a string
	def get_data(self):
		function = self.types.get( self.get_data_type() )
		return function()

	def get_data_type(self):
		return self.data_type

	def parseREG_NONE(self):
		return "None"

	def parseREG_SZ(self):
		string_bytes = self.binary[0:self.length]
		#string = string_bytes.decode("UTF-16-le","ignore")
		#isUnicode = self.test_string(string)
		try:
			if string_bytes[1] == 0:
				return string_bytes.decode("UTF-16-le","strict")
			else:
				return string_bytes.decode("ascii","strict")
		except:
			return "Couldnt be decoded"

	def parseREG_BINARY(self):
		string = ""
		for x in range( self.length):
			if self.binary[x] == 0:
				string+="00-"
			else:
				string+=hex(self.binary[x]).lstrip("0x")+"-"
		return string.rstrip("-") #remove extra '-' from AB-CE-8E-

	def parseREG_DWORD(self):
		return str( regutils.bytes_to_int(self.binary[0:4]) )

	def parseREG_DWORD_BIG_ENDIAN(self):
		endian_switch = regutils.reverse_endian( self.binary[0:4] )
		return str( regutils.bytes_to_int(endian_switch) )

		#aight so sometimes these dont follow this format.... and could even be ascii? wtf
	def parseREG_MULTI_SZ(self): #strings where a null byte is a line seperator and two null bytes indicates end of strings
		string=""
		x = 0
		try:
			while x < self.length:
				if self.binary[x] == 0 and self.binary[x+1] == 0 and self.binary[x+2] == 0:
					break
				elif self.binary[x] == 0: #and the next character is 0
					string+="\n"
				else:
					uni_char = self.binary[x:x+2] #UTF-16 is two bytes per character
					string += uni_char.decode("UTF-16-le")#,"strict")
				x+=2
			return string
		except:
			return string


	def parseREG_QWORD(self):
		return str(  regutils.bytes_to_int( self.binary[0:8] )  ) #note this method works for any size of bytes not just 4

	def parseNOTHING(self):
		return "Sorry I didnt parse that!\nBytes : " + self.parseREG_BINARY()

	types = {  "REG_NONE" : parseREG_NONE ,
  					"REG_SZ" : parseREG_SZ ,
				    "REG_EXPAND_SZ" : parseREG_SZ , #same as REG_SZ just a longer string
				    "REG_BINARY" : parseREG_BINARY ,
				    "REG_DWORD" : parseREG_DWORD ,
				    "REG_DWORD_BIG_ENDIAN" : parseREG_DWORD_BIG_ENDIAN ,
		    		"REG_LINK" : parseREG_SZ ,
				    "REG_MULTI_SZ" : parseREG_MULTI_SZ ,
				    "REG_RESOURCE_LIST" : parseNOTHING ,
		    		"REG_FULL_RESOURCE_DESCRIPTOR" : parseNOTHING ,
					"REG_RESOURCE_REQUIREMENTS_LIST" : parseNOTHING ,
		    		"REG_QWORD" : parseREG_QWORD ,
		    		"REG_QWORD_LITTLE_ENDIAN" : parseREG_QWORD}

		#based on data type return the data as a string
	def get_data(self):
		function = self.types.get( self.get_data_type() , self.parseNOTHING() )
		#if function is None:
		#	return "Didn't parse"
		return function(self)

	def __str__(self):
		string = (  "--------------Data--------------" +
					"\nType : " + self.get_data_type() + 
					"\nData Length : "+ str(self.length) +
					"\nData : " + self.get_data()
				 )
		return string
