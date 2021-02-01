from Hive import *
import regutils
import sys
import re

def filter_lines(lines):
	try:
		lines.remove("")#remove empty lines
	except:
		pass #there were no empty lines
	pattern = re.compile("root(\\\\)\\S+")
	for x in range( len(lines) ):
		line = lines[x]
		if not pattern.match(line):
			print("Invalid formatting of input file on line "+str(x)+".  \n"+line)
			sys.exit()
	return lines

def get_info_helper( subkey ):
	info = subkey.get_name() + "	Last Modified: "+subkey.get_timestamp() + " (Your timezone)"
	value_list = subkey.list_values()
	info += "\n--Values--\n"
	for value in value_list:
		value = subkey.get_value( value )
		info += "\n"+value.get_name() + "	" + value.get_data_type()
		try:
			info+="	"+value.get_data()
		except:
			info+="	Couldnt decode data properly"
	return info + "\n"

def get_info( root , line ):
	info = ""
	key = root.get_subkey( line )
	if not isinstance( key , type( KeyRecord() ) ):
		print( line + " has an invalid key name.  Exiting.")
		sys.exit()
	info = get_info_helper( key )
	return info


def get_output( hive_file , lines ):
	output = ""
	hive = Hive( hive_file )
	#print( hive.get_root().list_subkeys() )
	for line in lines:
		line = line.lstrip("root\\")
		output += get_info( hive.get_root() , line ) + "\n"
	return output





if len(sys.argv) < 2 or sys.argv[1] == "-help":
	prompt = ( "To use this program: "+
			   "\n\nPoopyParser path/Registry_Hive path/input.txt > output.txt"+
			   "\nExample: PoopyParser ./NTUSER.dat ./input.txt > output.txt"
			   "\n\nThe format of the input file is as follows: "+
			   "\nEach line of the file must contain the path to the key for which to display values "+
			   "\nExamples: "+
			   "\nroot\\AppEvents"+
			   "\nroot\\AppEvents\\EventLabels"+
			   "\nroot\\AppEvents\\EventLabels\\A Key\\something" +
			   "\n\n*Note* The names of keys are case sensitive" +
			   "\n WARNING : The program works, but for extremely large hives it takes forever since I parse the whole hive first"
			  )
	print( prompt )
else:
	try:
		hive_file = sys.argv[1] 
		input_file = open( sys.argv[2] ,"r")

		input_content = input_file.read()
		input_file.close()
	except:
		print("Either the input file does not exist or a path was entered incorrectly")
	lines = filter_lines(input_content.split("\n")) #what happens if /r/n
	output = ""
	try:
		output = get_output( hive_file , lines )
	except:
		print("Fuqq it broke.... this was the last line of defense")
	print( output )

	sys.exit()




#root = Hive(sys.argv[1]).get_root()

def list_all( root ):
	print( root.get_name() )
	values = root.list_values()
	if len(values) > 0:
		for value in values:
			value = root.get_value( value )
			print( value.get_name() + " " , end="")
			print( value.get_data_type() + " " , end="")
			try:
				print( value.get_data() )
			except:
				print("Couldnt be decoded")
	subkeys = root.list_subkeys()
	if len(subkeys) > 0:
		print( subkeys )
		for sk in subkeys:
			key = root.get_subkey(sk)
			list_all( key )

#list_all( root )


