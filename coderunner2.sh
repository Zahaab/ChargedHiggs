#!/usr/bin/bash

nice -n 1 nohup sh -c './execute configFiles/configSet2/config.txt >configFiles/configLogs/Set2config.log' &

nice -n 1 nohup sh -c './execute configFiles/configSet2/config1.txt >configFiles/configLogs/Set2config1.log' &

nice -n 1 nohup sh -c './execute configFiles/configSet2/config2.txt >configFiles/configLogs/Set2config2.log;
./execute configFiles/configSet2/config3.txt >configFiles/configLogs/Set2config3.log;
./execute configFiles/configSet2/config4.txt >configFiles/configLogs/Set2config4.log;
./execute configFiles/configSet2/config5.txt >configFiles/configLogs/Set2config5.log;
./execute configFiles/configSet2/config6.txt >configFiles/configLogs/Set2config6.log;
./execute configFiles/configSet2/config7.txt >configFiles/configLogs/Set2config7.log;
./execute configFiles/configSet2/config8.txt >configFiles/configLogs/Set2config8.log' &