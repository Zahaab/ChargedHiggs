#ifndef CONFIGPARSER_H
#define CONFIGPARSER_H
#include <unordered_map>
#include <string>
#include <fstream>
#include <algorithm>

std::unordered_map<std::string, std::string> parseConfig(std::string path)
{
    std::string line;
    std::string key;
    std::string value;
    std::string delimiter = "=";
    std::int8_t del_index;
    std::unordered_map<std::string, std::string> configuration;

    std::ifstream MyReadFile("test.txt");
    while (std::getline(MyReadFile, line))
    {
        line.erase(std::remove_if(line.begin(), line.end(), ::isspace), line.end());
        del_index = line.find(delimiter);
        key = line.substr(0, del_index);
        line.erase(0, del_index + delimiter.length());
        value = line;
        configuration[key] = value;
    }
    return configuration;
}

#endif