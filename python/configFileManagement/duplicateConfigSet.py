import sys
from configFunctions import duplicateConfigSet

print(sys.argv)

if len(sys.argv) == 3:
    _, directory1, directory2 = sys.argv
    duplicateConfigSet(directory1, directory2)
elif len(sys.argv) == 4:
    _, directory1, directory2, filename = sys.argv
    duplicateConfigSet(directory1, directory2, filename)
