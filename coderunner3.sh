nice -n 1 nohup sh -c './execute configFiles/configSet3/config.txt' &

nice -n 1 nohup sh -c './execute configFiles/configSet3/config1.txt' &

nice -n 1 nohup sh -c './execute configFiles/configSet3/config2.txt;
./execute configFiles/configSet3/config3.txt;
./execute configFiles/configSet3/config4.txt;
./execute configFiles/configSet3/config5.txt;
./execute configFiles/configSet3/config6.txt;
./execute configFiles/configSet3/config7.txt;
./execute configFiles/configSet3/config8.txt' &