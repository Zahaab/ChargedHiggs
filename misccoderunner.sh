#!/usr/bin/bash

nice -n 1 nohup sh -c './execute configFiles/miscConfig/configSet2.txt >configFiles/configLogs/miscConfigSet2.log' &

nice -n 1 nohup sh -c './execute configFiles/miscConfig/configSet3.txt >configFiles/configLogs/miscConfigSet3.log' &