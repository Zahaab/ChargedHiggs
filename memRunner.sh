#!/usr/bin/bash

FILES=/home/ap17080/Thesis/ChargedHiggs/configFiles/miscConfig*
for configSets in $FILES
do 
    configSet=$configSets/*
    executeprocesses="$(pgrep execute -u ap17080 | wc -l)"
    for config in $configSet
    do
        echo "Begining to process" $config
        nice -n 1 nohup sh -c "./execute $config" &
        executeprocesses="$(pgrep execute -u ap17080 | wc -l)"
        while [ $executeprocesses -gt 7 ]
        do
            echo "8 processes running"
            sleep 20m
            executeprocesses="$(pgrep execute -u ap17080 | wc -l)"
        done
    done
done 

# FILES=/home/ap17080/Thesis/ChargedHiggs/configFiles/configSet*
# for configSets in $FILES
# do 
#     configSet=$configSet*
#     executeprocesses="$(pgrep exectue -u ap17080 | wc -l)"
#     for config in $configSet
#     do
#         echo $config
#         executeprocesses=$(( $executeprocesses + 1))
#         while [ $executeprocesses -gt 5 ]
#         do
#             echo "6 processes running"
#             sleep 5s
#             echo "process ended"
#             executeprocesses=$(( $executeprocesses - 1))
#         done
#     done
# done 
