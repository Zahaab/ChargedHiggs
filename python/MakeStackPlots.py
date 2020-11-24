# -*- coding: utf-8 -*-
# python
import sys
import glob
import math
import re
from ROOT import *
from array import *

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

# for HistoName in ["MET","METSig","nJets","Mwt","HT","HT_bjets","DeltaPhi_HW","mVH","Lepton_Pt","Lepton_Eta"]:
for HistoName in ["Mwt", "Lepton_Pt", "HT", "mVH"]:
    for Region in ["Resolved_LepP_SR", "Resolved_LepP_CR"]:
        for btagStrategy in ["TwoTags", "ThreeTags"]:

            ReBin = False
            YAxisScale = 1.4

            if "MET" in HistoName:
                Xaxis_label = "Missing Transverse Momentum [GeV]"
            elif "METSig" in HistoName:
                Xaxis_label = "E_{T}^{mis.} significance"
            elif "nJets" in HistoName:
                Xaxis_label = "Jet Multiplicity"
            elif "nBTags" in HistoName:
                Xaxis_label = "b-Tag Multiplicity"
            elif "Mwt" in HistoName:
                Xaxis_label = "Transverse W-boson Mass [GeV]"
            elif "mVH" in HistoName:
                Xaxis_label = "m_{Wh}[GeV]"
            elif "Lepton_Pt" in HistoName:
                Xaxis_label = "Lepton Transverse Momentum[GeV]"
            elif "HT" in HistoName:
                Xaxis_label = "Scalar Transverse Momentum Sum [GeV]"
            elif "HT_bjets" in HistoName:
                Xaxis_label = "Scalar Transverse Momentum Sum [GeV]"
            else:
                Xaxis_label = ""

            # correct problem in maker: wrong normalisation
            dscale = 1.223695
            escale = 1.61419497

            file1a = TFile.Open(
                "../PlotFiles/sig_Hplus_Wh_m400-0_77p_MC16a.root", "READ")
            file1d = TFile.Open(
                "../PlotFiles/sig_Hplus_Wh_m400-0_77p_MC16d.root", "READ")
            file1e = TFile.Open(
                "../PlotFiles/sig_Hplus_Wh_m400-0_77p_MC16e.root", "READ")
            dir1a = file1a.GetDirectory("Nominal").GetDirectory(HistoName)
            dir1d = file1d.GetDirectory("Nominal").GetDirectory(HistoName)
            dir1e = file1e.GetDirectory("Nominal").GetDirectory(HistoName)
            h_sig_Hplus_m400a = dir1a.Get(
                "sig_Hplus_Wh_m400-0_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
            h_sig_Hplus_m400d = dir1d.Get(
                "sig_Hplus_Wh_m400-0_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
            h_sig_Hplus_m400e = dir1e.Get(
                "sig_Hplus_Wh_m400-0_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
            h_sig_Hplus_m400d.Scale(dscale)
            h_sig_Hplus_m400e.Scale(escale)
            h_sig_Hplus_m400 = h_sig_Hplus_m400a+h_sig_Hplus_m400d+h_sig_Hplus_m400e
            h_sig_Hplus_m400.SetLineColor(kBlack)
            h_sig_Hplus_m400.SetLineStyle(7)
            if ReBin == True:
                h_sig_Hplus_m400.Rebin(2)

            file7a = TFile.Open(
                "../PlotFiles/sig_Hplus_Wh_m800-0_77p_MC16a.root", "READ")
            file7d = TFile.Open(
                "../PlotFiles/sig_Hplus_Wh_m800-0_77p_MC16d.root", "READ")
            file7e = TFile.Open(
                "../PlotFiles/sig_Hplus_Wh_m800-0_77p_MC16e.root", "READ")
            dir7a = file7a.GetDirectory("Nominal").GetDirectory(HistoName)
            dir7d = file7d.GetDirectory("Nominal").GetDirectory(HistoName)
            dir7e = file7e.GetDirectory("Nominal").GetDirectory(HistoName)
            h_sig_Hplus_m800a = dir7a.Get(
                "sig_Hplus_Wh_m800-0_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
            h_sig_Hplus_m800d = dir7d.Get(
                "sig_Hplus_Wh_m800-0_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
            h_sig_Hplus_m800e = dir7e.Get(
                "sig_Hplus_Wh_m800-0_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
            h_sig_Hplus_m800d.Scale(dscale)
            h_sig_Hplus_m800e.Scale(escale)
            h_sig_Hplus_m800 = h_sig_Hplus_m800a+h_sig_Hplus_m800d+h_sig_Hplus_m800e
            h_sig_Hplus_m800.SetLineColor(kBlue)
            h_sig_Hplus_m800.SetLineStyle(7)
            if ReBin == True:
                h_sig_Hplus_m800.Rebin(2)

            file8a = TFile.Open(
                "../PlotFiles/sig_Hplus_Wh_m1600-0_77p_MC16a.root", "READ")
            file8d = TFile.Open(
                "../PlotFiles/sig_Hplus_Wh_m1600-0_77p_MC16d.root", "READ")
            file8e = TFile.Open(
                "../PlotFiles/sig_Hplus_Wh_m1600-0_77p_MC16e.root", "READ")
            dir8a = file8a.GetDirectory("Nominal").GetDirectory(HistoName)
            dir8d = file8d.GetDirectory("Nominal").GetDirectory(HistoName)
            dir8e = file8e.GetDirectory("Nominal").GetDirectory(HistoName)
            h_sig_Hplus_m1600a = dir8a.Get(
                "sig_Hplus_Wh_m1600-0_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
            h_sig_Hplus_m1600d = dir8d.Get(
                "sig_Hplus_Wh_m1600-0_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
            h_sig_Hplus_m1600e = dir8e.Get(
                "sig_Hplus_Wh_m1600-0_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
            h_sig_Hplus_m1600d.Scale(dscale)
            h_sig_Hplus_m1600e.Scale(escale)
            h_sig_Hplus_m1600 = h_sig_Hplus_m1600a+h_sig_Hplus_m1600d+h_sig_Hplus_m1600e
            h_sig_Hplus_m1600.SetLineColor(kViolet)
            h_sig_Hplus_m1600.SetLineStyle(7)
            if ReBin == True:
                h_sig_Hplus_m1600.Rebin(2)

            file2a = TFile.Open(
                "../PlotFiles/ttbarSherpa_77p_MC16a.root", "READ")
            file2d = TFile.Open(
                "../PlotFiles/ttbarSherpa_77p_MC16d.root", "READ")
            file2e = TFile.Open(
                "../PlotFiles/ttbarSherpa_77p_MC16d.root", "READ")
            dir2a = file2a.GetDirectory("Nominal").GetDirectory(HistoName)
            dir2d = file2d.GetDirectory("Nominal").GetDirectory(HistoName)
            dir2e = file2e.GetDirectory("Nominal").GetDirectory(HistoName)
            h_ttbar_background_a = dir2a.Get(
                "ttbarSherpa_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
            h_ttbar_background_d = dir2d.Get(
                "ttbarSherpa_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
            h_ttbar_background_e = dir2e.Get(
                "ttbarSherpa_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
            h_ttbar_background_d.Scale(dscale)
            h_ttbar_background_e.Scale(escale)
            h_ttbar_background = h_ttbar_background_a + \
                h_ttbar_background_d+h_ttbar_background_e
            h_ttbar_background.SetLineColor(kGreen+3)
            if ReBin == True:
                h_ttbar_background.Rebin(2)

            file3a = TFile.Open("../PlotFiles/Wjets_77p_MC16a.root", "READ")
            file3d = TFile.Open("../PlotFiles/Wjets_77p_MC16d.root", "READ")
            file3e = TFile.Open("../PlotFiles/Wjets_77p_MC16e.root", "READ")
            dir3a = file3a.GetDirectory("Nominal").GetDirectory(HistoName)
            dir3d = file3d.GetDirectory("Nominal").GetDirectory(HistoName)
            dir3e = file3e.GetDirectory("Nominal").GetDirectory(HistoName)
            h_W_background_a = dir3a.Get(
                "Wjets_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
            h_W_background_d = dir3d.Get(
                "Wjets_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
            h_W_background_e = dir3e.Get(
                "Wjets_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
            h_W_background_d.Scale(dscale)
            h_W_background_e.Scale(escale)
            h_W_background = h_W_background_a+h_W_background_d+h_W_background_e
            h_W_background.SetLineColor(kRed-3)
            if ReBin == True:
                h_W_background.Rebin(2)

            file4a = TFile.Open("../PlotFiles/Zjets_77p_MC16a.root", "READ")
            file4d = TFile.Open("../PlotFiles/Zjets_77p_MC16d.root", "READ")
            file4e = TFile.Open("../PlotFiles/Zjets_77p_MC16e.root", "READ")
            dir4a = file4a.GetDirectory("Nominal").GetDirectory(HistoName)
            dir4d = file4d.GetDirectory("Nominal").GetDirectory(HistoName)
            dir4e = file4e.GetDirectory("Nominal").GetDirectory(HistoName)
            h_Z_background_a = dir4a.Get(
                "Zjets_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
            h_Z_background_d = dir4d.Get(
                "Zjets_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
            h_Z_background_e = dir4e.Get(
                "Zjets_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
            h_Z_background_d.Scale(dscale)
            h_Z_background_e.Scale(escale)
            h_Z_background = h_Z_background_a+h_Z_background_d+h_Z_background_e
            h_Z_background.SetLineColor(kRed-3)
            if ReBin == True:
                h_Z_background.Rebin(2)

            file5a = TFile.Open("../PlotFiles/diboson_77p_MC16a.root", "READ")
            file5d = TFile.Open("../PlotFiles/diboson_77p_MC16d.root", "READ")
            file5e = TFile.Open("../PlotFiles/diboson_77p_MC16e.root", "READ")
            dir5a = file5a.GetDirectory("Nominal").GetDirectory(HistoName)
            dir5d = file5d.GetDirectory("Nominal").GetDirectory(HistoName)
            dir5e = file5e.GetDirectory("Nominal").GetDirectory(HistoName)
            h_diboson_background_a = dir5a.Get(
                "diboson_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
            h_diboson_background_d = dir5d.Get(
                "diboson_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
            h_diboson_background_e = dir5e.Get(
                "diboson_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
            h_diboson_background_d.Scale(dscale)
            h_diboson_background_e.Scale(escale)
            h_diboson_background = h_diboson_background_a + \
                h_diboson_background_d+h_diboson_background_e
            h_diboson_background.SetLineColor(kRed-3)
            if ReBin == True:
                h_diboson_background.Rebin(2)

            file6a = TFile.Open(
                "../PlotFiles/singleTop_77p_MC16a.root", "READ")
            file6d = TFile.Open(
                "../PlotFiles/singleTop_77p_MC16d.root", "READ")
            file6e = TFile.Open(
                "../PlotFiles/singleTop_77p_MC16e.root", "READ")
            dir6a = file6a.GetDirectory("Nominal").GetDirectory(HistoName)
            dir6d = file6d.GetDirectory("Nominal").GetDirectory(HistoName)
            dir6e = file6e.GetDirectory("Nominal").GetDirectory(HistoName)
            h_singleTop_background_a = dir6a.Get(
                "singleTop_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
            h_singleTop_background_d = dir6d.Get(
                "singleTop_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
            h_singleTop_background_e = dir6e.Get(
                "singleTop_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
            h_singleTop_background_d.Scale(dscale)
            h_singleTop_background_e.Scale(escale)
            h_singleTop_background = h_singleTop_background_a + \
                h_singleTop_background_d+h_singleTop_background_e
            h_singleTop_background.SetLineColor(kRed-3)
            if ReBin == True:
                h_singleTop_background.Rebin(2)

            h_other_background = h_singleTop_background + \
                h_diboson_background + h_W_background
            h_all_background = h_ttbar_background + h_other_background
            h_sig_Hplus_m400.Scale(5)
            h_sig_Hplus_m800.Scale(5)
            h_sig_Hplus_m1600.Scale(5)
            h_sig_Hplus_m400n = h_sig_Hplus_m400+h_all_background
            h_sig_Hplus_m800n = h_sig_Hplus_m800+h_all_background
            h_sig_Hplus_m1600n = h_sig_Hplus_m1600+h_all_background
            h_all_background.SetLineColor(1)
            h_all_background.SetFillColor(kGreen+3)
            h_other_background.SetLineColor(1)
            h_other_background.SetFillColor(kRed-3)
            h_sig_Hplus_m400n.SetNdivisions(8)
            h_sig_Hplus_m400n.SetXTitle(Xaxis_label)
            ymax = h_sig_Hplus_m400n.GetMaximum()
            h_sig_Hplus_m400n.GetYaxis().SetRangeUser(0.001, ymax*1.3)

            nbins = 20
            # ymax=0
            # ymax=h_sig_Hplus_m400n.GetMaximum()
            # NormalizeHisto(h_other_background)
            # if ymax<h_other_background.GetMaximum():
            #     ymax=h_other_background.GetMaximum()
            # NormalizeHisto(h_ttbar_background)
            # if ymax<h_ttbar_background.GetMaximum():
            #     ymax=h_ttbar_background.GetMaximum()
            # NormalizeHisto(h_sig_Hplus_m400)
            # if ymax<h_sig_Hplus_m400.GetMaximum():
            #     ymax=h_sig_Hplus_m400.GetMaximum()
            # NormalizeHisto(h_sig_Hplus_m800)
            # if ymax<h_sig_Hplus_m800.GetMaximum():
            #     ymax=h_sig_Hplus_m800.GetMaximum()
            # NormalizeHisto(h_sig_Hplus_m1600)
            # if ymax<h_sig_Hplus_m1600.GetMaximum():
            #     ymax=h_sig_Hplus_m1600.GetMaximum()

            h_sig_Hplus_m400n.Draw("HIST")
            h_all_background.Draw("HISTSAME")
            h_other_background.Draw("HISTSAME")
            h_sig_Hplus_m400n.Draw("HISTSAME")
            h_sig_Hplus_m800n.Draw("HISTSAME")
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

            leg.AddEntry(h_sig_Hplus_m400,
                         "H^{+}#rightarrow hW^{+} (m_{H^{+}}=400GeV) x5", "L")
            leg.AddEntry(h_sig_Hplus_m800,
                         "H^{+}#rightarrow hW^{+} (m_{H^{+}}=800GeV) x5", "L")
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
            c1.SaveAs("../Plots/ShapePlot_%s_lvbb.pdf" %
                      (HistoName+"_"+Region+"_"+btagStrategy))
