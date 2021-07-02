#!/usr/bin/env bash

FILES=/home/ap17080/Thesis/ChargedHiggs/testConfigFiles/*
for configFolder in $FILES
do 
    config=$configFolder
    echo "Processing" $config
    executeprocesses="$pgrep MakeStackPlots.py -u ap17080 | wc -l"
    nice -n 1 sh -c "python MakeStackPlots.py $config"
    while [ $executeprocesses -gt 0 ]
    do
      sleep 1s
      executeprocesses="$pgrep MakeStackPlots.py -u ap17080 | wc -l"
    done
done
