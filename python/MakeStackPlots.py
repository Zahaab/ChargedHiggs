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

# THIS IS WHERE THE ACCEPTANCE IS HANDELED

cutParameters = ["TotalEvents", "Hadronic_rejected", "Leptonic_rejected", "MET", "Lepton_momentum", "Higgs_momentum",
                 "Wboson_momentum", "Higgs_Lepton_Angle", "Wboson_Lepton_Angle", "Higgs_Wboson_Angle", "PositiveLep_Wboson_bool",
                 "PositiveLep_Higgs_bool", "Higgs_Mass", "Wplus_Mass"]

realCutParameters = ["real"+i for i in cutParameters]

altcutParameters = ["TotalEvents", "Hadronic_rejected", "Leptonic_rejected", "jjbb_OR_lvbb_rejected", "Higgs_momentum",
                    "Higgs_Lepton_Angle", "Wboson_Lepton_Angle", "Higgs_Wboson_Angle", "PositiveLep_Wboson_bool",
                    "PositiveLep_Higgs_bool", "Higgs_Mass", "Wplus_Mass"]

altrealCutParameters = ["real"+i for i in altcutParameters]


def prepareCutHolder(cutHolder, cutParameters, btagStrategies):
    for parameter in cutParameters:
        cutHolder[parameter] = {}
        for channel in ["jjbb", "lvbb"]:
            cutHolder[parameter][channel] = {}
            for btagStrategy in btagStrategies:
                cutHolder[parameter][channel][btagStrategy] = []
            cutHolder[parameter][channel]["Total"] = []
    return cutHolder


def cutFlowExtraction(content, cutParameters, cutHolder):
    for index, parameter in enumerate(cutParameters):
        jjbb_values, lvbb_values = content[index].split("=")[1].split("|")
        for tagged_values in [(jjbb_values.split(","), "jjbb"), (lvbb_values.split(","), "lvbb")]:
            if tagged_values[0][-1] == "0":  # Some cut parameters don't cut anythign
                for btagStrategy in btagStrategies:
                    cutHolder[parameter][tagged_values[1]
                                         ][btagStrategy].append("0")
                cutHolder[parameter][tagged_values[1]]["Total"].append("0")
                continue
            for tagging, cutFlowValue in enumerate(tagged_values[0]):
                if tagged_values[0][tagging] == tagged_values[0][-1]:
                    cutHolder[parameter][tagged_values[1]
                                         ]["Total"].append(cutFlowValue)
                else:
                    cutHolder[parameter][tagged_values[1]][btagStrategies[tagging]].append(
                        cutFlowValue)


def cutFlowPercentExtraction(content, cutParameters, cutHolder):
    total_events = []
    for index, parameter in enumerate(cutParameters):
        jjbb_values, lvbb_values = content[index].split("=")[1].split("|")
        for tagged_values in [(jjbb_values.split(","), "jjbb"), (lvbb_values.split(","), "lvbb")]:
            if tagged_values[0][-1] == "0":  # Some cut parameters don't cut anythign
                for btagStrategy in btagStrategies:
                    cutHolder[parameter][tagged_values[1]
                                         ][btagStrategy].append("0")
                cutHolder[parameter][tagged_values[1]]["Total"].append("0")
                continue
            if parameter[-11:] == "TotalEvents":
                total_events = [float(i) for i in tagged_values[0]]
                for tagging, cutFlowValue in enumerate(tagged_values[0]):
                    if tagged_values[0][tagging] == tagged_values[0][-1]:
                        cutHolder[parameter][tagged_values[1]
                                             ]["Total"].append(cutFlowValue)
                    else:
                        cutHolder[parameter][tagged_values[1]][btagStrategies[tagging]].append(
                            cutFlowValue)
                continue
            for tagging, cutFlowValue in enumerate(tagged_values[0]):
                if tagged_values[0][tagging] == tagged_values[0][-1]:
                    cutHolder[parameter][tagged_values[1]]["Total"].append(
                        str((float(cutFlowValue)/total_events[-1])*100))
                else:
                    cutHolder[parameter][tagged_values[1]][btagStrategies[tagging]].append(
                        str((float(cutFlowValue)/total_events[tagging])*100))


def sumPercent(total_list, percents):
    flat_values = []
    for index, total in enumerate(total_list):
        if percents[index] == 0:
            continue
        flat_values.append(total*percents[index])
    if flat_values == []:
        return 0
    else:
        return (sum(flat_values)/sum(total_list))


def cutFlowInsertion(file, data_set, dataPeriodes, btagStrategies, cutParameters, cutHolder, Percent="disable"):
    for periodindex, dataPeriod in enumerate(dataPeriodes):
        for btagStrategy in btagStrategies:
            for channel in ["jjbb", "lvbb"]:
                rowData = [data_set, dataPeriod, btagStrategy, channel]
                rowValues = []
                total_events = 0
                for parameter in cutParameters:
                    if parameter[-11:] == "TotalEvents":
                        total_events = float(
                            cutHolder[parameter][channel][btagStrategy][periodindex])
                    rowValues.append(
                        float(cutHolder[parameter][channel][btagStrategy][periodindex]))
                    rowData.append(
                        str(cutHolder[parameter][channel][btagStrategy][periodindex]))
                file.write(",".join(rowData) + "," +
                           str(sum(rowValues) - total_events) + "\n")
        for channel in ["jjbb", "lvbb"]:
            rowData = [data_set, dataPeriod, "All_Tagging", channel]
            rowValues = []
            total_events = 0
            for parameter in cutParameters:
                if parameter[-11:] == "TotalEvents":
                    total_events = float(
                        cutHolder[parameter][channel]["Total"][periodindex])
                rowValues.append(
                    float(cutHolder[parameter][channel]["Total"][periodindex]))
                rowData.append(
                    str(cutHolder[parameter][channel]["Total"][periodindex]))
            file.write(",".join(rowData) + "," +
                       str(sum(rowValues) - total_events) + "\n")
    for btagStrategy in btagStrategies:
        for channel in ["jjbb", "lvbb"]:
            rowData = [data_set, "All_Data_Periods", btagStrategy, channel]
            rowValues = []
            total_events = 0
            total_events_list = []
            for parameter in cutParameters:
                if Percent == "enable":
                    if parameter[-11:] == "TotalEvents":
                        total_events_list = [
                            float(i) for i in cutHolder[parameter][channel][btagStrategy]]
                        valueAllPeriods = sum(
                            [float(i) for i in cutHolder[parameter][channel][btagStrategy]])
                    else:
                        valueAllPeriods = sumPercent(total_events_list, [float(
                            i) for i in cutHolder[parameter][channel][btagStrategy]])
                else:
                    if parameter[-11:] == "TotalEvents":
                        total_events = sum([float(i)
                                            for i in cutHolder[parameter][channel][btagStrategy]])
                    valueAllPeriods = sum([float(i)
                                           for i in cutHolder[parameter][channel][btagStrategy]])
                rowValues.append(float(valueAllPeriods))
                rowData.append(str(valueAllPeriods))
            if Percent == "enable":
                file.write(",".join(rowData) + "," +
                           str(sum(rowValues) - sum(total_events_list)) + "\n")
            else:
                file.write(",".join(rowData) + "," +
                           str(sum(rowValues) - total_events) + "\n")
    for channel in ["jjbb", "lvbb"]:
        rowData = [data_set, "All_Data_Periods", "All_Tagging", channel]
        rowValues = []
        total_events = 0
        for parameter in cutParameters:
            if Percent == "enable":
                if parameter[-11:] == "TotalEvents":
                    total_events_list = [float(i)
                                         for i in cutHolder[parameter][channel]["Total"]]
                    valueAllPeriods = sum([float(i)
                                           for i in cutHolder[parameter][channel]["Total"]])
                else:
                    valueAllPeriods = sumPercent(total_events_list, [float(
                        i) for i in cutHolder[parameter][channel]["Total"]])
            else:
                if parameter[-11:] == "TotalEvents":
                    total_events = sum([float(i)
                                        for i in cutHolder[parameter][channel]["Total"]])
                valueAllPeriods = sum([float(i)
                                       for i in cutHolder[parameter][channel]["Total"]])
            rowValues.append(float(valueAllPeriods))
            rowData.append(str(valueAllPeriods))

        if Percent == "enable":
            file.write(",".join(rowData) + "," +
                       str(sum(rowValues) - sum(total_events_list)) + "\n")
        else:
            file.write(",".join(rowData) + "," +
                       str(sum(rowValues) - total_events) + "\n")


cutFlowFile = open(outputdir + "/cutflow.txt", 'w')
cutFlowFile.truncate(0)  # to ensure the file is empty
cutFlowFile.write("Data-Set,"+"Data_Period," + "Number_of_Tags," + "Channel," +
                  ",".join(cutParameters) + "," + "Total" + "\n")

realCutFlowFile = open(outputdir + "/realcutflow.txt", 'w')
realCutFlowFile.truncate(0)
realCutFlowFile.write("Data-Set,"+"Data_Period," + "Number_of_Tags," + "Channel," +
                      ",".join(realCutParameters) + "," + "Total" + "\n")

cutFlowFilePercent = open(outputdir + "/cutflowPercent.txt", 'w')
cutFlowFilePercent.truncate(0)
cutFlowFilePercent.write("Data-Set,"+"Data_Period," + "Number_of_Tags," + "Channel," +
                         ",".join(cutParameters) + "," + "Total" + "\n")

realCutFlowFilePercent = open(outputdir + "/realcutflowPercent.txt", 'w')
realCutFlowFilePercent.truncate(0)
realCutFlowFilePercent.write("Data-Set,"+"Data_Period," + "Number_of_Tags," + "Channel," +
                             ",".join(realCutParameters) + "," + "Total" + "\n")

# vvvvv THIS IS FOR THE ALTERNATE CUT FLOW vvvvvv

altcutFlowFile = open(outputdir + "/altcutflow.txt", 'w')
altcutFlowFile.truncate(0)  # to ensure the file is empty
altcutFlowFile.write("Data-Set,"+"Data_Period," + "Number_of_Tags," + "Channel," +
                     ",".join(altcutParameters) + "," + "Total" + "\n")

altrealCutFlowFile = open(outputdir + "/altrealcutflow.txt", 'w')
altrealCutFlowFile.truncate(0)
altrealCutFlowFile.write("Data-Set,"+"Data_Period," + "Number_of_Tags," + "Channel," +
                         ",".join(altrealCutParameters) + "," + "Total" + "\n")

altcutFlowFilePercent = open(outputdir + "/altcutflowpercent.txt", 'w')
altcutFlowFilePercent.truncate(0)
altcutFlowFilePercent.write("Data-Set,"+"Data_Period," + "Number_of_Tags," + "Channel," +
                            ",".join(altcutParameters) + "," + "Total" + "\n")

altrealCutFlowFilePercent = open(outputdir + "/altrealcutflowpercent.txt", 'w')
altrealCutFlowFilePercent.truncate(0)
altrealCutFlowFilePercent.write("Data-Set,"+"Data_Period," + "Number_of_Tags," + "Channel," +
                                ",".join(altrealCutParameters) + "," + "Total" + "\n")

# ^^^^^^ THIS IS FOR THE ALTERNATE CUT FLOW ^^^^^

for data_set in plotEvents:  # Grabs the data sets
    cutFlowHold = {}
    realCutFlowHold = {}
    cutFlowHoldPercent = {}
    realCutFlowHoldPercent = {}
    cutFlowHold = prepareCutHolder(cutFlowHold, cutParameters, btagStrategies)
    realCutFlowHold = prepareCutHolder(
        realCutFlowHold, realCutParameters, btagStrategies)
    cutFlowHoldPercent = prepareCutHolder(
        cutFlowHoldPercent, cutParameters, btagStrategies)
    realCutFlowHoldPercent = prepareCutHolder(
        realCutFlowHoldPercent, realCutParameters, btagStrategies)

    altcutFlowHold = {}
    altrealCutFlowHold = {}
    altcutFlowHoldPercent = {}
    altrealCutFlowHoldPercent = {}
    altcutFlowHold = prepareCutHolder(
        altcutFlowHold, altcutParameters, btagStrategies)
    altrealCutFlowHold = prepareCutHolder(
        altrealCutFlowHold, altrealCutParameters, btagStrategies)
    altcutFlowHoldPercent = prepareCutHolder(
        altcutFlowHoldPercent, altcutParameters, btagStrategies)
    altrealCutFlowHoldPercent = prepareCutHolder(
        altrealCutFlowHoldPercent, altrealCutParameters, btagStrategies)

    for dataPeriod in MCDataPeriodes:
        cutFlow_content = []
        realCutFlow_content = []
        cutFlowPath = histoFiles[dataPeriod][data_set].replace(
            ".root", "-cutFlow.txt")
        rawCutFlow = open("../PlotFiles/"+cutFlowPath, "r")
        rawCutFlow_content = rawCutFlow.read().split("\n")

        altcutFlow_content = []
        altrealCutFlow_content = []
        altcutFlowPath = histoFiles[dataPeriod][data_set].replace(
            ".root", "-cutFlowAlt.txt")
        altrawCutFlow = open("../PlotFiles/"+altcutFlowPath, "r")
        altrawCutFlow_content = altrawCutFlow.read().split("\n")

        for line in rawCutFlow_content:
            if line == "":
                continue
            if line.split("=")[0][-9:-1] == "noFatJets":
                continue
            if line[0:4] == "real":
                realCutFlow_content.append(line)
            else:
                cutFlow_content.append(line)

        for line in altrawCutFlow_content:
            if line == "":
                continue
            if line.split("=")[0][-9:-1] == "noFatJet":
                continue
            if line[0:4] == "real":
                altrealCutFlow_content.append(line)
            else:
                altcutFlow_content.append(line)

        cutFlowExtraction(cutFlow_content, cutParameters, cutFlowHold)
        cutFlowExtraction(realCutFlow_content,
                          realCutParameters, realCutFlowHold)
        cutFlowPercentExtraction(
            cutFlow_content, cutParameters, cutFlowHoldPercent)
        cutFlowPercentExtraction(realCutFlow_content,
                                 realCutParameters, realCutFlowHoldPercent)

        cutFlowExtraction(altcutFlow_content, altcutParameters, altcutFlowHold)
        cutFlowExtraction(altrealCutFlow_content,
                          altrealCutParameters, altrealCutFlowHold)
        cutFlowPercentExtraction(
            altcutFlow_content, altcutParameters, altcutFlowHoldPercent)
        cutFlowPercentExtraction(altrealCutFlow_content,
                                 altrealCutParameters, altrealCutFlowHoldPercent)
        rawCutFlow.close()
        altrawCutFlow.close()

    cutFlowInsertion(cutFlowFile, data_set, MCDataPeriodes,
                     btagStrategies, cutParameters, cutFlowHold)
    cutFlowInsertion(realCutFlowFile, data_set, MCDataPeriodes,
                     btagStrategies, realCutParameters, realCutFlowHold)
    cutFlowInsertion(cutFlowFilePercent, data_set, MCDataPeriodes,
                     btagStrategies, cutParameters, cutFlowHoldPercent, "enable")
    cutFlowInsertion(realCutFlowFilePercent, data_set, MCDataPeriodes,
                     btagStrategies, realCutParameters, realCutFlowHoldPercent, "enable")
    cutFlowInsertion(altcutFlowFile, data_set, MCDataPeriodes,
                     btagStrategies, altcutParameters, altcutFlowHold)
    cutFlowInsertion(altrealCutFlowFile, data_set, MCDataPeriodes,
                     btagStrategies, altrealCutParameters, altrealCutFlowHold)
    cutFlowInsertion(altcutFlowFilePercent, data_set, MCDataPeriodes,
                     btagStrategies, altcutParameters, altcutFlowHoldPercent, "enable")
    cutFlowInsertion(altrealCutFlowFilePercent, data_set, MCDataPeriodes,
                     btagStrategies, altrealCutParameters, altrealCutFlowHoldPercent, "enable")

cutFlowFile.close()
realCutFlowFile.close()
cutFlowFilePercent.close()
realCutFlowFilePercent.close()

altcutFlowFile.close()
altrealCutFlowFile.close()
altcutFlowFilePercent.close()
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
    "HisogramName,"+",".join(signalMasses) + "\n")


def calcSignificance(signalHisto, backgroundHisto):
    h1 = signalHisto.Clone()
    h2 = backgroundHisto.Clone()
    sigList = []
    for i in range(h1.GetNbinsX()):
        signal = abs(h1.GetBinContent(i))
        background = abs(h2.GetBinContent(i))
        if signal and background != 0.0:
            x = 2 * ((signal+background) *
                     math.log(1+(signal/background)) - signal)
            sigList.append(x)
    significance = math.sqrt(sum(sigList))
    return significance

# NOW WE GRAPH THE FIGURES


gROOT.SetBatch(True)
gStyle.SetOptStat(0)
gStyle.SetPalette(1)
gROOT.LoadMacro("../style/AtlasStyle.C")
gROOT.LoadMacro("../style/AtlasUtils.C")
SetAtlasStyle()

y_axis_label = "Event fraction"
c_blue = TColor.GetColor("#3366ff")
c_red = TColor.GetColor("#ee3311")
c_orange = TColor.GetColor("#ff9900")


def sumHistosList(histo_list):
    resultHisto = 0
    if len(histo_list) > 0:
        for i in histo_list:
            if resultHisto == 0:
                resultHisto = i
            else:
                resultHisto += i
    return resultHisto

# def NormalizeHisto(histo):
#     n_events = histo.Integral(-1, histo.GetNbinsX()+1)
#     if n_events == 0:
#         return
#     print n_events, histo.Integral(histo.GetNbinsX(), histo.GetNbinsX()+1)
#     histo.Scale(1./n_events)
#     histo.SetLineWidth(2)
#     histo.SetStats(0)
#     histo.SetFillStyle(3001)
#     histo.SetMarkerColor(histo.GetLineColor())
#     histo.SetMarkerSize(0.0)
#     histo.GetXaxis().SetTitleOffset(1.2)
#     histo.GetYaxis().SetTitleOffset(1.52)
#     histo.GetXaxis().SetLabelSize(0.05)
#     histo.GetYaxis().SetLabelSize(0.05)
#     histo.GetXaxis().SetTitleSize(0.05)
#     histo.GetYaxis().SetTitleSize(0.05)
#     histo.GetYaxis().SetNdivisions(504)
#     histo.GetXaxis().SetNdivisions(504)


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

    for Region in ["Merged_LepP_SR", "Merged_LepN_SR"]:
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
            print histoFiles
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

            if config["Plot_ttbar"] == "Enable":
                h_ttbar_background_list = []
                if config["Stack_MC16a"] == "Enable":
                    file4a = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16a"]["ttbar"], "READ")
                    dir4a = file4a.GetDirectory(
                        "Nominal").GetDirectory(HistoName)
                    h_ttbar_background_a = dir4a.Get(
                        "ttbar_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_ttbar_background_list.append(h_ttbar_background_a)
                if config["Stack_MC16d"] == "Enable":
                    file4d = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16d"]["ttbar"], "READ")
                    dir4d = file4d.GetDirectory(
                        "Nominal").GetDirectory(HistoName)
                    h_ttbar_background_d = dir4d.Get(
                        "ttbar_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_ttbar_background_d.Scale(dscale)
                    h_ttbar_background_list.append(h_ttbar_background_d)
                if config["Stack_MC16e"] == "Enable":
                    file4e = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16e"]["ttbar"], "READ")
                    dir4e = file4e.GetDirectory(
                        "Nominal").GetDirectory(HistoName)
                    h_ttbar_background_e = dir4e.Get(
                        "ttbar_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_ttbar_background_e.Scale(escale)
                    h_ttbar_background_list.append(h_ttbar_background_e)

                h_ttbar_background = sumHistosList(h_ttbar_background_list)
                h_ttbar_background.SetLineColor(kGreen+3)
                if ReBin == True:
                    h_ttbar_background.Rebin(2)

            elif config["Plot_ttbarSherpa"] == "Enable":
                h_ttbarSherpa_background_list = []
                if config["Stack_MC16a"] == "Enable":
                    file5a = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16a"]["ttbarSherpa"], "READ")
                    dir5a = file5a.GetDirectory(
                        "Nominal").GetDirectory(HistoName)
                    h_ttbarSherpa_background_a = dir5a.Get(
                        "ttbarSherpa_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_ttbarSherpa_background_list.append(
                        h_ttbarSherpa_background_a)
                if config["Stack_MC16d"] == "Enable":
                    file5d = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16d"]["ttbarSherpa"], "READ")
                    dir5d = file5d.GetDirectory(
                        "Nominal").GetDirectory(HistoName)
                    h_ttbarSherpa_background_d = dir5d.Get(
                        "ttbarSherpa_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_ttbarSherpa_background_d.Scale(dscale)
                    h_ttbarSherpa_background_list.append(
                        h_ttbarSherpa_background_d)
                if config["Stack_MC16e"] == "Enable":
                    file5e = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16e"]["ttbarSherpa"], "READ")
                    dir5e = file5e.GetDirectory(
                        "Nominal").GetDirectory(HistoName)
                    h_ttbarSherpa_background_e = dir5e.Get(
                        "ttbarSherpa_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_ttbarSherpa_background_e.Scale(escale)
                    h_ttbarSherpa_background_list.append(
                        h_ttbarSherpa_background_e)

                h_ttbar_background = sumHistosList(
                    h_ttbarSherpa_background_list)
                h_ttbar_background.SetLineColor(kGreen+3)
                if ReBin == True:
                    h_ttbar_background.Rebin(2)

            if config["Plot_Wjets"] == "Enable":
                h_Wjets_background_list = []
                if config["Stack_MC16a"] == "Enable":
                    file6a = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16a"]["Wjets"], "READ")
                    dir6a = file6a.GetDirectory(
                        "Nominal").GetDirectory(HistoName)
                    h_Wjets_background_a = dir6a.Get(
                        "Wjets_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_Wjets_background_list.append(h_Wjets_background_a)
                if config["Stack_MC16d"] == "Enable":
                    file6d = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16d"]["Wjets"], "READ")
                    dir6d = file6d.GetDirectory(
                        "Nominal").GetDirectory(HistoName)
                    h_Wjets_background_d = dir6d.Get(
                        "Wjets_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_Wjets_background_d.Scale(dscale)
                    h_Wjets_background_list.append(h_Wjets_background_d)
                if config["Stack_MC16e"] == "Enable":
                    file6e = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16e"]["Wjets"], "READ")
                    dir6e = file6e.GetDirectory(
                        "Nominal").GetDirectory(HistoName)
                    h_Wjets_background_e = dir6e.Get(
                        "Wjets_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_Wjets_background_e.Scale(escale)
                    h_Wjets_background_list.append(h_Wjets_background_e)

                h_Wjets_background = sumHistosList(h_Wjets_background_list)
                h_Wjets_background.SetLineColor(kRed-3)
                if ReBin == True:
                    h_Wjets_background.Rebin(2)
                h_other_background_list.append(h_Wjets_background)

            if config["Plot_Zjets"] == "Enable":
                h_Zjets_background_list = []
                if config["Stack_MC16a"] == "Enable":
                    file7a = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16a"]["Zjets"], "READ")
                    dir7a = file7a.GetDirectory(
                        "Nominal").GetDirectory(HistoName)
                    h_Zjets_background_a = dir7a.Get(
                        "Zjets_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_Zjets_background_list.append(h_Zjets_background_a)
                if config["Stack_MC16d"] == "Enable":
                    file7d = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16d"]["Zjets"], "READ")
                    dir7d = file7d.GetDirectory(
                        "Nominal").GetDirectory(HistoName)
                    h_Zjets_background_d = dir7d.Get(
                        "Zjets_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_Zjets_background_d.Scale(dscale)
                    h_Zjets_background_list.append(h_Zjets_background_d)
                if config["Stack_MC16e"] == "Enable":
                    file7e = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16e"]["Zjets"], "READ")
                    dir7e = file7e.GetDirectory(
                        "Nominal").GetDirectory(HistoName)
                    h_Zjets_background_e = dir7e.Get(
                        "Zjets_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_Zjets_background_e.Scale(escale)
                    h_Zjets_background_list.append(h_Zjets_background_e)

                h_Zjets_background = sumHistosList(h_Zjets_background_list)
                h_Zjets_background.SetLineColor(kRed-3)
                if ReBin == True:
                    h_Zjets_background.Rebin(2)
                h_other_background_list.append(h_Zjets_background)

            if config["Plot_diboson"] == "Enable":
                h_diboson_background_list = []
                if config["Stack_MC16a"] == "Enable":
                    file8a = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16a"]["diboson"], "READ")
                    dir8a = file8a.GetDirectory(
                        "Nominal").GetDirectory(HistoName)
                    h_diboson_background_a = dir8a.Get(
                        "diboson_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_diboson_background_list.append(h_diboson_background_a)
                if config["Stack_MC16d"] == "Enable":
                    file8d = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16d"]["diboson"], "READ")
                    dir8d = file8d.GetDirectory(
                        "Nominal").GetDirectory(HistoName)
                    h_diboson_background_d = dir8d.Get(
                        "diboson_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_diboson_background_d.Scale(dscale)
                    h_diboson_background_list.append(h_diboson_background_d)
                if config["Stack_MC16e"] == "Enable":
                    file8e = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16e"]["diboson"], "READ")
                    dir8e = file8e.GetDirectory(
                        "Nominal").GetDirectory(HistoName)
                    h_diboson_background_e = dir8e.Get(
                        "diboson_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_diboson_background_e.Scale(escale)
                    h_diboson_background_list.append(h_diboson_background_e)

                h_diboson_background = sumHistosList(h_diboson_background_list)
                h_diboson_background.SetLineColor(kRed-3)
                if ReBin == True:
                    h_diboson_background.Rebin(2)
                h_other_background_list.append(h_diboson_background)

            if config["Plot_singleTop"] == "Enable":
                h_singleTop_background_list = []
                if config["Stack_MC16a"] == "Enable":
                    file9a = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16a"]["singleTop"], "READ")
                    dir9a = file9a.GetDirectory(
                        "Nominal").GetDirectory(HistoName)
                    h_singleTop_background_a = dir9a.Get(
                        "singleTop_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_singleTop_background_list.append(
                        h_singleTop_background_a)
                if config["Stack_MC16d"] == "Enable":
                    file9d = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16d"]["singleTop"], "READ")
                    dir9d = file9d.GetDirectory(
                        "Nominal").GetDirectory(HistoName)
                    h_singleTop_background_d = dir9d.Get(
                        "singleTop_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_singleTop_background_d.Scale(dscale)
                    h_singleTop_background_list.append(
                        h_singleTop_background_d)
                if config["Stack_MC16e"] == "Enable":
                    file9e = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16e"]["singleTop"], "READ")
                    dir9e = file9e.GetDirectory(
                        "Nominal").GetDirectory(HistoName)
                    h_singleTop_background_e = dir9e.Get(
                        "singleTop_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_singleTop_background_e.Scale(escale)
                    h_singleTop_background_list.append(
                        h_singleTop_background_e)

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
                    significanceValues.append(calcSignificance(
                        h_sig_Hplus_m400, h_all_background))
                else:
                    significanceValues.append("NaN")
                if config["Plot_sig_Hplus_Wh_m800-0"] == "Enable":
                    significanceValues.append(calcSignificance(
                        h_sig_Hplus_m800, h_all_background))
                else:
                    significanceValues.append("NaN")
                if config["Plot_sig_Hplus_Wh_m1600-0"] == "Enable":
                    significanceValues.append(calcSignificance(
                        h_sig_Hplus_m1600, h_all_background))
                else:
                    significanceValues.append("NaN")

            # THIS IS WHERE THE SIGNIFICANCE IS HANDELED

            # BACK TO GRAPHING

            if h_all_background == 0:
                if config["Plot_sig_Hplus_Wh_m400-0"] == "Enable":
                    h_sig_Hplus_m400.Scale(5)
                    h_sig_Hplus_m400n = h_sig_Hplus_m400d
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
                h_all_background.SetFillColor(kGreen+3)
            if h_other_background_list != []:
                h_other_background.SetLineColor(1)
                h_other_background.SetFillColor(kRed-3)

            nbins = 20
            ymax = 0
            xmax = 0
            # NormalizeHisto(h_other_background)
            if h_other_background_list != []:
                if ymax < h_other_background.GetMaximum():
                    ymax = h_other_background.GetMaximum()
                if xmax < h_other_background.GetMaximum():
                    xmax = h_other_background.GetMaximum()
            # NormalizeHisto(h_all_background)
            if h_all_background != 0:
                if ymax < h_all_background.GetMaximum():
                    ymax = h_all_background.GetMaximum()
                if xmax < h_all_background.GetMaximum():
                    xmax = h_all_background.GetMaximum()

            if config["Plot_ttbar"] == "Enable" or config["Plot_ttbarSherpa"] == "Enable":
                # NormalizeHisto(h_ttbar_background)
                if ymax < h_ttbar_background.GetMaximum():
                    ymax = h_ttbar_background.GetMaximum()
                if xmax < h_ttbar_background.GetMaximum():
                    xmax = h_ttbar_background.GetMaximum()

            if config["Plot_sig_Hplus_Wh_m400-0"] == "Enable":
                # NormalizeHisto(h_sig_Hplus_m400)
                if ymax < h_sig_Hplus_m400.GetMaximum():
                    ymax = h_sig_Hplus_m400.GetMaximum()
                if xmax < h_sig_Hplus_m400.GetMaximum():
                    xmax = h_sig_Hplus_m400.GetMaximum()
            if config["Plot_sig_Hplus_Wh_m800-0"] == "Enable":
                # NormalizeHisto(h_sig_Hplus_m800)
                if ymax < h_sig_Hplus_m800.GetMaximum():
                    ymax = h_sig_Hplus_m800.GetMaximum()
                if xmax < h_sig_Hplus_m800.GetMaximum():
                    xmax = h_sig_Hplus_m800.GetMaximum()
            if config["Plot_sig_Hplus_Wh_m1600-0"] == "Enable":
                # NormalizeHisto(h_sig_Hplus_m1600)
                if ymax < h_sig_Hplus_m1600.GetMaximum():
                    ymax = h_sig_Hplus_m1600.GetMaximum()
                if xmax < h_sig_Hplus_m1600.GetMaximum():
                    xmax = h_sig_Hplus_m1600.GetMaximum()

            if h_all_background != 0:
                h_all_background.SetNdivisions(8)
                h_all_background.SetXTitle(Xaxis_label)
                h_all_background.GetYaxis().SetRangeUser(0.001, ymax*1.5)
                h_all_background.GetXaxis().SetRangeUser(0.001, 700)
                h_all_background.Draw("HIST")
                if h_other_background_list != []:
                    h_other_background.Draw("HISTSAME")
                if config["Plot_sig_Hplus_Wh_m400-0"] == "Enable":
                    h_sig_Hplus_m400n.Draw("HISTSAME")
                if config["Plot_sig_Hplus_Wh_m800-0"] == "Enable":
                    h_sig_Hplus_m800n.Draw("HISTSAME")
                if config["Plot_sig_Hplus_Wh_m1600-0"] == "Enable":
                    h_sig_Hplus_m1600n.Draw("HISTSAME")
            elif h_other_background_list != []:
                h_other_background.SetNdivisions(8)
                h_other_background.SetXTitle(Xaxis_label)
                h_other_background.GetYaxis().SetRangeUser(0.001, ymax*1.5)
                h_other_background.GetXaxis().SetRangeUser(0.001, 700)
                h_other_background.Draw("HIST")
                if config["Plot_sig_Hplus_Wh_m400-0"] == "Enable":
                    h_sig_Hplus_m400n.Draw("HISTSAME")
                if config["Plot_sig_Hplus_Wh_m800-0"] == "Enable":
                    h_sig_Hplus_m800n.Draw("HISTSAME")
                if config["Plot_sig_Hplus_Wh_m1600-0"] == "Enable":
                    h_sig_Hplus_m1600n.Draw("HISTSAME")
            elif config["Plot_sig_Hplus_Wh_m400-0"] == "Enable":
                h_sig_Hplus_m400.SetNdivisions(8)
                h_sig_Hplus_m400.SetXTitle(Xaxis_label)
                h_sig_Hplus_m400.GetYaxis().SetRangeUser(0.001, ymax*1.5)
                h_sig_Hplus_m400.GetXaxis().SetRangeUser(0.001, 700)
                h_sig_Hplus_m400.Draw("HIST")
                if config["Plot_sig_Hplus_Wh_m800-0"] == "Enable":
                    h_sig_Hplus_m800n.Draw("HISTSAME")
                if config["Plot_sig_Hplus_Wh_m1600-0"] == "Enable":
                    h_sig_Hplus_m1600n.Draw("HISTSAME")
            elif config["Plot_sig_Hplus_Wh_m800-0"] == "Enable":
                h_sig_Hplus_m800.SetNdivisions(8)
                h_sig_Hplus_m800.SetXTitle(Xaxis_label)
                h_sig_Hplus_m800.GetYaxis().SetRangeUser(0.001, ymax*1.5)
                h_sig_Hplus_m800.GetXaxis().SetRangeUser(0.001, 700)
                h_sig_Hplus_m800.Draw("HIST")
                if config["Plot_sig_Hplus_Wh_m1600-0"] == "Enable":
                    h_sig_Hplus_m1600n.Draw("HISTSAME")
            elif config["Plot_sig_Hplus_Wh_m1600-0"] == "Enable":
                h_sig_Hplus_m1600.SetNdivisions(8)
                h_sig_Hplus_m1600.SetXTitle(Xaxis_label)
                h_sig_Hplus_m1600.GetYaxis().SetRangeUser(0.001, ymax*1.5)
                h_sig_Hplus_m1600.GetXaxis().SetRangeUser(0.001, 700)
                h_sig_Hplus_m1600.Draw("HIST")

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
            c1.SaveAs(histoDir + "/ShapePlot_%s_lvbb.pdf" %
                      (HistoName+"_"+Region+"_"+btagStrategy))

        significanceFile.write(
            HistoName + "," + ",".join(significanceValues) + "\n")
significanceFile.close()
