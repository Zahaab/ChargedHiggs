#ifndef CONFIGPARSER_H
#define CONFIGPARSER_H
#include <unordered_map>
#include <string>
#include <vector>
#include <fstream>
#include <algorithm>
#include <iostream>

std::unordered_map<std::string, std::string> parseConfig(std::string path)
{
    std::string line;
    std::string key;
    std::string value;
    std::string delimiter = "=";
    std::int8_t del_index;
    std::unordered_map<std::string, std::string> configuration;

    std::ifstream MyReadFile(path);
    while (std::getline(MyReadFile, line))
    {
        line.erase(std::remove_if(line.begin(), line.end(), ::isspace), line.end());
        del_index = line.find(delimiter);
        key = line.substr(0, del_index);
        line.erase(0, del_index + delimiter.length());
        value = line;
        configuration[key] = value;
    }
    configuration.erase("-----------");
    configuration.erase("------------");
    return configuration;
}

std::vector<std::string> parseDataPeriodes(std::unordered_map<std::string, std::string> config)
{
    std::string path = config["path"];
    std::vector<std::string> MCDataPeriodes;

    if (path.find("MC16a") != std::string::npos)
    {
        MCDataPeriodes.push_back("MC16a");
        if (config["Stack_MC16d"] == "Enable")
        {
            MCDataPeriodes.push_back("MC16d");
        }
        if (config["Stack_MC16e"] == "Enable")
        {
            MCDataPeriodes.push_back("MC16e");
        }
    }
    if (path.find("MC16d") != std::string::npos)
    {
        MCDataPeriodes.push_back("MC16d");
        if (config["Stack_MC16a"] == "Enable")
        {
            MCDataPeriodes.push_back("MC16a");
        }
        if (config["Stack_MC16e"] == "Enable")
        {
            MCDataPeriodes.push_back("MC16e");
        }
    }
    if (path.find("MC16e") != std::string::npos)
    {
        MCDataPeriodes.push_back("MC16e");
        if (config["Stack_MC16d"] == "Enable")
        {
            MCDataPeriodes.push_back("MC16d");
        }
        if (config["Stack_MC16a"] == "Enable")
        {
            MCDataPeriodes.push_back("MC16a");
        }
    }
    return MCDataPeriodes;
}

#endif