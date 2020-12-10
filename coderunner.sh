#!/usr/bin/bash

nice -n 1 nohup sh -c './execute configFiles/configSet/config.txt >configFiles/configLogs/Set1config.log' &

nice -n 1 nohup sh -c './execute configFiles/configSet/config1.txt >configFiles/configLogs/Set1config1.log' &

nice -n 1 nohup sh -c './execute configFiles/configSet/config2.txt >configFiles/configLogs/Set1config2.log;
./execute configFiles/configSet/config3.txt >configFiles/configLogs/Set1config3.log;
./execute configFiles/configSet/config4.txt >configFiles/configLogs/Set1config4.log;
./execute configFiles/configSet/config5.txt >configFiles/configLogs/Set1config5.log;
./execute configFiles/configSet/config6.txt >configFiles/configLogs/Set1config6.log;
./execute configFiles/configSet/config7.txt >configFiles/configLogs/Set1config7.log;
./execute configFiles/configSet/config8.txt >configFiles/configLogs/Set1config8.log' &
