# -*- coding: utf-8 -*-
# python
import sys
import glob
import math
import re
from ROOT import *
from array import *
from configparser import configParser, getConfigData, getPlotFiles, getXaxisLabel

_, config_path = sys.argv

config = configParser(config_path)
MCDataPeriodes = getConfigData(config, "Stack_")
histoNames = getConfigData(config, "Graph_")
btagStrategies = getConfigData(config, "Btag_")
dataPeriodeStack = "-".join(MCDataPeriodes)
histoFiles = {i: getPlotFiles(config, i) for i in MCDataPeriodes}
plotEvents = getConfigData(config, "Plot_")

outputdir = "../Plots/" + config["WP"] + "/" + "StackPlots" + "/" + dataPeriodeStack + "-" + config["Higgs_mass_lower_bound"] + "-" + config["Higgs_mass_upper_bound"] + "-" +
config["Wboson_mass_lower_bound"] + "-" + config["Wboson_mass_upper_bound"] + "-" + config["Missing_transverse_momentum"] + "-" +
config["Lepton_transverse_momentum"] + "-" + config["2Jets_Jet1_transverse_momentum"] + "-" +
config["2Jets_Jet2_transverse_momentum"] + "-" + config["2Jets_Jet1_lepton_angle"] + "-" + config["2Jets_Jet2_lepton_angle"] + "-" +
config["Higgs_Wboson_angle"] + "-" + \
    config["1Jet_Jet_transverse_momentum"]

try:
    os.mkdir(outputdir)
except OSError:
    print "Creation of the directory %s failed" % outputdir
else:
    print "Successfully created the directory %s " % outputdir

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


def NormalizeHisto(histo):
    n_events = histo.Integral(-1, histo.GetNbinsX()+1)
    if n_events == 0:
        return
    print n_events, histo.Integral(histo.GetNbinsX(), histo.GetNbinsX()+1)
    histo.Scale(1./n_events)
    histo.SetLineWidth(2)
    histo.SetStats(0)
    histo.SetFillStyle(3001)
    histo.SetMarkerColor(histo.GetLineColor())
    histo.SetMarkerSize(0.0)
    histo.GetXaxis().SetTitleOffset(1.2)
    histo.GetYaxis().SetTitleOffset(1.52)
    histo.GetXaxis().SetLabelSize(0.05)
    histo.GetYaxis().SetLabelSize(0.05)
    histo.GetXaxis().SetTitleSize(0.05)
    histo.GetYaxis().SetTitleSize(0.05)
    histo.GetYaxis().SetNdivisions(504)
    histo.GetXaxis().SetNdivisions(504)


c1 = TCanvas("ShapePlots", "", 720, 720)

# for HistoName in ["Mwt", "Lepton_Pt", "HT", "mVH"]:
#    for Region in ["Resolved_LepP_SR", "Resolved_LepP_CR"]:
#        for btagStrategy in ["TwoTags", "ThreeTags"]:
for HistoName in histoNames:
    for Region in ["Merged_LepN_SR"]:
        for btagStrategy in btagStrategies:
            if config[Graph_Rebin] = "Enable":
                    ReBin = True
                else:
                    ReBin = False
            YAxisScale = 1.4
            Xaxis_label = getXaxisLabel(HistoName)

            # correct problem in maker: wrong normalisation
            dscale = 1.223695
            escale = 1.61419497
            h_other_background_list = []
            h_ttbar_background = []

            if config["Plot_sig_Hplus_Wh_m400-0"] == "Enable":
                h_sig_Hplus_m400list = []
                if config["Stack_MC16a"] == "Enable":
                    file1a = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16a"]["sig_Hplus_Wh_m400-0"], "READ")
                    dir1a = file1a.GetDirectory("Nominal").GetDirectory(HistoName)
                    h_sig_Hplus_m400a = dir1a.Get(
                    "sig_Hplus_Wh_m400-0_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_sig_Hplus_m400list.append(h_sig_Hplus_m400a)
                if config["Stack_MC16d"] == "Enable":
                    file1d = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16d"]["sig_Hplus_Wh_m400-0"], "READ")
                    dir1d = file1d.GetDirectory("Nominal").GetDirectory(HistoName)
                    h_sig_Hplus_m400d = dir1d.Get(
                    "sig_Hplus_Wh_m400-0_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_sig_Hplus_m400d.Scale(dscale)
                    h_sig_Hplus_m400list.append(h_sig_Hplus_m400d)
                if config["Stack_MC16e"] == "Enable":
                    file1e = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16e"]["sig_Hplus_Wh_m400-0"], "READ")
                    dir1e = file1e.GetDirectory("Nominal").GetDirectory(HistoName)     
                    h_sig_Hplus_m400e = dir1e.Get(
                    "sig_Hplus_Wh_m400-0_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_sig_Hplus_m400e.Scale(escale)
                    h_sig_Hplus_m400list.append(h_sig_Hplus_m400e)           
            
                h_sig_Hplus_m400 = sum(h_sig_Hplus_m400list)
                h_sig_Hplus_m400.SetLineColor(kBlack)
                h_sig_Hplus_m400.SetLineStyle(7)
                if ReBin == True:
                    h_sig_Hplus_m400.Rebin(2)

            if config["Plot_sig_Hplus_Wh_m800-0"] == "Enable":
                h_sig_Hplus_m800list = []
                if config["Stack_MC16a"] == "Enable":
                    file2a = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16a"]["sig_Hplus_Wh_m800-0"], "READ")
                    dir1a = file2a.GetDirectory("Nominal").GetDirectory(HistoName)
                    h_sig_Hplus_m800a = dir1a.Get(
                    "sig_Hplus_Wh_m800-0_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_sig_Hplus_m800list.append(h_sig_Hplus_m800a)
                if config["Stack_MC16d"] == "Enable":
                    file2d = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16d"]["sig_Hplus_Wh_m800-0"], "READ")
                    dir1d = file2d.GetDirectory("Nominal").GetDirectory(HistoName)
                    h_sig_Hplus_m800d = dir1d.Get(
                    "sig_Hplus_Wh_m800-0_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_sig_Hplus_m800d.Scale(dscale)
                    h_sig_Hplus_m800list.append(h_sig_Hplus_m800d)
                if config["Stack_MC16e"] == "Enable":
                    file2e = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16e"]["sig_Hplus_Wh_m800-0"], "READ")
                    dir1e = file2e.GetDirectory("Nominal").GetDirectory(HistoName)     
                    h_sig_Hplus_m800e = dir1e.Get(
                    "sig_Hplus_Wh_m800-0_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_sig_Hplus_m800e.Scale(escale)
                    h_sig_Hplus_m800list.append(h_sig_Hplus_m800e)           
            
                h_sig_Hplus_m800 = sum(h_sig_Hplus_m800list)
                h_sig_Hplus_m800.SetLineColor(kBlue)
                h_sig_Hplus_m800.SetLineStyle(7)
                if ReBin == True:
                    h_sig_Hplus_m800.Rebin(2)
            
            if config["Plot_sig_Hplus_Wh_m1600-0"] == "Enable":
                h_sig_Hplus_m1600list = []
                if config["Stack_MC16a"] == "Enable":
                    file3a = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16a"]["sig_Hplus_Wh_m1600-0"], "READ")
                    dir1a = file3a.GetDirectory("Nominal").GetDirectory(HistoName)
                    h_sig_Hplus_m1600a = dir1a.Get(
                    "sig_Hplus_Wh_m1600-0_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_sig_Hplus_m1600list.append(h_sig_Hplus_m1600a)
                if config["Stack_MC16d"] == "Enable":
                    file3d = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16d"]["sig_Hplus_Wh_m1600-0"], "READ")
                    dir1d = file3d.GetDirectory("Nominal").GetDirectory(HistoName)
                    h_sig_Hplus_m1600d = dir1d.Get(
                    "sig_Hplus_Wh_m1600-0_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_sig_Hplus_m1600d.Scale(dscale)
                    h_sig_Hplus_m1600list.append(h_sig_Hplus_m1600d)
                if config["Stack_MC16e"] == "Enable":
                    file3e = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16e"]["sig_Hplus_Wh_m1600-0"], "READ")
                    dir1e = file3e.GetDirectory("Nominal").GetDirectory(HistoName)     
                    h_sig_Hplus_m1600e = dir1e.Get(
                    "sig_Hplus_Wh_m1600-0_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_sig_Hplus_m1600e.Scale(escale)
                    h_sig_Hplus_m1600list.append(h_sig_Hplus_m1600e)           
            
                h_sig_Hplus_m1600 = sum(h_sig_Hplus_m1600list)
                h_sig_Hplus_m1600.SetLineColor(kViolet)
                h_sig_Hplus_m1600.SetLineStyle(7)
                if ReBin == True:
                    h_sig_Hplus_m1600.Rebin(2)
            
            if config["Plot_ttbar"] == "Enable":
                h_ttbar_background_list = []
                if config["Stack_MC16a"] == "Enable":
                    file3a = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16a"]["ttbar"], "READ")
                    dir1a = file3a.GetDirectory("Nominal").GetDirectory(HistoName)
                    h_ttbar_background_a = dir1a.Get(
                    "ttbar_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_ttbar_background_list.append(h_ttbar_background_a)
                if config["Stack_MC16d"] == "Enable":
                    file3d = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16d"]["ttbar"], "READ")
                    dir1d = file3d.GetDirectory("Nominal").GetDirectory(HistoName)
                    h_ttbar_background_d = dir1d.Get(
                    "ttbar_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_ttbar_background_d.Scale(dscale)
                    h_ttbar_background_list.append(h_ttbar_background_d)
                if config["Stack_MC16e"] == "Enable":
                    file3e = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16e"]["ttbar"], "READ")
                    dir1e = file3e.GetDirectory("Nominal").GetDirectory(HistoName)     
                    h_ttbar_background_e = dir1e.Get(
                    "ttbar_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_ttbar_background_e.Scale(escale)
                    h_ttbar_background_list.append(h_ttbar_background_e)           
            
                h_ttbar_background = sum(h_ttbar_background_list)
                h_ttbar_background.SetLineColor(kGreen+3)
                if ReBin == True:
                    h_ttbar_background.Rebin(2)

            elif config["Plot_ttbarSherpa"] == "Enable":
                h_ttbarSherpa_background_list = []
                if config["Stack_MC16a"] == "Enable":
                    file3a = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16a"]["ttbarSherpa"], "READ")
                    dir1a = file3a.GetDirectory("Nominal").GetDirectory(HistoName)
                    h_ttbarSherpa_background_a = dir1a.Get(
                    "ttbarSherpa_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_ttbarSherpa_background_list.append(h_ttbarSherpa_background_a)
                if config["Stack_MC16d"] == "Enable":
                    file3d = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16d"]["ttbarSherpa"], "READ")
                    dir1d = file3d.GetDirectory("Nominal").GetDirectory(HistoName)
                    h_ttbarSherpa_background_d = dir1d.Get(
                    "ttbarSherpa_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_ttbarSherpa_background_d.Scale(dscale)
                    h_ttbarSherpa_background_list.append(h_ttbarSherpa_background_d)
                if config["Stack_MC16e"] == "Enable":
                    file3e = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16e"]["ttbarSherpa"], "READ")
                    dir1e = file3e.GetDirectory("Nominal").GetDirectory(HistoName)     
                    h_ttbarSherpa_background_e = dir1e.Get(
                    "ttbarSherpa_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_ttbarSherpa_background_e.Scale(escale)
                    h_ttbarSherpa_background_list.append(h_ttbarSherpa_background_e)           
            
                h_ttbar_background = sum(h_ttbarSherpa_background_list)
                h_ttbar_background.SetLineColor(kGreen+3)
                if ReBin == True:
                    h_ttbar_background.Rebin(2)

            if config["Plot_Wjets"] == "Enable":
                h_Wjets_background_list = []
                if config["Stack_MC16a"] == "Enable":
                    file3a = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16a"]["Wjets"], "READ")
                    dir1a = file3a.GetDirectory("Nominal").GetDirectory(HistoName)
                    h_Wjets_background_a = dir1a.Get(
                    "Wjets_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_Wjets_background_list.append(h_Wjets_background_a)
                if config["Stack_MC16d"] == "Enable":
                    file3d = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16d"]["Wjets"], "READ")
                    dir1d = file3d.GetDirectory("Nominal").GetDirectory(HistoName)
                    h_Wjets_background_d = dir1d.Get(
                    "Wjets_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_Wjets_background_d.Scale(dscale)
                    h_Wjets_background_list.append(h_Wjets_background_d)
                if config["Stack_MC16e"] == "Enable":
                    file3e = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16e"]["Wjets"], "READ")
                    dir1e = file3e.GetDirectory("Nominal").GetDirectory(HistoName)     
                    h_Wjets_background_e = dir1e.Get(
                    "Wjets_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_Wjets_background_e.Scale(escale)
                    h_Wjets_background_list.append(h_Wjets_background_e)           
            
                h_Wjets_background = sum(h_Wjets_background_list)
                h_Wjets_background.SetLineColor(kRed-3)
                if ReBin == True:
                    h_Wjets_background.Rebin(2)
                h_other_background_list.append(h_Wjets_background)

            if config["Plot_Zjets"] == "Enable":
                h_Zjets_background_list = []
                if config["Stack_MC16a"] == "Enable":
                    file3a = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16a"]["Zjets"], "READ")
                    dir1a = file3a.GetDirectory("Nominal").GetDirectory(HistoName)
                    h_Zjets_background_a = dir1a.Get(
                    "Zjets_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_Zjets_background_list.append(h_Zjets_background_a)
                if config["Stack_MC16d"] == "Enable":
                    file3d = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16d"]["Zjets"], "READ")
                    dir1d = file3d.GetDirectory("Nominal").GetDirectory(HistoName)
                    h_Zjets_background_d = dir1d.Get(
                    "Zjets_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_Zjets_background_d.Scale(dscale)
                    h_Zjets_background_list.append(h_Zjets_background_d)
                if config["Stack_MC16e"] == "Enable":
                    file3e = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16e"]["Zjets"], "READ")
                    dir1e = file3e.GetDirectory("Nominal").GetDirectory(HistoName)     
                    h_Zjets_background_e = dir1e.Get(
                    "Zjets_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_Zjets_background_e.Scale(escale)
                    h_Zjets_background_list.append(h_Zjets_background_e)           
            
                h_Zjets_background = sum(h_Zjets_background_list)
                h_Zjets_background.SetLineColor(kRed-3)
                if ReBin == True:
                    h_Zjets_background.Rebin(2)
                h_other_background_list.append(h_Zjets_background)

            if config["Plot_diboson"] == "Enable":
                h_diboson_background_list = []
                if config["Stack_MC16a"] == "Enable":
                    file3a = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16a"]["diboson"], "READ")
                    dir1a = file3a.GetDirectory("Nominal").GetDirectory(HistoName)
                    h_diboson_background_a = dir1a.Get(
                    "diboson_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_diboson_background_list.append(h_diboson_background_a)
                if config["Stack_MC16d"] == "Enable":
                    file3d = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16d"]["diboson"], "READ")
                    dir1d = file3d.GetDirectory("Nominal").GetDirectory(HistoName)
                    h_diboson_background_d = dir1d.Get(
                    "diboson_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_diboson_background_d.Scale(dscale)
                    h_diboson_background_list.append(h_diboson_background_d)
                if config["Stack_MC16e"] == "Enable":
                    file3e = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16e"]["diboson"], "READ")
                    dir1e = file3e.GetDirectory("Nominal").GetDirectory(HistoName)     
                    h_diboson_background_e = dir1e.Get(
                    "diboson_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_diboson_background_e.Scale(escale)
                    h_diboson_background_list.append(h_diboson_background_e)           
            
                h_diboson_background = sum(h_diboson_background_list)
                h_diboson_background.SetLineColor(kRed-3)
                if ReBin == True:
                    h_diboson_background.Rebin(2)
                h_other_background_list.append(h_diboson_background)

            if config["Plot_singleTop"] == "Enable":
                h_singleTop_background_list = []
                if config["Stack_MC16a"] == "Enable":
                    file3a = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16a"]["singleTop"], "READ")
                    dir1a = file3a.GetDirectory("Nominal").GetDirectory(HistoName)
                    h_singleTop_background_a = dir1a.Get(
                    "singleTop_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_singleTop_background_list.append(h_singleTop_background_a)
                if config["Stack_MC16d"] == "Enable":
                    file3d = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16d"]["singleTop"], "READ")
                    dir1d = file3d.GetDirectory("Nominal").GetDirectory(HistoName)
                    h_singleTop_background_d = dir1d.Get(
                    "singleTop_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_singleTop_background_d.Scale(dscale)
                    h_singleTop_background_list.append(h_singleTop_background_d)
                if config["Stack_MC16e"] == "Enable":
                    file3e = TFile.Open("../PlotFiles/" +
                                        histoFiles["MC16e"]["singleTop"], "READ")
                    dir1e = file3e.GetDirectory("Nominal").GetDirectory(HistoName)     
                    h_singleTop_background_e = dir1e.Get(
                    "singleTop_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_singleTop_background_e.Scale(escale)
                    h_singleTop_background_list.append(h_singleTop_background_e)           
            
                h_singleTop_background = sum(h_singleTop_background_list)
                h_singleTop_background.SetLineColor(kRed-3)
                if ReBin == True:
                    h_singleTop_background.Rebin(2)
                h_other_background_list.append(h_singleTop_background)

            h_other_background = sum(h_other_background_list)
            h_all_background = h_ttbar_background + h_other_background
            h_sig_Hplus_m400.Scale(5)
            h_sig_Hplus_m800.Scale(5)
            h_sig_Hplus_m1600.Scale(5)

            if config["Plot_sig_Hplus_Wh_m400-0"] == "Enable":
                h_sig_Hplus_m400n = h_sig_Hplus_m400+h_all_background
            if config["Plot_sig_Hplus_Wh_m800-0"] == "Enable":
                h_sig_Hplus_m800n = h_sig_Hplus_m800+h_all_background
            if config["Plot_sig_Hplus_Wh_m1600-0"] == "Enable":
                h_sig_Hplus_m1600n = h_sig_Hplus_m1600+h_all_background
                
            h_all_background.SetLineColor(1)
            h_all_background.SetFillColor(kGreen+3)
            h_other_background.SetLineColor(1)
            h_other_background.SetFillColor(kRed-3)

            if config["Plot_sig_Hplus_Wh_m400-0"] == "Enable":
                h_sig_Hplus_m400n.SetNdivisions(8)
                h_sig_Hplus_m400n.SetXTitle(Xaxis_label)
                ymax = h_sig_Hplus_m400n.GetMaximum()
                h_sig_Hplus_m400n.GetYaxis().SetRangeUser(0.001, ymax*1.3)
                nbins = 20
                h_sig_Hplus_m400n.Draw("HIST")
            elif config["Plot_sig_Hplus_Wh_m800-0"] == "Enable":
                h_sig_Hplus_m800n.SetNdivisions(8)
                h_sig_Hplus_m800n.SetXTitle(Xaxis_label)
                ymax = h_sig_Hplus_m800n.GetMaximum()
                h_sig_Hplus_m800n.GetYaxis().SetRangeUser(0.001, ymax*1.3)
                nbins = 20
                h_sig_Hplus_m800n.Draw("HIST")
            elif config["Plot_sig_Hplus_Wh_m1600-0"] == "Enable":
                h_sig_Hplus_m1600n.SetNdivisions(8)
                h_sig_Hplus_m1600n.SetXTitle(Xaxis_label)
                ymax = h_sig_Hplus_m1600n.GetMaximum()
                h_sig_Hplus_m1600n.GetYaxis().SetRangeUser(0.001, ymax*1.3)
                nbins = 
                h_sig_Hplus_m1600n.Draw("HIST")
    
            h_all_background.Draw("HIST")
            h_other_background.Draw("HISTSAME")

            if config["Plot_sig_Hplus_Wh_m400-0"] == "Enable":
                h_sig_Hplus_m400n.Draw("HISTSAME")
            if config["Plot_sig_Hplus_Wh_m800-0"] == "Enable":
                h_sig_Hplus_m800n.Draw("HISTSAME")
            if config["Plot_sig_Hplus_Wh_m1600-0"] == "Enable":
                h_sig_Hplus_m1600n.Draw("HISTSAME")

            if HistoName in "maxMVAResponse":
                leg = TLegend(0.2, 0.65, 0.725, 0.855)
            else:
                leg = TLegend(0.42, 0.6, 0.92, 0.805)
            ATLAS_LABEL(0.20, 0.885, " Simulation Internal", 1, 0.19)
            myText(0.20, 0.825, 1, HistoName+" "+btagStrategy)
            leg.SetShadowColor(kWhite)
            leg.SetFillColor(kWhite)
            leg.SetLineColor(kWhite)

            if config["Plot_sig_Hplus_Wh_m400-0"] == "Enable":
            leg.AddEntry(h_sig_Hplus_m400,
                         "H^{+}#rightarrow hW^{+} (m_{H^{+}}=400GeV) x5", "L")
            if config["Plot_sig_Hplus_Wh_m800-0"] == "Enable":
            leg.AddEntry(h_sig_Hplus_m800,
                         "H^{+}#rightarrow hW^{+} (m_{H^{+}}=800GeV) x5", "L")
            if config["Plot_sig_Hplus_Wh_m1600-0"] == "Enable":
            leg.AddEntry(h_sig_Hplus_m1600,
                         "H^{+}#rightarrow hW^{+} (m_{H^{+}}=1600GeV) x5", "L")
            leg.AddEntry(h_all_background,    "t#bar{t}", "F")
            leg.AddEntry(h_other_background,  "other backgrounds", "F")
            leg.SetTextSize(0.0325)
            leg.Draw()
            # h_sig_Hplus_m400n.GetXaxis().SetTitle(Xaxis_label)
            # h_sig_Hplus_m400n.GetYaxis().SetRangeUser(0.001,ymax*1.3)
            # c1.RedrawAxis()
            # c1.Update()
            # c1.RedrawAxis()
            c1.SaveAs(outputdir + "/ShapePlot_%s_lvbb.pdf" %
                      (HistoName+"_"+Region+"_"+btagStrategy))
