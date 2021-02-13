#!/usr/bin/bash

nice -n 1 nohup sh -c './execute configFiles/miscConfig/config400.txt ' &
nice -n 1 nohup sh -c './execute configFiles/miscConfig/config800.txt ' &
nice -n 1 nohup sh -c './execute configFiles/miscConfig/config1600.txt ' &