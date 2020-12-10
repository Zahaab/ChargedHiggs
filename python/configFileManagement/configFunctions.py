import os


def changeConfig(path, changeVariable, newValue):
    with open(path, 'r') as config:
        configuration = []
        config_index = ""
        for count, line in enumerate(config):
            configuration.append(line)
            if changeVariable in line:
                config_index = count
                break
        configuration.extend(config.readlines())

        if config_index == "":
            raise Exception("Chosen Variable not found in config")

        configuration[config_index] = changeVariable + \
            " = "+str(newValue)+"\n"
    with open(path, 'w') as config:
        config.writelines(configuration)


def changeConfigSet(directory, changeVariable, newValue):
    for configfile in os.listdir(directory):
        print(configfile)
        changeConfig(directory+"/"+configfile, changeVariable, newValue)


def duplicateConfig(path, directory, filename="config", config_limit=100):
    with open(path, 'r') as config:
        configuration = config.readlines()
        filename = filename.replace(".txt", "")
        print(filename)
        filemade = False
        i = -1
        while filemade == False:
            print(filename)
            new_config_name = ""
            i += 1
            if i > 100:
                raise Exception(
                    "Error, check inputs, if directory has many config files, change config_limit")
            print(new_config_name)
            if i == 0:
                new_config_name = filename + ".txt"
            else:
                new_config_name = filename + str(i) + ".txt"
            print(new_config_name)
            if os.path.isfile(directory + "/" + new_config_name) == False:
                print(new_config_name)
                new_config = open(directory + "/" + new_config_name, "w+")
                new_config.writelines(configuration)
                new_config.close()
                filemade = True
    return


def duplicateConfigSet(directory1, directory2, filename="config"):
    try:
        os.mkdir(directory2)
    except OSError:
        print("Creation of the directory %s failed, or it already exists" % directory2)
    else:
        print("Successfully created the directory %s " % directory2)
    for configfile in os.listdir(directory1):
        if filename == "config":
            duplicateConfig(directory1 + "/" + configfile, directory2)
        else:
            duplicateConfig(directory1 + "/" + configfile,
                            directory2, filename)
