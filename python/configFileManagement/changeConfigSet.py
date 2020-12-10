import sys
from configFunctions import changeConfigSet, changeConfig

_, directory, changeVariable, newValue = sys.argv
changeConfigSet(directory, changeVariable, newValue)
