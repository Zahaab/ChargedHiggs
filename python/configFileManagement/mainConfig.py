import sys
from configFunctions import mainConfig

print(sys.argv)

_, directory1, graphdir, changeVariable = sys.argv

mainConfig(directory1, graphdir, changeVariable)
