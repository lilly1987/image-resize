import sys
from os import path
from ConsoleColor import print, console
from pathlib import *

sys.path.append( path.dirname( path.abspath(__file__) ) )

main=sys.argv.pop(0)
print(sys.argv)
for i in sys.argv:    
    if Path(i).is_dir():
        for f in Path(i).glob("**/*.*"):
            print(f)
    else:
        print(i)