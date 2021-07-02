#!/usr/bin/env bash

FILES=/home/ap17080/Thesis/ChargedHiggs/mainConfigFiles/*

for configFolder in $FILES
do 
    configSets=$configFolder/*
    executeprocesses="$(pgrep execute -u ap17080 | wc -l)"
    for configSet in $configSets
    do
        configs=$configSet/*
        for config in $configs
        do
            echo "Begining to process" $config
            nice -n 1 sh -c "./execute $config" 
            executeprocesses="$(pgrep execute -u ap17080 | wc -l)"
            while [ $executeprocesses -gt 0 ]
            do
                echo "1 processes running"
                sleep 10s
                executeprocesses="$(pgrep execute -u ap17080 | wc -l)"
            done
        done
    done
done 
