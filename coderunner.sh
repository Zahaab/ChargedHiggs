#!/usr/bin/bash

nice -n 1 nohup sh -c './execute test.txt >test.log' &

nice -n 1 nohup sh -c './execute test1.txt >test1.log' &

nice -n 1 nohup sh -c './execute test2.txt >test2.log;
./execute test3.txt >test3.log;
./execute test4.txt >test4.log;
./execute test5.txt >test5.log;
./execute test6.txt >test6.log;
./execute test7.txt >test7.log;
./execute test8.txt >test8.log' &
