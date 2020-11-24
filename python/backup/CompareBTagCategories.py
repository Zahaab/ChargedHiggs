# -*- coding: utf-8 -*-
#python
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

def SignificanceFunction2(s,b,rel_unc):
    n     = s + b
    sigma = b*rel_unc
    if not (s > 0 and b > 0):
        print("ERROR signal or background events is ZERO!!!")
        return -1
    else:
	if n >= b:
            Z = math.sqrt(2*(n*math.log((n*(b+(sigma ** 2)))/((b ** 2) +n*(sigma ** 2))) - (b ** 2)/(sigma ** 2) *math.log(1+((sigma ** 2)*(n-b))/(b*(b+(sigma ** 2))))))
        else:
            Z = -1
            print("this is at n < b")
        return Z

def SignificanceFunction1(s,b):
    if (b > 0):
        return s/math.sqrt(b)
    else:
	return -1

def CalculateSignificanceValues(h_signal,h_bkg, Hmass, thisWP, Cat_label):
    latexList = []
    latexList.append(r"\begin{table}")
    latexList.append(r"\centering")
    latexList.append(r"\begin{tabular}{c| c c c c}")
    latexList.append(r"\hline")
    latexList.append(r"\hline")
    latexList.append(r""+ Cat_label +"& $S/\sqrt{B}$ & $z_{\sigma = 2.5\%}$ & $z_{\sigma = 5.0\%}$ & $z_{\sigma = 10\%}$ \\")
    latexList.append(r"\hline")
    n=h_signal.GetNbinsX()
    if "category" in Cat_label:
      n = n-1
    else:
      n = n
    SoversqrtB_total = 0
    Z02_total        = 0
    Z03_total        = 0
    Z04_total        = 0
    for i in range (1, n):
        SoversqrtB = round(SignificanceFunction1(h_signal.GetBinContent(i), h_bkg.GetBinContent(i)),2)
        Z02 = round(SignificanceFunction2(h_signal.GetBinContent(i), h_bkg.GetBinContent(i), 0.025),2)
        Z03 = round(SignificanceFunction2(h_signal.GetBinContent(i), h_bkg.GetBinContent(i), 0.05),2)
        Z04 = round(SignificanceFunction2(h_signal.GetBinContent(i), h_bkg.GetBinContent(i), 0.10),2)
        latexList.append(str(i) + " & " + str(SoversqrtB) + " & " + str(Z02) + " & " + str(Z03) + " & " + str(Z04) + r" \\" )
        SoversqrtB_total += SoversqrtB**2
        Z02_total        += Z02**2
        Z03_total        += Z03**2
        Z04_total        += Z04**2
    latexList.append(r"\hline")
    latexList.append(r"\hline")
    latexList.append(r"\end{tabular}")
    latexList.append(r"\caption{BTagCategories for" + " %s  and in '%s'}" % (Hmass, thisWP))
    latexList.append(r"\end{table}")
    print Hmass, thisWP, Cat_label, round(math.sqrt(SoversqrtB_total),2), round(math.sqrt(Z02_total),2), round(math.sqrt(Z03_total),2), round(math.sqrt(Z04_total),2)
    return latexList

def WriteTabularInLaTeX(latexFile,thisLatexList):
    for line in thisLatexList:
        latexFile.write(line + " \n")

def main():
  latexFile = open(r"../LatexOutput/latexSignificanceTables_resolved_wh_qqbb.tex", "w")    # initializing Latex document
  latexFile.write(r"\documentclass[a4paper,12pt]{article}" + " \n")
  latexFile.write(r"\begin{document}" + " \n")
  for HistoName in ["BtagCategory","nBTags"]:
    for bTagStrategy in ["Incl"]:
       for WP in ["60p","70p","77p","85p"]:

         DirName = HistoName

         file6       = TFile.Open("../PlotFiles/WP_"+WP+"_resolved/sig_Hplus_Wh_m400-0.root","READ")
         dir6        = file6.GetDirectory("Nominal").GetDirectory(DirName)
         h_sig_Hplus_m400 = dir6.Get("sig_Hplus_Wh_m400-0_"+HistoName+"_Resolved_SR_"+bTagStrategy+"_Nominal")
 
         file1       = TFile.Open("../PlotFiles/WP_"+WP+"_resolved/sig_Hplus_Wh_m800-0.root","READ")
         dir1        = file1.GetDirectory("Nominal").GetDirectory(DirName)
         h_sig_Hplus_m800 = dir1.Get("sig_Hplus_Wh_m800-0_"+HistoName+"_Resolved_SR_"+bTagStrategy+"_Nominal")

         file7       = TFile.Open("../PlotFiles/WP_"+WP+"_resolved/sig_Hplus_Wh_m1600-0.root","READ")
         dir7        = file7.GetDirectory("Nominal").GetDirectory(DirName)
         h_sig_Hplus_m1600 = dir7.Get("sig_Hplus_Wh_m1600-0_"+HistoName+"_Resolved_SR_"+bTagStrategy+"_Nominal")
       
         file2   = TFile.Open("../PlotFiles/WP_"+WP+"_resolved/ttbar.root","READ")
         dir2    = file2.GetDirectory("Nominal").GetDirectory(DirName)
         h_ttbar_background = dir2.Get("ttbar_"+HistoName+"_Resolved_SR_"+bTagStrategy+"_Nominal")

         file3   = TFile.Open("../PlotFiles/WP_"+WP+"_resolved/Wjets.root","READ")
         dir3    = file3.GetDirectory("Nominal").GetDirectory(DirName)
         h_W_background = dir3.Get("Wjets_"+HistoName+"_Resolved_SR_"+bTagStrategy+"_Nominal")

         file4   = TFile.Open("../PlotFiles/WP_"+WP+"_resolved/diboson.root","READ")
         dir4    = file4.GetDirectory("Nominal").GetDirectory(DirName)
         h_diboson_background = dir4.Get("diboson_"+HistoName+"_Resolved_SR_"+bTagStrategy+"_Nominal")

         file5   = TFile.Open("../PlotFiles/WP_"+WP+"_resolved/singleTop.root","READ")
         dir5    = file5.GetDirectory("Nominal").GetDirectory(DirName)
         h_singleTop = dir5.Get("singleTop_"+HistoName+"_Resolved_SR_"+bTagStrategy+"_Nominal")

         h_total_bkg = h_ttbar_background.Clone()
         h_total_bkg.Add(h_W_background)
         h_total_bkg.Add(h_diboson_background)
         h_total_bkg.Add(h_singleTop)
     
         Cat_label = ""
         if "BtagCategory" in HistoName:
             Cat_label = "BTag category"
         elif "nBTags" in HistoName:
             Cat_label = "BTag multiplicity"

         latexTabm400 = CalculateSignificanceValues(h_sig_Hplus_m400, h_total_bkg, "m=400GeV", WP, Cat_label)
       	 WriteTabularInLaTeX(latexFile,latexTabm400)
         latexTabm800 = CalculateSignificanceValues(h_sig_Hplus_m800, h_total_bkg, "m=800GeV", WP, Cat_label)
         WriteTabularInLaTeX(latexFile,latexTabm800)
         latexTabm1600 = CalculateSignificanceValues(h_sig_Hplus_m1600, h_total_bkg, "m=1600GeV", WP, Cat_label)
         WriteTabularInLaTeX(latexFile,latexTabm1600)


  latexFile.write(r"\end{document}")    # End of Latex document


main()
