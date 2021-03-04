#!/usr/bin/env bash

echo "This mic on??"
nice -n 1 nohup sh -c './execute mainConfigFiles/77p/Set_Lepton_1/config.txt' &
nice -n 1 nohup sh -c './execute mainConfigFiles/77p/Set_Lepton_1/config1.txt' &
nice -n 1 nohup sh -c './execute mainConfigFiles/77p/Set_Lepton_1/config2.txt' &
