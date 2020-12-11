# -*- coding: utf-8 -*-
# python
import sys
import glob
import math
import re
import os
from ROOT import *
from array import *
from configparser import configParser, getConfigData, getPlotFiles, getaxisLabels

_, config_path = sys.argv


config = configParser(config_path)
MCDataPeriodes = getConfigData(config, "Stack_")
histoNames = getConfigData(config, "Graph_")
btagStrategies = getConfigData(config, "Btag_")


def NormalizeHisto(histo):
    n_events = histo.Integral(-1, histo.GetNbinsX()+1)
    if n_events == 0:
        return
    # print n_events, histo.Integral(histo.GetNbinsX(), histo.GetNbinsX()+1)
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


for MCDataPeriode in MCDataPeriodes:
    histoFiles = getPlotFiles(config, MCDataPeriode)

    outputdir = str("../Plots/" +
                    config["WP"] + "/" + MCDataPeriode +
                    "/" + config["Higgs_mass_lower_bound"]
                    + "-" + config["Higgs_mass_upper_bound"] + "-" +
                    config["Wboson_mass_lower_bound"] + "-" +
                    config["Wboson_mass_upper_bound"]
                    + "-" + config["Missing_transverse_momentum"] + "-" +
                    config["Lepton_transverse_momentum"] + "-" +
                    config["2Jets_Jet1_transverse_momentum"]
                    + "-" + config["2Jets_Jet2_transverse_momentum"] + "-" +
                    config["2Jets_Jet1_lepton_angle"] + "-" +
                    config["2Jets_Jet2_lepton_angle"]
                    + "-" + config["Higgs_Wboson_angle"] + "-" +
                    config["1Jet_Jet_transverse_momentum"])

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

    c1 = TCanvas("ShapePlots", "", 720, 720)
    # for HistoName in ["Mwt"]:
    for HistoName in histoNames:
        histoDir = outputdir + "/" + HistoName
        try:
            os.mkdir(histoDir)
        except OSError:
            pass
        Xaxis_label, legend_place, text_place = getaxisLabels(HistoName)
        leg_pl1, leg_pl2, leg_pl3, leg_pl4 = legend_place
        test_pl1, test_pl2 = text_place

        for Region in ["Merged_LepN_SR"]:
            # What is Incl in terms of BTagStrategy?
            for btagStrategy in btagStrategies:
                # for btagStrategy in ["TwoTags"]:
                ReBin = False
                if config["Rebin"] == "Enable":
                    ReBin = True
                else:
                    ReBin = False
                YAxisScale = 1.4
                h_other_backgroundlist = []

                if config["Plot_sig_Hplus_Wh_m400-0"] == "Enable":
                    file1 = TFile.Open("../PlotFiles/" +
                                       histoFiles["sig_Hplus_Wh_m400-0"], "READ")
                    dir1 = file1.GetDirectory(
                        "Nominal").GetDirectory(HistoName)
                    h_sig_Hplus_m400 = dir1.Get(
                        "sig_Hplus_Wh_m400-0_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_sig_Hplus_m400.SetLineColor(kBlack)
                    h_sig_Hplus_m400.SetLineStyle(7)
                    if ReBin == True:
                        h_sig_Hplus_m400.Rebin(2)

                if config["Plot_sig_Hplus_Wh_m800-0"] == "Enable":
                    file2 = TFile.Open("../PlotFiles/" +
                                       histoFiles["sig_Hplus_Wh_m800-0"], "READ")
                    dir2 = file2.GetDirectory(
                        "Nominal").GetDirectory(HistoName)
                    h_sig_Hplus_m800 = dir2.Get(
                        "sig_Hplus_Wh_m800-0_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_sig_Hplus_m800.SetLineColor(kBlue)
                    h_sig_Hplus_m800.SetLineStyle(3)
                    if ReBin == True:
                        h_sig_Hplus_m800.Rebin(2)

                if config["Plot_sig_Hplus_Wh_m1600-0"] == "Enable":
                    file3 = TFile.Open("../PlotFiles/" +
                                       histoFiles["sig_Hplus_Wh_m1600-0"], "READ")
                    dir3 = file3.GetDirectory(
                        "Nominal").GetDirectory(HistoName)
                    h_sig_Hplus_m1600 = dir3.Get(
                        "sig_Hplus_Wh_m1600-0_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_sig_Hplus_m1600.SetLineColor(kViolet)
                    h_sig_Hplus_m1600.SetLineStyle(9)
                    if ReBin == True:
                        h_sig_Hplus_m1600.Rebin(2)

                if config["Plot_ttbar"] == "Enable":
                    file4 = TFile.Open("../PlotFiles/" +
                                       histoFiles["ttbar"], "READ")
                    dir4 = file4.GetDirectory(
                        "Nominal").GetDirectory(HistoName)
                    h_ttbar_background = dir4.Get(
                        "ttbar_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_ttbar_background.SetLineColor(kGreen+3)
                    if ReBin == True:
                        h_ttbar_background.Rebin(2)

                elif config["Plot_ttbarSherpa"] == "Enable":
                    file5 = TFile.Open("../PlotFiles/" +
                                       histoFiles["ttbarSherpa"], "READ")
                    dir5 = file5.GetDirectory(
                        "Nominal").GetDirectory(HistoName)
                    h_ttbarSherpa_background = dir5.Get(
                        "ttbarSherpa_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_ttbarSherpa_background.SetLineColor(kGreen+3)
                    if ReBin == True:
                        h_ttbarSherpa_background.Rebin(2)

                if config["Plot_Wjets"] == "Enable":
                    file6 = TFile.Open("../PlotFiles/" +
                                       histoFiles["Wjets"], "READ")
                    dir6 = file6.GetDirectory(
                        "Nominal").GetDirectory(HistoName)
                    h_W_background = dir6.Get(
                        "Wjets_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_W_background.SetLineColor(kRed)
                    if ReBin == True:
                        h_W_background.Rebin(2)
                    h_other_backgroundlist.append(h_W_background)

                if config["Plot_Zjets"] == "Enable":
                    file7 = TFile.Open("../PlotFiles/" +
                                       histoFiles["Zjets"], "READ")
                    dir7 = file7.GetDirectory(
                        "Nominal").GetDirectory(HistoName)
                    h_Z_background = dir7.Get(
                        "Zjets_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_Z_background.SetLineColor(kRed)
                    if ReBin == True:
                        h_Z_background.Rebin(2)
                    h_other_backgroundlist.append(h_Z_background)

                if config["Plot_diboson"] == "Enable":
                    file8 = TFile.Open("../PlotFiles/" +
                                       histoFiles["diboson"], "READ")
                    dir8 = file8.GetDirectory(
                        "Nominal").GetDirectory(HistoName)
                    h_diboson_background = dir8.Get(
                        "diboson_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_diboson_background.SetLineColor(kRed)
                    if ReBin == True:
                        h_diboson_background.Rebin(2)
                    h_other_backgroundlist.append(h_diboson_background)

                if config["Plot_singleTop"] == "Enable":
                    file9 = TFile.Open("../PlotFiles/" +
                                       histoFiles["singleTop"], "READ")
                    dir9 = file9.GetDirectory(
                        "Nominal").GetDirectory(HistoName)
                    h_singleTop_background = dir9.Get(
                        "singleTop_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
                    h_singleTop_background.SetLineColor(kRed)
                    if ReBin == True:
                        h_singleTop_background.Rebin(2)
                    h_other_backgroundlist.append(h_singleTop_background)

                h_other_background = 0

                if len(h_other_backgroundlist) > 0:
                    for i in h_other_backgroundlist:
                        if h_other_background == 0:
                            h_other_background = i
                        else:
                            h_other_background += i

                nbins = 20
                ymax = 0
                NormalizeHisto(h_other_background)
                if ymax < h_other_background.GetMaximum():
                    ymax = h_other_background.GetMaximum()

                if config["Plot_ttbar"] == "Enable":
                    NormalizeHisto(h_ttbar_background)
                    if ymax < h_ttbar_background.GetMaximum():
                        ymax = h_ttbar_background.GetMaximum()
                elif config["Plot_ttbarSherpa"] == "Enable":
                    NormalizeHisto(h_ttbarSherpa_background)
                    if ymax < h_ttbarSherpa_background.GetMaximum():
                        ymax = h_ttbarSherpa_background.GetMaximum()

                if config["Plot_sig_Hplus_Wh_m400-0"] == "Enable":
                    NormalizeHisto(h_sig_Hplus_m400)
                    if ymax < h_sig_Hplus_m400.GetMaximum():
                        ymax = h_sig_Hplus_m400.GetMaximum()
                if config["Plot_sig_Hplus_Wh_m800-0"] == "Enable":
                    NormalizeHisto(h_sig_Hplus_m800)
                    if ymax < h_sig_Hplus_m800.GetMaximum():
                        ymax = h_sig_Hplus_m800.GetMaximum()
                if config["Plot_sig_Hplus_Wh_m1600-0"] == "Enable":
                    NormalizeHisto(h_sig_Hplus_m1600)
                    if ymax < h_sig_Hplus_m1600.GetMaximum():
                        ymax = h_sig_Hplus_m1600.GetMaximum()

                h_other_background.GetXaxis().SetTitle(Xaxis_label)
                h_other_background.GetYaxis().SetRangeUser(0.001, round(ymax*1.25, 3)+0.001)
                h_other_background.Draw("HIST")
                h_ttbar_background.Draw("HISTSAME")
                h_sig_Hplus_m400.Draw("HISTSAME")
                h_sig_Hplus_m800.Draw("HISTSAME")
                h_sig_Hplus_m1600.Draw("HISTSAME")

                leg = TLegend(leg_pl1, leg_pl2, leg_pl3, leg_pl4)
                atlas_lable = ATLAS_LABEL(0.19, 0.95)
                myText(test_pl1, test_pl2, 1, HistoName+" "+btagStrategy)
                leg.SetShadowColor(kWhite)
                leg.SetFillColor(kWhite)
                leg.SetLineColor(kBlack)

                if config["Plot_sig_Hplus_Wh_m400-0"] == "Enable":
                    leg.AddEntry(h_sig_Hplus_m400,
                                 "H^{+}#rightarrow hW^{+} (m_{H^{+}} = 400GeV)", "L")
                if config["Plot_sig_Hplus_Wh_m800-0"] == "Enable":
                    leg.AddEntry(h_sig_Hplus_m800,
                                 "H^{+}#rightarrow hW^{+} (m_{H^{+}} = 800GeV)", "L")
                if config["Plot_sig_Hplus_Wh_m1600-0"] == "Enable":
                    leg.AddEntry(h_sig_Hplus_m1600,
                                 "H^{+}#rightarrow hW^{+} (m_{H^{+}} = 1600GeV)", "L")

                if config["Plot_ttbar"] == "Enable":
                    leg.AddEntry(h_ttbar_background,  "t#bar{t}", "L")
                elif config["Plot_ttbarSherpa"] == "Enable":
                    leg.AddEntry(h_ttbarSherpa_background,
                                 "t#bar{t}Sherpa", "L")

                leg.AddEntry(h_other_background,  "other backgrounds", "L")
                leg.SetTextSize(0.0325)
                leg.Draw()
                c1.RedrawAxis()
                c1.Update()
                c1.RedrawAxis()
                c1.SaveAs(histoDir + "/ShapePlot_%s_lvbb.pdf" %
                          (HistoName + "_" + btagStrategy))
