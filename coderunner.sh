#!/usr/bin/bash

nice -n 1 nohup sh -c './execute "data/MC16a" "Wjets.root" "77p"  "."  0 90. 140. 70. 100. 30000. 30000. 200000. 200000. 1.0 1.0 2.5 250000. >test.log' &

nice -n 1 nohup sh -c './execute "data/MC16a" "ttbar.root" "77p"  "."  0 90. 140. 70. 100. 30000. 30000. 200000. 200000. 1.0 1.0 2.5 250000. >test1.log' &

nice -n 1 nohup sh -c './execute "data/MC16a" "data15.root" "77p"  "."  0 90. 140. 70. 100. 30000. 30000. 200000. 200000. 1.0 1.0 2.5 250000. > test2.log;
./execute "data/MC16a" "data16.root" "77p"  "."  0 90. 140. 70. 100. 30000. 30000. 200000. 200000. 1.0 1.0 2.5 250000. > test3.log;
./execute "data/MC16a" "diboson.root" "77p"  "."  0 90. 140. 70. 100. 30000. 30000. 200000. 200000. 1.0 1.0 2.5 250000.  >test4.log;
./execute "data/MC16a" "sig_Hplus_Wh_m1600-0.root" "77p"  "."  0 90. 140. 70. 100. 30000. 30000. 200000. 200000. 1.0 1.0 2.5 250000. >test5.log;
./execute "data/MC16a" "sig_Hplus_Wh_m400-0.root" "77p"  "."  0 90. 140. 70. 100. 30000. 30000. 200000. 200000. 1.0 1.0 2.5 250000. >test6.log;
./execute "data/MC16a" "sig_Hplus_Wh_m800-0.root" "77p"  "."  0 90. 140. 70. 100. 30000. 30000. 200000. 200000. 1.0 1.0 2.5 250000. >test7.log;
./execute "data/MC16a" "singleTop.root" "77p"  "."  0 90. 140. 70. 100. 30000. 30000. 200000. 200000. 1.0 1.0 2.5 250000. >test8.log;
./execute "data/MC16a" "Zjets.root" "77p"  "."  0 90. 140. 70. 100. 30000. 30000. 200000. 200000. 1.0 1.0 2.5 250000. >test9.log;
./execute "data/MC16a" "ttbarSherpa.root" "77p"  "."  0 90. 140. 70. 100. 30000. 30000. 200000. 200000. 1.0 1.0 2.5 250000. >test10.log' &
