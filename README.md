This tool is a registry parser.  The way it works is by reading from an input text file
where each line is a path to the key to parse.  It is somewhat fragile 
and was developed in a week for my Digital Forensics final project.

Example:
	./PoopyParser.exe ./NTUSER.dat ./input.txt

The contents of the input file must be formatted like this:

root\AppEvents\EventLabels
root\Some key\spaces dont matter

-------------

There is no compiling the source code as it was written in Python, an interpreted language.
To run from source, you must install the latest version of Python.
	-The binary file was created with pyinstaller using the command 'pyinstaller --onefile PoopyParser.py'

*Error Notes*
If the subkeys of a given key are stored in the "ri" type of sublist (which has pointers to 
additional subkey lists) then the program will not work.  After creating this tool, it seems like 
these types of subkey lists are few.

Keys with odd names like 🌎🌏🌍 are unable to be parsed or any of their subkeys.

Also, sometimes for REG_SZ or REG_MULTI_SZ data types, the string is not encoded as per the format 
specified by the Windows page: https://docs.microsoft.com/en-us/windows/win32/shell/hkey-type
	- the string printed out will be "Sorry couldn't decode"

*Additional Notes*
After hastily developing this program, I see in many areas ways to improve it.
There is alot of boiler plate code, and the organization behind the program is not how I would 
write it now.  In addition, the tool parses the entire registry before outputing information, making
it slow, whereas I could have parsed in a better order only the information that was requested.
Finally, the tool works relatively fast for most hive files, but for extremely large ones like the software
hive, the tool takes minutes. 
 
