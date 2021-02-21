# -*- coding: utf-8 -*-
# python

import sys
import os
from configparser import configParser, getConfigData, getPlotFiles, getaxisLabels
import glob
import math
import re
from ROOT import *
from array import *

_, config_path = sys.argv
config = configParser(config_path)
MCDataPeriodes = getConfigData(config, "Stack_")
histoNames = getConfigData(config, "Graph_")
btagStrategies = getConfigData(config, "Btag_")
dataPeriodeStack = "-".join(MCDataPeriodes)
histoFiles = {i: getPlotFiles(config, i) for i in MCDataPeriodes}
plotEvents = getConfigData(config, "Plot_")

outputdir = str("../Plots/" + config["WP"] + "/" + "StackPlots" + "/" + dataPeriodeStack + "-" + config["Higgs_mass_lower_bound"] + "-" + config["Higgs_mass_upper_bound"] + "-" +
                config["Wboson_mass_lower_bound"] + "-" + config["Wboson_mass_upper_bound"] + "-" + config["Missing_transverse_momentum"] + "-" +
                config["Lepton_transverse_momentum"] + "-" + config["2Jets_Jet1_transverse_momentum"] + "-" +
                config["2Jets_Jet2_transverse_momentum"] + "-" + config["2Jets_Jet1_lepton_angle"] + "-" + config["2Jets_Jet2_lepton_angle"] + "-" +
                config["Higgs_Wboson_angle"] + "-" + config["1Jet_Jet_transverse_momentum"])

try:
    os.mkdir(outputdir)
except OSError:
    print "Creation of the directory %s failed" % outputdir
else:
    print "Successfully created the directory %s " % outputdir


def sumHistosList(histo_list):
    resultHisto = 0
    if len(histo_list) > 0:
        for i in histo_list:
            if resultHisto == 0:
                resultHisto = i
            else:
                resultHisto += i
    return resultHisto


HistoName = "mH"
btagStrategy = "TwoTags"
dscale = 1.223695
escale = 1.61419497
for Region in ["Merged_LepN_SR"]:
    if config["Plot_sig_Hplus_Wh_m400-0"] == "Enable":
        h_sig_Hplus_m400list = []
        if config["Stack_MC16a"] == "Enable":
            file1a = TFile.Open("../PlotFiles/" +
                                histoFiles["MC16a"]["sig_Hplus_Wh_m400-0"], "READ")
            dir1a = file1a.GetDirectory(
                "Nominal").GetDirectory(HistoName)
            h_sig_Hplus_m400a = dir1a.Get(
                "sig_Hplus_Wh_m400-0_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
            h_sig_Hplus_m400list.append(h_sig_Hplus_m400a)
        if config["Stack_MC16d"] == "Enable":
            file1d = TFile.Open("../PlotFiles/" +
                                histoFiles["MC16d"]["sig_Hplus_Wh_m400-0"], "READ")
            dir1d = file1d.GetDirectory(
                "Nominal").GetDirectory(HistoName)
            h_sig_Hplus_m400d = dir1d.Get(
                "sig_Hplus_Wh_m400-0_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
            h_sig_Hplus_m400d.Scale(dscale)
            h_sig_Hplus_m400list.append(h_sig_Hplus_m400d)
        if config["Stack_MC16e"] == "Enable":
            file1e = TFile.Open("../PlotFiles/" +
                                histoFiles["MC16e"]["sig_Hplus_Wh_m400-0"], "READ")
            dir1e = file1e.GetDirectory(
                "Nominal").GetDirectory(HistoName)
            h_sig_Hplus_m400e = dir1e.Get(
                "sig_Hplus_Wh_m400-0_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
            h_sig_Hplus_m400e.Scale(escale)
            h_sig_Hplus_m400list.append(h_sig_Hplus_m400e)

        h_sig_Hplus_m400 = sumHistosList(h_sig_Hplus_m400list)
        h_sig_Hplus_m400.SetLineColor(kBlack)
        h_sig_Hplus_m400.SetLineStyle(7)

    if config["Plot_sig_Hplus_Wh_m800-0"] == "Enable":
        h_sig_Hplus_m800list = []
        if config["Stack_MC16a"] == "Enable":
            file2a = TFile.Open("../PlotFiles/" +
                                histoFiles["MC16a"]["sig_Hplus_Wh_m800-0"], "READ")
            dir2a = file2a.GetDirectory(
                "Nominal").GetDirectory(HistoName)
            h_sig_Hplus_m800a = dir2a.Get(
                "sig_Hplus_Wh_m800-0_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
            h_sig_Hplus_m800list.append(h_sig_Hplus_m800a)
        if config["Stack_MC16d"] == "Enable":
            file2d = TFile.Open("../PlotFiles/" +
                                histoFiles["MC16d"]["sig_Hplus_Wh_m800-0"], "READ")
            dir2d = file2d.GetDirectory(
                "Nominal").GetDirectory(HistoName)
            h_sig_Hplus_m800d = dir2d.Get(
                "sig_Hplus_Wh_m800-0_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
            h_sig_Hplus_m800d.Scale(dscale)
            h_sig_Hplus_m800list.append(h_sig_Hplus_m800d)
        if config["Stack_MC16e"] == "Enable":
            file2e = TFile.Open("../PlotFiles/" +
                                histoFiles["MC16e"]["sig_Hplus_Wh_m800-0"], "READ")
            dir2e = file2e.GetDirectory(
                "Nominal").GetDirectory(HistoName)
            h_sig_Hplus_m800e = dir2e.Get(
                "sig_Hplus_Wh_m800-0_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
            h_sig_Hplus_m800e.Scale(escale)
            h_sig_Hplus_m800list.append(h_sig_Hplus_m800e)

        h_sig_Hplus_m800 = sumHistosList(h_sig_Hplus_m800list)
        h_sig_Hplus_m800.SetLineColor(kBlue)
        h_sig_Hplus_m800.SetLineStyle(7)


Region = "Merged_LepN_SR"
f3 = TFile.Open(
    "../PlotFiles/ttbar_77p_MC16d_90.-140.-70.-100.-30000.-30000.-200000-200000.-1.0-1.0-2.5-250000..root", "READ")
d3 = file2e.GetDirectory(
    "Nominal").GetDirectory(HistoName)
h3 = dir2e.Get(
    "sig_Hplus_Wh_m800-0_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")

f1 = TFile.Open(
    "../PlotFiles/sig_Hplus_Wh_m800-0_77p_MC16d_90.-140.-70.-100.-30000.-30000.-200000-200000.-1.0-1.0-2.5-250000..root", "READ")
d1 = file2e.GetDirectory(
    "Nominal").GetDirectory(HistoName)
h1 = dir2e.Get(
    "sig_Hplus_Wh_m800-0_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")

h2 = h_sig_Hplus_m800.Clone()
# c = h1.GetNbinsX()
# d = h2.GetNbinsX()
# e = h3.GetNbinsX()
# print d
# print c
# print e
sigList = []
for i in range(h1.GetNbinsX()):
    b = h1.GetBinContent(i)
    c = h3.GetBinContent(i)

    print b
    print c

    if b and c != 0.0:
        x = 2 * ((b+c) * math.log(1+(b/c)) - b)
        print x
        sigList.append(x)
    print "\n"
print sigList
sig = math.sqrt(sum(sigList))
print sig
