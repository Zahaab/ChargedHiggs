import sys
from configFunctions import duplicateConfig


if len(sys.argv) == 3:
    _, path, directory = sys.argv
    duplicateConfig(path, directory)
elif len(sys.argv) == 4:
    if sys.argv[3] == int:
        _, path, directory, config_limit = sys.argv
        duplicateConfig(path, directory, filename="config",
                        config_limit=config_limit)
    elif sys.argv[3] == str:
        _, path, directory, filename = sys.argv
        duplicateConfig(path, directory, filename=filename, config_limit=100)
else:
    _, path, directory, filename, config_limit = sys.argv
    duplicateConfig(path, directory, filename, config_limit)
