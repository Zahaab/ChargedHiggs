import sys
import os
import glob
import math
import re
from ROOT import *
from array import *
from configparser import configParser, getConfigData, getPlotFiles, getaxisLabels
from CutFlowMethods import prepareCutHolder, cutFlowExtraction, cutFlowPercentExtraction, sumPercent, cutFlowInsertion

_, config_path = sys.argv

config = configParser(config_path)
MCDataPeriodes = getConfigData(config, "Stack_")
histoNames = getConfigData(config, "Graph_")
btagStrategies = getConfigData(config, "Btag_")
dataPeriodeStack = "-".join(MCDataPeriodes)
histoFiles = {i: getPlotFiles(config, i) for i in MCDataPeriodes}
plotEvents = getConfigData(config, "Plot_")
Regions = getConfigData(config, "Region_")

# outputdir = str("../Plots/" + config["WP"] + "/" + "StackPlots" + "/" + dataPeriodeStack + "-" + config["Higgs_mass_lower_bound"] + "-" + config["Higgs_mass_upper_bound"] + "-" +
#                 config["Wboson_mass_lower_bound"] + "-" + config["Wboson_mass_upper_bound"] + "-" + config["Missing_transverse_momentum"] + "-" +
#                 config["Lepton_transverse_momentum"] + "-" + config["2Jets_Jet1_transverse_momentum"] + "-" +
#                 config["2Jets_Jet2_transverse_momentum"] + "-" + config["2Jets_Jet1_lepton_angle"] + "-" + config["2Jets_Jet2_lepton_angle"] + "-" +
#                 config["Higgs_Wboson_angle"] + "-" + config["1Jet_Jet_transverse_momentum"])

# try:
#     os.mkdir(outputdir)
# except OSError:
#     print "Creation of the directory %s failed" % outputdir
# else:
#     print "Successfully created the directory %s " % outputdir


def sumHistosList(histo_list):
    resultHisto = 0
    if len(histo_list) > 0:
        for i in histo_list:
            if resultHisto == 0:
                resultHisto = i
            else:
                resultHisto += i
    return resultHisto


ReBin = False
YAxisScale = 1.4
dscale = 1.223695
escale = 1.61419497

HistoName = "mH"
Region = "Merged_LepP_SR"
btagStrategy = "TwoTags"

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
    if ReBin == True:
        h_sig_Hplus_m400.Rebin(2)
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
    if ReBin == True:
        h_sig_Hplus_m800.Rebin(2)
if config["Plot_sig_Hplus_Wh_m1600-0"] == "Enable":
    h_sig_Hplus_m1600list = []
    if config["Stack_MC16a"] == "Enable":
        file3a = TFile.Open("../PlotFiles/" +
                            histoFiles["MC16a"]["sig_Hplus_Wh_m1600-0"], "READ")
        dir3a = file3a.GetDirectory(
            "Nominal").GetDirectory(HistoName)
        h_sig_Hplus_m1600a = dir3a.Get(
            "sig_Hplus_Wh_m1600-0_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
        h_sig_Hplus_m1600list.append(h_sig_Hplus_m1600a)
    if config["Stack_MC16d"] == "Enable":
        file3d = TFile.Open("../PlotFiles/" +
                            histoFiles["MC16d"]["sig_Hplus_Wh_m1600-0"], "READ")
        dir3d = file3d.GetDirectory(
            "Nominal").GetDirectory(HistoName)
        h_sig_Hplus_m1600d = dir3d.Get(
            "sig_Hplus_Wh_m1600-0_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
        h_sig_Hplus_m1600d.Scale(dscale)
        h_sig_Hplus_m1600list.append(h_sig_Hplus_m1600d)
    if config["Stack_MC16e"] == "Enable":
        file3e = TFile.Open("../PlotFiles/" +
                            histoFiles["MC16e"]["sig_Hplus_Wh_m1600-0"], "READ")
        dir3e = file3e.GetDirectory(
            "Nominal").GetDirectory(HistoName)
        h_sig_Hplus_m1600e = dir3e.Get(
            "sig_Hplus_Wh_m1600-0_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
        h_sig_Hplus_m1600e.Scale(escale)
        h_sig_Hplus_m1600list.append(h_sig_Hplus_m1600e)

    h_sig_Hplus_m1600 = sumHistosList(h_sig_Hplus_m1600list)
    h_sig_Hplus_m1600.SetLineColor(kViolet)
    h_sig_Hplus_m1600.SetLineStyle(7)
    if ReBin == True:
        h_sig_Hplus_m1600.Rebin(2)

# INTEGRTATING PRACTICE

print "\n"
print "This is the number of bins"

bins400 = h_sig_Hplus_m400.GetNbinsX()
bins800 = h_sig_Hplus_m800.GetNbinsX()
bins1600 = h_sig_Hplus_m1600.GetNbinsX()

print bins400
print bins800
print bins1600

print "\n"
print "This is the integrals"

# a = h.Integral(h.FindFixBin(0), h.FindFixBin(b), "")
int400 = h_sig_Hplus_m400.Integral(-1, bins400+1, "")
int800 = h_sig_Hplus_m800.Integral(-1, bins800+1, "")
int1600 = h_sig_Hplus_m1600.Integral(-1, bins1600+1, "")

print int800
print int400
print int1600
