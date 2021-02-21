#!/usr/bin/bash

FILES=/home/ap17080/Thesis/ChargedHiggs/mainConfigFiles/*
for configFolder in $FILES
do 
    configSets=$configFolder/*
    executeprocesses="$(pgrep MakeStackPlots.py -u ap17080 | wc -l)"
    for configSet in $configSets
    do
        configs=$configSet/*
        for config in $configs
        do
            nice -n 1 nohup sh -c "python MakeStackPlots.py $config" 
            
        done
    done
done 


