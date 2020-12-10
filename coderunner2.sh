nice -n 1 nohup sh -c './execute configFiles/configSet2/config.txt' &

nice -n 1 nohup sh -c './execute configFiles/configSet2/config1.txt' &

nice -n 1 nohup sh -c './execute configFiles/configSet2/config2.txt;
./execute configFiles/configSet2/config3.txt;
./execute configFiles/configSet2/config4.txt;
./execute configFiles/configSet2/config5.txt;
./execute configFiles/configSet2/config6.txt;
./execute configFiles/configSet2/config7.txt;
./execute configFiles/configSet2/config8.txt' &