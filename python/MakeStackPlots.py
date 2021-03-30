# -*- coding: utf-8 -*-
# python
import sys
import os
import glob
import math
import re
from ROOT import *
from array import *
from configparser import configParser, getConfigData, getPlotFiles, getaxisLabels
from CutFlowMethods import prepareCutHolder, prepareCutContent, sortCutContent, cutFlowExtraction, cutFlowPercentExtraction, sumPercent, cutFlowInsertion, addCutFlows

_, config_path = sys.argv

config = configParser(config_path)
# This is the output of the c++, thus input of python
input_dir = config["OUTPUTDIR"]
MCDataPeriodes = getConfigData(config, "Stack_")
histoNames = getConfigData(config, "Graph_")
btagStrategies = getConfigData(config, "Btag_")
histoFiles = {i: getPlotFiles(config, i) for i in MCDataPeriodes}
plotEvents = getConfigData(config, "Plot_")
Regions = getConfigData(config, "Region_")

if len(MCDataPeriodes) < 2:
    dataPeriodeStack = str(MCDataPeriodes[0])
else:
    dataPeriodeStack = "-".join(MCDataPeriodes)

for data_set in plotEvents:
    for dataPeriode in MCDataPeriodes:
        histoFiles[dataPeriode][data_set] = [input_dir + "/" +
                                             "PlotFiles/" + histoFiles[dataPeriode][data_set].replace(".root", "_0.root")]
        fileExtention = 1
        extraHisto = histoFiles[dataPeriode][data_set][0].replace(
            "_0.root", "_" + str(fileExtention) + ".root")
        plotDataExists = os.path.exists(extraHisto)
        while plotDataExists == True:
            histoFiles[dataPeriode][data_set].append(extraHisto)
            fileExtention += 1
            extraHisto = histoFiles[dataPeriode][data_set][0].replace(
                "_0.root", "_" + str(fileExtention) + ".root")
            plotDataExists = os.path.exists(extraHisto)


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

# THIS IS WHERE THE ACCEPTANCE IS HANDELED

cutParameters = ["TotalEvents", "Hadronic_rejected", "Leptonic_rejected", "jjbb_OR_lvbb_rejected", "Higgs_momentum",
                 "Higgs_Lepton_Angle", "Wboson_Lepton_Angle", "Higgs_Wboson_Angle", "PositiveLep_Wboson_bool",
                 "PositiveLep_Higgs_momentum", "Higgs_Mass", "Wplus_Mass"]

realCutParameters = ["real"+i for i in cutParameters]

altcutParameters = []

altrealCutParameters = ["real"+i for i in altcutParameters]

if config["CSV_FlatCutFlow"] == "Enable":
    cutFlowFile = open(outputdir + "/cutflow.txt", 'w')
    cutFlowFile.truncate(0)  # to ensure the file is empty
    cutFlowFile.write("Data-Set,"+"Data_Period," + "Number_of_Tags," + "Channel," +
                      ",".join(cutParameters) + "," + "Total" + "\n")

if config["CSV_RealCutFlow"] == "Enable":
    realCutFlowFile = open(outputdir + "/realcutflow.txt", 'w')
    realCutFlowFile.truncate(0)
    realCutFlowFile.write("Data-Set,"+"Data_Period," + "Number_of_Tags," + "Channel," +
                          ",".join(realCutParameters) + "," + "Total" + "\n")

if config["CSV_FlatCutFlowPercent"] == "Enable":
    cutFlowFilePercent = open(outputdir + "/cutflowPercent.txt", 'w')
    cutFlowFilePercent.truncate(0)
    cutFlowFilePercent.write("Data-Set,"+"Data_Period," + "Number_of_Tags," + "Channel," +
                             ",".join(cutParameters) + "," + "Total" + "\n")

if config["CSV_RealCutFlowPercent"] == "Enable":
    realCutFlowFilePercent = open(outputdir + "/realcutflowPercent.txt", 'w')
    realCutFlowFilePercent.truncate(0)
    realCutFlowFilePercent.write("Data-Set,"+"Data_Period," + "Number_of_Tags," + "Channel," +
                                 ",".join(realCutParameters) + "," + "Total" + "\n")

# vvvvv THIS IS FOR THE ALTERNATE CUT FLOW vvvvvv
if config["CSV_AlternateCutFlow"] == "Enable":
    if config["CSV_FlatCutFlow"] == "Enable":
        altcutFlowFile = open(outputdir + "/altcutflow.txt", 'w')
        altcutFlowFile.truncate(0)  # to ensure the file is empty
        altcutFlowFile.write("Data-Set,"+"Data_Period," + "Number_of_Tags," + "Channel," +
                             ",".join(altcutParameters) + "," + "Total" + "\n")

    if config["CSV_RealCutFlow"] == "Enable":
        altrealCutFlowFile = open(outputdir + "/altrealcutflow.txt", 'w')
        altrealCutFlowFile.truncate(0)
        altrealCutFlowFile.write("Data-Set,"+"Data_Period," + "Number_of_Tags," + "Channel," +
                                 ",".join(altrealCutParameters) + "," + "Total" + "\n")

    if config["CSV_FlatCutFlowPercent"] == "Enable":
        altcutFlowFilePercent = open(outputdir + "/altcutflowpercent.txt", 'w')
        altcutFlowFilePercent.truncate(0)
        altcutFlowFilePercent.write("Data-Set,"+"Data_Period," + "Number_of_Tags," + "Channel," +
                                    ",".join(altcutParameters) + "," + "Total" + "\n")

    if config["CSV_RealCutFlowPercent"] == "Enable":
        altrealCutFlowFilePercent = open(
            outputdir + "/altrealcutflowpercent.txt", 'w')
        altrealCutFlowFilePercent.truncate(0)
        altrealCutFlowFilePercent.write("Data-Set,"+"Data_Period," + "Number_of_Tags," + "Channel," +
                                        ",".join(altrealCutParameters) + "," + "Total" + "\n")

# ^^^^^^ THIS IS FOR THE ALTERNATE CUT FLOW ^^^^^
if config["CSV_FlatCutFlow"] == "Enable" or config["CSV_RealCutFlow"] == "Enable" or config["CSV_FlatCutFlowPercent"] == "Enable" or config["CSV_RealCutFlowPercent"] == "Enable":
    for data_set in plotEvents:  # Grabs the data sets
        if config["CSV_FlatCutFlow"] == "Enable":
            cutFlowHold = {}
            cutFlowHold = prepareCutHolder(
                cutFlowHold, cutParameters, btagStrategies)
        if config["CSV_RealCutFlow"] == "Enable":
            realCutFlowHold = {}
            realCutFlowHold = prepareCutHolder(
                realCutFlowHold, realCutParameters, btagStrategies)
        if config["CSV_FlatCutFlowPercent"] == "Enable":
            cutFlowHoldPercent = {}
            cutFlowHoldPercent = prepareCutHolder(
                cutFlowHoldPercent, cutParameters, btagStrategies)
        if config["CSV_RealCutFlowPercent"] == "Enable":
            realCutFlowHoldPercent = {}
            realCutFlowHoldPercent = prepareCutHolder(
                realCutFlowHoldPercent, realCutParameters, btagStrategies)

        if config["CSV_AlternateCutFlow"] == "Enable":
            if config["CSV_FlatCutFlow"] == "Enable":
                altcutFlowHold = {}
                altcutFlowHold = prepareCutHolder(
                    altcutFlowHold, altcutParameters, btagStrategies)
            if config["CSV_RealCutFlow"] == "Enable":
                altrealCutFlowHold = {}
                altrealCutFlowHold = prepareCutHolder(
                    altrealCutFlowHold, altrealCutParameters, btagStrategies)
            if config["CSV_FlatCutFlowPercent"] == "Enable":
                altcutFlowHoldPercent = {}
                altcutFlowHoldPercent = prepareCutHolder(
                    altcutFlowHoldPercent, altcutParameters, btagStrategies)
            if config["CSV_RealCutFlowPercent"] == "Enable":
                altrealCutFlowHoldPercent = {}
                altrealCutFlowHoldPercent = prepareCutHolder(
                    altrealCutFlowHoldPercent, altrealCutParameters, btagStrategies)

        for dataPeriod in MCDataPeriodes:
            cutFlow_content, cutFlow_content_t = prepareCutContent(
                cutParameters)
            realCutFlow_content, realCutFlow_content_t = prepareCutContent(
                realCutParameters)
            altcutFlow_content, altcutFlow_content_t = prepareCutContent(
                altcutParameters)
            altrealCutFlow_content, altrealCutFlow_content_t = prepareCutContent(
                altrealCutParameters)

            cutFlowPath = histoFiles[dataPeriod][data_set][0].replace(
                "_0.root", "-cutFlow.txt")
            rawCutFlow = open(cutFlowPath, "r")
            rawCutFlow_content = rawCutFlow.read().split("\n")
            realCutFlow_content, cutFlow_content = sortCutContent(
                rawCutFlow_content, realCutFlow_content, cutFlow_content)
            rawCutFlow.close()

            if len(histoFiles[dataPeriod][data_set]) > 1:
                for cutFlowPath in histoFiles[dataPeriod][data_set]:
                    if cutFlowPath == histoFiles[dataPeriod][data_set][0]:
                        continue
                    rawCutFlow = open(cutFlowPath.replace(
                        ".root", "-cutFlow.txt"), "r")
                    rawCutFlow_content = rawCutFlow.read().split("\n")
                    realCutFlow_content_t, cutFlow_content_t = sortCutContent(
                        rawCutFlow_content, realCutFlow_content_t, cutFlow_content_t)
                    if config["CSV_FlatCutFlow"] == "Enable":
                        cutFlow_content = addCutFlows(
                            cutFlow_content, cutFlow_content_t)
                    if config["CSV_RealCutFlow"] == "Enable":
                        realCutFlow_content = addCutFlows(
                            realCutFlow_content, realCutFlow_content_t)
                    rawCutFlow.close()

            if config["CSV_AlternateCutFlow"] == "Enable":
                altcutFlowPath = histoFiles[dataPeriod][data_set][0].replace(
                    "_0.root", "-cutFlowAlt.txt")
                altrawCutFlow = open(altcutFlowPath, "r")
                altrawCutFlow_content = altrawCutFlow.read().split("\n")
                altrealCutFlow_content, altcutFlow_content = sortCutContent(
                    rawCutFlow_content, altrealCutFlow_content, altcutFlow_content)
                altrawCutFlow.close()
                if len(histoFiles[dataPeriod][data_set]) > 1:
                    for cutFlowPath in histoFiles[dataPeriod][data_set]:
                        if cutFlowPath == histoFiles[dataPeriod][data_set][0]:
                            continue
                        altcutFlowPath = cutFlowPath.replace(
                            ".root", "-cutFlowAlt.txt")
                        altrawCutFlow = open(altcutFlowPath, "r")
                        altrawCutFlow_content = altrawCutFlow.read().split("\n")
                        altrealCutFlow_content_t, altcutFlow_content_t = sortCutContent(
                            altrawCutFlow_content, altrealCutFlow_content_t, altcutFlow_content_t)
                        if config["CSV_FlatCutFlow"] == "Enable":
                            altcutFlow_content = addCutFlows(
                                altcutFlow_content, altcutFlow_content_t)
                        if config["CSV_RealCutFlow"] == "Enable":
                            altrealCutFlow_content = addCutFlows(
                                altrealCutFlow_content, altrealCutFlow_content_t)
                        altrawCutFlow.close()

            if config["CSV_FlatCutFlow"] == "Enable":
                cutFlowExtraction(cutFlow_content, cutParameters,
                                  btagStrategies, cutFlowHold)
            if config["CSV_RealCutFlow"] == "Enable":
                cutFlowExtraction(realCutFlow_content,
                                  realCutParameters, btagStrategies, realCutFlowHold)
            if config["CSV_FlatCutFlowPercent"] == "Enable":
                cutFlowPercentExtraction(
                    cutFlow_content, cutParameters, btagStrategies, cutFlowHoldPercent)
            if config["CSV_RealCutFlowPercent"] == "Enable":
                cutFlowPercentExtraction(realCutFlow_content,
                                         realCutParameters, btagStrategies, realCutFlowHoldPercent)

            if config["CSV_AlternateCutFlow"] == "Enable":
                if config["CSV_FlatCutFlow"] == "Enable":
                    cutFlowExtraction(altcutFlow_content,
                                      altcutParameters, btagStrategies, altcutFlowHold)
                if config["CSV_RealCutFlow"] == "Enable":
                    cutFlowExtraction(altrealCutFlow_content,
                                      altrealCutParameters, btagStrategies, altrealCutFlowHold)
                if config["CSV_FlatCutFlowPercent"] == "Enable":
                    cutFlowPercentExtraction(
                        altcutFlow_content, altcutParameters, btagStrategies, altcutFlowHoldPercent)
                if config["CSV_RealCutFlowPercent"] == "Enable":
                    cutFlowPercentExtraction(altrealCutFlow_content,
                                             altrealCutParameters, btagStrategies, altrealCutFlowHoldPercent)

        if config["CSV_FlatCutFlow"] == "Enable":
            cutFlowInsertion(cutFlowFile, data_set, MCDataPeriodes,
                             btagStrategies, cutParameters, cutFlowHold)
        if config["CSV_RealCutFlow"] == "Enable":
            cutFlowInsertion(realCutFlowFile, data_set, MCDataPeriodes,
                             btagStrategies, realCutParameters, realCutFlowHold)
        if config["CSV_FlatCutFlowPercent"] == "Enable":
            cutFlowInsertion(cutFlowFilePercent, data_set, MCDataPeriodes,
                             btagStrategies, cutParameters, cutFlowHoldPercent, "enable")
        if config["CSV_RealCutFlowPercent"] == "Enable":
            cutFlowInsertion(realCutFlowFilePercent, data_set, MCDataPeriodes,
                             btagStrategies, realCutParameters, realCutFlowHoldPercent, "enable")
        if config["CSV_AlternateCutFlow"] == "Enable":
            if config["CSV_FlatCutFlow"] == "Enable":
                cutFlowInsertion(altcutFlowFile, data_set, MCDataPeriodes,
                                 btagStrategies, altcutParameters, altcutFlowHold)
            if config["CSV_RealCutFlow"] == "Enable":
                cutFlowInsertion(altrealCutFlowFile, data_set, MCDataPeriodes,
                                 btagStrategies, altrealCutParameters, altrealCutFlowHold)
            if config["CSV_FlatCutFlowPercent"] == "Enable":
                cutFlowInsertion(altcutFlowFilePercent, data_set, MCDataPeriodes,
                                 btagStrategies, altcutParameters, altcutFlowHoldPercent, "enable")
            if config["CSV_RealCutFlowPercent"] == "Enable":
                cutFlowInsertion(altrealCutFlowFilePercent, data_set, MCDataPeriodes,
                                 btagStrategies, altrealCutParameters, altrealCutFlowHoldPercent, "enable")

    if config["CSV_FlatCutFlow"] == "Enable":
        cutFlowFile.close()
    if config["CSV_RealCutFlow"] == "Enable":
        realCutFlowFile.close()
    if config["CSV_FlatCutFlowPercent"] == "Enable":
        cutFlowFilePercent.close()
    if config["CSV_RealCutFlowPercent"] == "Enable":
        realCutFlowFilePercent.close()

    if config["CSV_AlternateCutFlow"] == "Enable":
        if config["CSV_FlatCutFlow"] == "Enable":
            altcutFlowFile.close()
        if config["CSV_RealCutFlow"] == "Enable":
            altrealCutFlowFile.close()
        if config["CSV_FlatCutFlowPercent"] == "Enable":
            altcutFlowFilePercent.close()
        if config["CSV_RealCutFlowPercent"] == "Enable":
            altrealCutFlowFilePercent.close()

# THIS IS WHERE THE ACCEPTANCE IS HANDELED

# THIS IS FOR SIGNIFICANCE WHICH IS CALCULATED DURING GRAPHING

signalMasses = []
for btagStrategy in btagStrategies:
    if config["Plot_sig_Hplus_Wh_m400-0"] == "Enable":
        signalMasses.append("400GeV_Signal" + btagStrategy)
    if config["Plot_sig_Hplus_Wh_m800-0"] == "Enable":
        signalMasses.append("800GeV_Signal" + btagStrategy)
    if config["Plot_sig_Hplus_Wh_m1600-0"] == "Enable":
        signalMasses.append("1600GeV_Signal" + btagStrategy)

significanceFile = open(outputdir + "/significance.txt", 'w')
significanceFile.truncate(0)  # to ensure the file is empty
significanceFile.write(
    "HisogramName," + "Region" + ",".join(signalMasses) + "\n")


def calcSignificance(signalHisto, backgroundHisto):
    h1 = signalHisto.Clone()
    h2 = backgroundHisto.Clone()
    sigList = []
    for i in range(h1.GetNbinsX()):
        signal = h1.GetBinContent(i)
        background = h2.GetBinContent(i)
        if signal < 0 or background < 0:
            continue
        if signal and background != 0.0:
            x = 2 * ((signal+background) *
                     math.log(1+(signal/background)) - signal)
            sigList.append(x)
    if sigList == []:
        return 0
    significance = math.sqrt(sum(sigList))
    return significance

# NOW WE GRAPH THE FIGURES


gROOT.SetBatch(True)
gStyle.SetOptStat(0)
gStyle.SetPalette(1)
gROOT.LoadMacro("../style/AtlasStyle.C")
gROOT.LoadMacro("../style/AtlasUtils.C")
SetAtlasStyle()
gStyle.SetEndErrorSize(6)
# gStyle.SetErrorX(1.)

y_axis_label = "Event fraction"
c_blue = TColor.GetColor("#3366ff")
c_red = TColor.GetColor("#ee3311")
c_orange = TColor.GetColor("#ff9900")


def sumHistosList(histo_list):
    resultHisto = 0
    print
    if len(histo_list) > 0:
        for i in histo_list:
            if resultHisto == 0:
                resultHisto = i
            else:
                resultHisto.Add(i, 1.0)
    return resultHisto


def getHistos(data_set, histo_list, histoName, region, btagStrategy, histoFiles):
    if config["Stack_MC16a"] == "Enable":
        MC16aHisto = TH1F()
        for histo in histoFiles["MC16a"][data_set]:
            filea = TFile.Open(
                histo, "READ")
            dira = filea.GetDirectory(
                "Nominal").GetDirectory(histoName)
            histoa = dira.Get(
                data_set+"_"+histoName+"_"+region+"_"+btagStrategy+"_Nominal")
            MC16aHisto.Add(histoa, 1.0)
        histo_list.append(MC16aHisto)
    if config["Stack_MC16d"] == "Enable":
        MC16dHisto = TH1F()
        for histo in histoFiles["MC16d"][data_set]:

            filed = TFile.Open(
                histo, "READ")
            dird = filed.GetDirectory(
                "Nominal").GetDirectory(histoName)
            histod = dird.Get(
                data_set+"_"+histoName+"_"+region+"_"+btagStrategy+"_Nominal")
            MC16dHisto.Add(histod, 1.0)
        MC16dHisto.Scale(dscale)
        histo_list.append(MC16dHisto)
    if config["Stack_MC16e"] == "Enable":
        MC16eHisto = TH1F()
        for histo in histoFiles["MC16d"][data_set]:
            filee = TFile.Open(
                histo, "READ")
            dire = filee.GetDirectory(
                "Nominal").GetDirectory(histoName)
            histoe = dire.Get(
                data_set+"_"+histoName+"_"+region+"_"+btagStrategy+"_Nominal")
            MC16eHisto.Add(histoe, 1.0)
        MC16eHisto.Scale(escale)
        histo_list.append(MC16eHisto)
    return histo_list


c1 = TCanvas("ShapePlots", "", 720, 720)


for HistoName in histoNames:
    histoDir = outputdir + "/" + HistoName
    try:
        os.mkdir(histoDir)
    except OSError:
        pass
    Xaxis_label, legend_place, text_place = getaxisLabels(HistoName)
    leg_pl1, leg_pl2, leg_pl3, leg_pl4 = legend_place
    test_pl1, test_pl2 = text_place

    for Region in Regions:
        significanceValues = []
        for btagStrategy in btagStrategies:
            ReBin = False
            if config["Rebin"] == "Enable":
                ReBin = True
            else:
                ReBin = False
            YAxisScale = 1.4
            dscale = 1.223695
            escale = 1.61419497
            h_other_background_list = []
            h_ttbar_background = []
            if config["Plot_sig_Hplus_Wh_m400-0"] == "Enable":
                h_sig_Hplus_m400list = []
                h_sig_Hplus_m400list = getHistos(
                    "sig_Hplus_Wh_m400-0", h_sig_Hplus_m400list, HistoName, Region, btagStrategy, histoFiles)

                h_sig_Hplus_m400 = sumHistosList(h_sig_Hplus_m400list)
                h_sig_Hplus_m400.SetLineColor(kBlack)
                h_sig_Hplus_m400.SetLineStyle(1)
                h_sig_Hplus_m400.SetMarkerStyle(1)
                if ReBin == True:
                    h_sig_Hplus_m400.Rebin(2)
            if config["Plot_sig_Hplus_Wh_m800-0"] == "Enable":
                h_sig_Hplus_m800list = []
                h_sig_Hplus_m800list = getHistos(
                    "sig_Hplus_Wh_m800-0", h_sig_Hplus_m800list, HistoName, Region, btagStrategy, histoFiles)

                h_sig_Hplus_m800 = sumHistosList(h_sig_Hplus_m800list)
                h_sig_Hplus_m800.SetLineColor(kBlue)
                h_sig_Hplus_m800.SetLineStyle(1)
                h_sig_Hplus_m800.SetMarkerStyle(1)
                if ReBin == True:
                    h_sig_Hplus_m800.Rebin(2)
            if config["Plot_sig_Hplus_Wh_m1600-0"] == "Enable":
                h_sig_Hplus_m1600list = []
                h_sig_Hplus_m1600list = getHistos(
                    "sig_Hplus_Wh_m1600-0", h_sig_Hplus_m1600list, HistoName, Region, btagStrategy, histoFiles)

                h_sig_Hplus_m1600 = sumHistosList(h_sig_Hplus_m1600list)
                h_sig_Hplus_m1600.SetLineColor(kViolet)
                h_sig_Hplus_m1600.SetLineStyle(1)
                h_sig_Hplus_m1600.SetMarkerStyle(1)
                if ReBin == True:
                    h_sig_Hplus_m1600.Rebin(2)

            if config["Plot_ttbar"] == "Enable":
                h_ttbar_background_list = []
                h_ttbar_background_list = getHistos(
                    "ttbar", h_ttbar_background_list, HistoName, Region, btagStrategy, histoFiles)

                h_ttbar_background = sumHistosList(h_ttbar_background_list)
                h_ttbar_background.SetLineColor(8)
                if ReBin == True:
                    h_ttbar_background.Rebin(2)

            elif config["Plot_ttbarSherpa"] == "Enable":
                h_ttbarSherpa_background_list = []
                h_ttbarSherpa_background_list = getHistos(
                    "ttbarSherpa", h_ttbarSherpa_background_list, HistoName, Region, btagStrategy, histoFiles)

                h_ttbar_background = sumHistosList(
                    h_ttbarSherpa_background_list)
                h_ttbar_background.SetLineColor(8)
                if ReBin == True:
                    h_ttbar_background.Rebin(2)

            if config["Plot_Wjets"] == "Enable":
                h_Wjets_background_list = []
                h_Wjets_background_list = getHistos(
                    "Wjets", h_Wjets_background_list, HistoName, Region, btagStrategy, histoFiles)

                h_Wjets_background = sumHistosList(h_Wjets_background_list)
                h_Wjets_background.SetLineColor(kRed-3)
                if ReBin == True:
                    h_Wjets_background.Rebin(2)
                h_other_background_list.append(h_Wjets_background)

            if config["Plot_Zjets"] == "Enable":
                h_Zjets_background_list = []
                h_Zjets_background_list = getHistos(
                    "Zjets", h_Zjets_background_list, HistoName, Region, btagStrategy, histoFiles)

                h_Zjets_background = sumHistosList(h_Zjets_background_list)
                h_Zjets_background.SetLineColor(kRed-3)
                if ReBin == True:
                    h_Zjets_background.Rebin(2)
                h_other_background_list.append(h_Zjets_background)

            if config["Plot_diboson"] == "Enable":
                h_diboson_background_list = []
                h_diboson_background_list = getHistos(
                    "diboson", h_diboson_background_list, HistoName, Region, btagStrategy, histoFiles)

                h_diboson_background = sumHistosList(h_diboson_background_list)
                h_diboson_background.SetLineColor(kRed-3)
                if ReBin == True:
                    h_diboson_background.Rebin(2)
                h_other_background_list.append(h_diboson_background)

            if config["Plot_singleTop"] == "Enable":
                h_singleTop_background_list = []
                h_singleTop_background_list = getHistos(
                    "singleTop", h_singleTop_background_list, HistoName, Region, btagStrategy, histoFiles)

                h_singleTop_background = sumHistosList(
                    h_singleTop_background_list)
                h_singleTop_background.SetLineColor(kRed-3)
                if ReBin == True:
                    h_singleTop_background.Rebin(2)
                h_other_background_list.append(h_singleTop_background)

            h_other_background = sumHistosList(h_other_background_list)

            if h_other_background_list == []:
                if config["Plot_ttbar"] == "Enable" or config["Plot_ttbarSherpa"] == "Enable":
                    h_all_background = h_ttbar_background
                else:
                    h_all_background = 0
            else:
                h_all_background = h_ttbar_background + h_other_background

            # THIS IS WHERE THE SIGNIFICANCE IS HANDELED

            if h_all_background != 0:
                if config["Plot_sig_Hplus_Wh_m400-0"] == "Enable":
                    significanceValues.append(str(calcSignificance(
                        h_sig_Hplus_m400, h_all_background)))
                else:
                    significanceValues.append("NaN")
                if config["Plot_sig_Hplus_Wh_m800-0"] == "Enable":
                    significanceValues.append(str(calcSignificance(
                        h_sig_Hplus_m800, h_all_background)))
                else:
                    significanceValues.append("NaN")
                if config["Plot_sig_Hplus_Wh_m1600-0"] == "Enable":
                    significanceValues.append(str(calcSignificance(
                        h_sig_Hplus_m1600, h_all_background)))
                else:
                    significanceValues.append("NaN")

            # THIS IS WHERE THE SIGNIFICANCE IS HANDELED

            # BACK TO GRAPHING

            if h_all_background == 0:
                if config["Plot_sig_Hplus_Wh_m400-0"] == "Enable":
                    h_sig_Hplus_m400.Scale(5)
                    h_sig_Hplus_m400n = h_sig_Hplus_m400
                if config["Plot_sig_Hplus_Wh_m800-0"] == "Enable":
                    h_sig_Hplus_m800.Scale(5)
                    h_sig_Hplus_m800n = h_sig_Hplus_m800
                if config["Plot_sig_Hplus_Wh_m1600-0"] == "Enable":
                    h_sig_Hplus_m1600.Scale(5)
                    h_sig_Hplus_m1600n = h_sig_Hplus_m1600
            else:
                if config["Plot_sig_Hplus_Wh_m400-0"] == "Enable":
                    h_sig_Hplus_m400.Scale(5)
                    h_sig_Hplus_m400n = h_sig_Hplus_m400+h_all_background
                if config["Plot_sig_Hplus_Wh_m800-0"] == "Enable":
                    h_sig_Hplus_m800.Scale(5)
                    h_sig_Hplus_m800n = h_sig_Hplus_m800+h_all_background
                if config["Plot_sig_Hplus_Wh_m1600-0"] == "Enable":
                    h_sig_Hplus_m1600.Scale(5)
                    h_sig_Hplus_m1600n = h_sig_Hplus_m1600+h_all_background

            if h_all_background != 0:
                h_all_background.SetLineColor(1)
                h_all_background.SetFillColor(8)
                h_all_background.SetLineStyle(1)
                h_all_background.SetMarkerStyle(1)
            if h_other_background_list != []:
                h_other_background.SetLineColor(1)
                h_other_background.SetFillColor(kRed-3)
                h_other_background.SetLineStyle(1)
                h_other_background.SetMarkerStyle(1)

            ymax = 0

            if h_all_background != 0:
                if ymax < h_all_background.GetMaximum():
                    ymax = h_all_background.GetMaximum()

            if config["Plot_sig_Hplus_Wh_m400-0"] == "Enable":
                if ymax < h_sig_Hplus_m400n.GetMaximum():
                    ymax = h_sig_Hplus_m400n.GetMaximum()

            if config["Plot_sig_Hplus_Wh_m800-0"] == "Enable":
                if ymax < h_sig_Hplus_m800n.GetMaximum():
                    ymax = h_sig_Hplus_m800n.GetMaximum()

            if config["Plot_sig_Hplus_Wh_m1600-0"] == "Enable":
                if ymax < h_sig_Hplus_m1600n.GetMaximum():
                    ymax = h_sig_Hplus_m1600n.GetMaximum()

            if h_all_background != 0:
                h_all_background.SetNdivisions(8)
                h_all_background.SetXTitle(Xaxis_label)
                h_all_background.GetYaxis().SetRangeUser(0.001, ymax*1.3)
                h_all_background.GetXaxis().SetRangeUser(0.001, 2400)
                h_all_background.Draw("HIST")
                if h_other_background_list != []:
                    h_other_background.Draw("HISTSAME")
                if config["Plot_sig_Hplus_Wh_m400-0"] == "Enable":
                    h_sig_Hplus_m400n.Draw("E1 HISTSAME")
                if config["Plot_sig_Hplus_Wh_m800-0"] == "Enable":
                    h_sig_Hplus_m800n.Draw("E1 HISTSAME")
                if config["Plot_sig_Hplus_Wh_m1600-0"] == "Enable":
                    h_sig_Hplus_m1600n.Draw("E1 HISTSAME")
            elif h_other_background_list != []:
                h_other_background.SetNdivisions(8)
                h_other_background.SetXTitle(Xaxis_label)
                h_other_background.GetYaxis().SetRangeUser(0.001, ymax*1.3)
                h_other_background.GetXaxis().SetRangeUser(0.001, 2400)
                h_other_background.Draw("HIST")
                if config["Plot_sig_Hplus_Wh_m400-0"] == "Enable":
                    h_sig_Hplus_m400n.Draw("E1 HISTSAME")
                if config["Plot_sig_Hplus_Wh_m800-0"] == "Enable":
                    h_sig_Hplus_m800n.Draw("E1 HISTSAME")
                if config["Plot_sig_Hplus_Wh_m1600-0"] == "Enable":
                    h_sig_Hplus_m1600n.Draw("E1 HISTSAME")
            elif config["Plot_sig_Hplus_Wh_m400-0"] == "Enable":
                h_sig_Hplus_m400n.SetNdivisions(8)
                h_sig_Hplus_m400n.SetXTitle(Xaxis_label)
                h_sig_Hplus_m400n.GetYaxis().SetRangeUser(0.001, ymax*1.3)
                h_sig_Hplus_m400n.GetXaxis().SetRangeUser(0.001, 2400)
                h_sig_Hplus_m400n.Draw("E1 HIST")
                if config["Plot_sig_Hplus_Wh_m800-0"] == "Enable":
                    h_sig_Hplus_m800n.Draw("E1 HISTSAME")
                if config["Plot_sig_Hplus_Wh_m1600-0"] == "Enable":
                    h_sig_Hplus_m1600n.Draw("E1 HISTSAME")
            elif config["Plot_sig_Hplus_Wh_m800-0"] == "Enable":
                h_sig_Hplus_m800n.SetNdivisions(8)
                h_sig_Hplus_m800n.SetXTitle(Xaxis_label)
                h_sig_Hplus_m800n.GetYaxis().SetRangeUser(0.001, ymax*1.3)
                h_sig_Hplus_m800n.GetXaxis().SetRangeUser(0.001, 2400)
                h_sig_Hplus_m800n.Draw("E1 HIST")
                if config["Plot_sig_Hplus_Wh_m1600-0"] == "Enable":
                    h_sig_Hplus_m1600n.Draw("E1 HISTSAME")
            elif config["Plot_sig_Hplus_Wh_m1600-0"] == "Enable":
                h_sig_Hplus_m1600n.SetNdivisions(8)
                h_sig_Hplus_m1600n.SetXTitle(Xaxis_label)
                h_sig_Hplus_m1600n.GetYaxis().SetRangeUser(0.001, ymax*1.3)
                h_sig_Hplus_m1600n.GetXaxis().SetRangeUser(0.001, 2400)
                h_sig_Hplus_m1600n.Draw("E1 HIST")

            leg = TLegend(leg_pl1, leg_pl2, leg_pl3, leg_pl4)
            atlas_lable = ATLAS_LABEL(0.19, 0.95)
            myText(test_pl1, test_pl2, 1, HistoName+" "+btagStrategy)
            leg.SetShadowColor(kWhite)
            leg.SetMargin(0.15)
            leg.SetTextSize(0.017)
            leg.SetFillColor(kWhite)
            leg.SetLineColor(kBlack)

            if config["Plot_sig_Hplus_Wh_m400-0"] == "Enable":
                leg.AddEntry(h_sig_Hplus_m400,
                             "H^{+}#rightarrow hW^{+} (m_{H^{+}}=400GeV) x5", "L")
            if config["Plot_sig_Hplus_Wh_m800-0"] == "Enable":
                leg.AddEntry(h_sig_Hplus_m800,
                             "H^{+}#rightarrow hW^{+} (m_{H^{+}}=800GeV) x5", "L")
            if config["Plot_sig_Hplus_Wh_m1600-0"] == "Enable":
                leg.AddEntry(h_sig_Hplus_m1600,
                             "H^{+}#rightarrow hW^{+} (m_{H^{+}}=1600GeV) x5", "L")

            if h_all_background != 0:
                leg.AddEntry(h_all_background,    "t#bar{t}", "F")
            if h_other_background_list != []:
                leg.AddEntry(h_other_background,  "other backgrounds", "F")
            leg.Draw()
            c1.RedrawAxis()
            c1.Update()
            c1.RedrawAxis()
            c1.SaveAs(histoDir + "/ShapePlot_%s.pdf" %
                      (HistoName+"_"+Region+"_"+btagStrategy))
        significanceFile.write(
            HistoName + "," + Region + "," + ",".join(significanceValues) + "\n")
significanceFile.close()
