from cx_Freeze import setup, Executable

base = None    

executables = [Executable("Driver.py", base=base)]

packages = ["idna","bitstring","sys","re"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "PoopyParser",
    options = options,
    version = "<any number>",
    description = '<any description>',
    executables = executables
)
