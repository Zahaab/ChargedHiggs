# -*- coding: utf-8 -*-
# python
import sys
import glob
import math
import re
import os
from ROOT import *
from array import *


_, hmlb, hmub, wmlb, wmub = sys.argv


def getChosenFiles(chosenFiles, path, hmlb, hmub, wmlb, wmub):
    varNums = path.split("_")[-1].replace(".root", "")
    var1, var2, var3, var4 = varNums.split("-")
    if hmlb in var1 and hmub in var2 and wmlb in var3 and wmub in var4:
        for key in chosenFiles:
            if key in path:
                chosenFiles[key] = path


def getDataFiles(hmlb, hmub, wmlb, wmub):
    chosenFiles = {"sig_Hplus_Wh_m400-0": 0,
                   "sig_Hplus_Wh_m800-0": 0,
                   "sig_Hplus_Wh_m1600-0": 0,
                   "ttbarSherpa": 0,
                   "Wjets": 0,
                   "diboson": 0,
                   "singleTop": 0}
    arr = os.listdir("../PlotFiles")
    for i in arr:
        getChosenFiles(chosenFiles, i, hmlb, hmub, wmlb, wmub)

    for key in chosenFiles:
        if chosenFiles[key] == 0:
            raise Exception("all files not found" + key)
    return chosenFiles


files = getDataFiles(hmlb, hmub, wmlb, wmub)


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

# for HistoName in ["Mwt"]:
for HistoName in ["MET", "METSig", "nJets", "Mwt", "HT", "HT_bjets", "DeltaPhi_HW", "mVH", "Lepton_Pt", "Lepton_Eta"]:
    for Region in ["Merged_LepN_SR"]:
        # What is Incl in terms of BTagStrategy?
        for btagStrategy in ["FourPlusTags", "ThreeTags", "TwoTags"]:
            # for btagStrategy in ["TwoTags"]:
            print HistoName
            ReBin = False
            YAxisScale = 1.4

            if "MET" in HistoName:
                Xaxis_label = "Missing Transverse Momentum [GeV]"
            if "METSig" in HistoName:
                Xaxis_label = "E_{T}^{mis.} significance"
            if "nJets" in HistoName:
                Xaxis_label = "Jet Multiplicity"
            if "nBTags" in HistoName:
                Xaxis_label = "b-Tag Multiplicity"
            if "Mwt" in HistoName:
                Xaxis_label = "Transverse W-boson Mass [GeV]"
            if "HT_bjets" in HistoName:
                Xaxis_label = "Scalar Transverse Momentum Sum [GeV]"
            Xaxis_label = ""

            file1 = TFile.Open("../PlotFiles/" +
                               files["sig_Hplus_Wh_m400-0"], "READ")
            dir1 = file1.GetDirectory("Nominal").GetDirectory(HistoName)
            print(file1)
            print(dir1)
            h_sig_Hplus_m400 = dir1.Get(
                "sig_Hplus_Wh_m400-0_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
            h_sig_Hplus_m400.SetLineColor(kBlack)
            h_sig_Hplus_m400.SetLineStyle(7)
            if ReBin == True:
                h_sig_Hplus_m400.Rebin(2)

            file6 = TFile.Open("../PlotFiles/" +
                               files["sig_Hplus_Wh_m800-0"], "READ")
            dir6 = file6.GetDirectory("Nominal").GetDirectory(HistoName)
            h_sig_Hplus_m800 = dir6.Get(
                "sig_Hplus_Wh_m800-0_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
            h_sig_Hplus_m800.SetLineColor(kBlue)
            h_sig_Hplus_m800.SetLineStyle(3)
            if ReBin == True:
                h_sig_Hplus_m800.Rebin(2)

            file7 = TFile.Open("../PlotFiles/" +
                               files["sig_Hplus_Wh_m1600-0"], "READ")
            dir7 = file7.GetDirectory("Nominal").GetDirectory(HistoName)
            h_sig_Hplus_m1600 = dir7.Get(
                "sig_Hplus_Wh_m1600-0_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
            h_sig_Hplus_m1600.SetLineColor(kViolet)
            h_sig_Hplus_m1600.SetLineStyle(9)
            if ReBin == True:
                h_sig_Hplus_m1600.Rebin(2)

            #file2   = TFile.Open("../PlotFiles/ForOptimisation/ttbar.root","READ")
            file2 = TFile.Open("../PlotFiles/" + files["ttbarSherpa"], "READ")
            dir2 = file2.GetDirectory("Nominal").GetDirectory(HistoName)
            #h_ttbar_background = dir2.Get("ttbar_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
            h_ttbar_background = dir2.Get(
                "ttbarSherpa_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
            h_ttbar_background.SetLineColor(219)
            if ReBin == True:
                h_ttbar_background.Rebin(2)

            file3 = TFile.Open("../PlotFiles/" + files["Wjets"], "READ")
            dir3 = file3.GetDirectory("Nominal").GetDirectory(HistoName)
            h_W_background = dir3.Get(
                "Wjets_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
            h_W_background.SetLineColor(kRed)
            if ReBin == True:
                h_W_background.Rebin(2)

            file4 = TFile.Open("../PlotFiles/" + files["diboson"], "READ")
            dir4 = file4.GetDirectory("Nominal").GetDirectory(HistoName)
            h_diboson_background = dir4.Get(
                "diboson_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
            h_diboson_background.SetLineColor(kRed)
            if ReBin == True:
                h_diboson_background.Rebin(2)

            file5 = TFile.Open("../PlotFiles/" + files["singleTop"], "READ")
            dir5 = file5.GetDirectory("Nominal").GetDirectory(HistoName)
            h_singleTop_background = dir5.Get(
                "singleTop_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
            h_singleTop_background.SetLineColor(kRed)
            if ReBin == True:
                h_singleTop_background.Rebin(2)

            h_other_background = h_singleTop_background + \
                h_diboson_background + h_W_background

            nbins = 20
            ymax = 0
            NormalizeHisto(h_other_background)
            if ymax < h_other_background.GetMaximum():
                ymax = h_other_background.GetMaximum()
            NormalizeHisto(h_ttbar_background)
            if ymax < h_ttbar_background.GetMaximum():
                ymax = h_ttbar_background.GetMaximum()
            NormalizeHisto(h_sig_Hplus_m400)
            if ymax < h_sig_Hplus_m400.GetMaximum():
                ymax = h_sig_Hplus_m400.GetMaximum()
            NormalizeHisto(h_sig_Hplus_m800)
            if ymax < h_sig_Hplus_m800.GetMaximum():
                ymax = h_sig_Hplus_m800.GetMaximum()
            NormalizeHisto(h_sig_Hplus_m1600)
            if ymax < h_sig_Hplus_m1600.GetMaximum():
                ymax = h_sig_Hplus_m1600.GetMaximum()

            h_other_background.Draw("HIST")
            h_ttbar_background.Draw("HISTSAME")
            h_sig_Hplus_m400.Draw("HISTSAME")
            h_sig_Hplus_m800.Draw("HISTSAME")
            h_sig_Hplus_m1600.Draw("HISTSAME")

            if HistoName in "maxMVAResponse":
                leg = TLegend(0.2, 0.65, 0.725, 0.855)
            else:
                leg = TLegend(0.45, 0.65, 0.925, 0.855)
            ATLAS_LABEL(0.20, 0.885, " Simulation Internal", 1, 0.19)
            leg.SetShadowColor(kWhite)
            leg.SetFillColor(kWhite)
            leg.SetLineColor(kWhite)

            leg.AddEntry(h_sig_Hplus_m400,
                         "H^{+}#rightarrow hW^{+} (m_{H^{+}} = 400GeV)", "L")
            leg.AddEntry(h_sig_Hplus_m800,
                         "H^{+}#rightarrow hW^{+} (m_{H^{+}} = 800GeV)", "L")
            leg.AddEntry(h_sig_Hplus_m1600,
                         "H^{+}#rightarrow hW^{+} (m_{H^{+}} = 1600GeV)", "L")
            leg.AddEntry(h_ttbar_background,  "t#bar{t}", "L")
            leg.AddEntry(h_other_background,  "other backgrounds", "L")
            leg.SetTextSize(0.0325)
            leg.Draw()
            h_other_background.GetXaxis().SetTitle(Xaxis_label)
            h_other_background.GetYaxis().SetRangeUser(0.001, round(ymax*1.25, 3)+0.001)

            c1.RedrawAxis()
            c1.Update()
            c1.RedrawAxis()
            c1.SaveAs("../Plots/ShapePlot_%s_lvbb.pdf" % (HistoName +
                                                          "_"+btagStrategy+"_"+hmlb+"-"+hmub+"-"+wmlb+"-"+wmub))
