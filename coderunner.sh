#!/usr/bin/bash

nice -n 1 nohup sh -c './execute configFiles/configSet/config.txt >config.log' &

nice -n 1 nohup sh -c './execute configFiles/configSet/config1.txt >config1.log' &

nice -n 1 nohup sh -c './execute configFiles/configSet/config2.txt >config2.log;
./execute configFiles/configSet/config3.txt >config3.log;
./execute configFiles/configSet/config4.txt >config4.log;
./execute configFiles/configSet/config5.txt >config5.log;
./execute configFiles/configSet/config6.txt >config6.log;
./execute configFiles/configSet/config7.txt >config7.log;
./execute configFiles/configSet/config8.txt >config8.log' &
