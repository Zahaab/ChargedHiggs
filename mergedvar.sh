#!/usr/bin/bash


nice -n 1 nohup sh -c './execute "data/MC16a" "data15.root" "77p"  "."  0 90. 140. 70. 100. > test.log;
./execute "data/MC16a" "data16.root" "77p"  "."  0 90. 140. 70. 100. > test1.log;
./execute "data/MC16a" "diboson.root" "77p"  "."  0 90. 140. 70. 100.  >test2.log' &

nice -n 1 nohup sh -c './execute "data/MC16a" "sig_Hplus_Wh_m1600-0.root" "77p"  "."  0 90. 140. 70. 100. >test3.log;
./execute "data/MC16a" "sig_Hplus_Wh_m400-0.root" "77p"  "."  0 90. 140. 70. 100. >test4.log' &

nice -n 1 nohup sh -c './execute "data/MC16a" "sig_Hplus_Wh_m800-0.root" "77p"  "."  0 90. 140. 70. 100. >test5.log;
./execute "data/MC16a" "singleTop.root" "77p"  "."  0 90. 140. 70. 100. >test6.log' &

nice -n 1 nohup sh -c './execute "data/MC16a" "ttbar.root" "77p"  "."  0 90. 140. 70. 100. >test7.log;
./execute "data/MC16a" "Wjets.root" "77p"  "."  0 90. 140. 70. 100. >test8.log' &


nice -n 1 nohup sh -c './execute "data/MC16a" "Zjets.root" "77p"  "."  0 90. 140. 70. 100. >test9.log;
./execute "data/MC16a" "ttbarSherpa.root" "77p"  "."  0 90. 140. 70. 100. >test10.log' &
