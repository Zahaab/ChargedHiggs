import sys
import os
import math
import re


def getChosenFiles(chosenFiles, path, hmlb, hmub, wmlb, wmub, met_ptv, lep_ptv, jet0_ptv, jet1_ptv, lep_jet0_angle, lep_jet1_angle, hw_angle, solo_jet_ptv):
    graph_var = [hmlb, hmub, wmlb, wmub, met_ptv, lep_ptv,
                 jet0_ptv, jet1_ptv, lep_jet0_angle, lep_jet1_angle, hw_angle, solo_jet_ptv]
    varNums = path.split("_")[-1].replace(".root", "")
    path_var = varNums.split("-")
    vardif = [i for i, j in zip(graph_var, path_var) if str(i) not in str(j)]
    if vardif == []:
        for key in chosenFiles:
            if key in path:
                chosenFiles[key] = path


def getDataFiles(hmlb, hmub, wmlb, wmub, met_ptv, lep_ptv, jet0_ptv, jet1_ptv, lep_jet0_angle, lep_jet1_angle, hw_angle, solo_jet_ptv):
    chosenFiles = {"sig_Hplus_Wh_m400-0": 0,
                   "sig_Hplus_Wh_m800-0": 0,
                   "sig_Hplus_Wh_m1600-0": 0,
                   "ttbarSherpa": 0,
                   "Wjets": 0,
                   "diboson": 0,
                   "singleTop": 0}
    arr = os.listdir("../PlotFiles")
    for i in arr:
        getChosenFiles(chosenFiles, i, hmlb, hmub, wmlb, wmub, met_ptv, lep_ptv,
                       jet0_ptv, jet1_ptv, lep_jet0_angle, lep_jet1_angle, hw_angle, solo_jet_ptv)
    for key in chosenFiles:
        if chosenFiles[key] == 0:
            raise Exception("all files not found" + key)
    return chosenFiles


files = getDataFiles(hmlb, hmub, wmlb, wmub, met_ptv, lep_ptv,
                     jet0_ptv, jet1_ptv, lep_jet0_angle, lep_jet1_angle, hw_angle, solo_jet_ptv)
