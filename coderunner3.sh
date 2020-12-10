#!/usr/bin/bash

nice -n 1 nohup sh -c './execute configFiles/configSet3/config.txt >configFiles/configLogs/Set3config.log' &

nice -n 1 nohup sh -c './execute configFiles/configSet3/config1.txt >configFiles/configLogs/Set3config1.log' &

nice -n 1 nohup sh -c './execute configFiles/configSet3/config2.txt >configFiles/configLogs/Set3config2.log;
./execute configFiles/configSet3/config3.txt >configFiles/configLogs/Set3config3.log;
./execute configFiles/configSet3/config4.txt >configFiles/configLogs/Set3config4.log;
./execute configFiles/configSet3/config5.txt >configFiles/configLogs/Set3config5.log;
./execute configFiles/configSet3/config6.txt >configFiles/configLogs/Set3config6.log;
./execute configFiles/configSet3/config7.txt >configFiles/configLogs/Set3config7.log;
./execute configFiles/configSet3/config8.txt >configFiles/configLogs/Set3config8.log' &