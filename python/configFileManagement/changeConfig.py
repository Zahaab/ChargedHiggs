import sys
from configFunctions import changeConfig

_, path, changeVariable, newValue = sys.argv
changeConfig(path, changeVariable, newValue)
