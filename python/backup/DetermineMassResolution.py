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

y_axis_label="Events"

c_blue   = TColor.GetColor("#3366ff")
c_red    = TColor.GetColor("#ee3311")
c_orange = TColor.GetColor("#ff9900")

def NormalizeHisto(histo):
     n_events=histo.Integral(-1,histo.GetNbinsX()+1)
     if n_events == 0:
         return
     print n_events, histo.Integral(histo.GetNbinsX(),histo.GetNbinsX()+1)
     ##### histo.Scale(1./n_events)
     histo.SetLineWidth(2)
     histo.SetStats(0)
     histo.SetFillStyle(3001)
     histo.SetMarkerColor(histo.GetLineColor())
     histo.SetMarkerSize(0.0)
     histo.GetXaxis().SetTitleOffset(1.2)
     histo.GetYaxis().SetTitleOffset(1.52)
     histo.GetXaxis().SetLabelSize(0.04)
     histo.GetYaxis().SetLabelSize(0.04)
     histo.GetXaxis().SetTitleSize(0.035)
     histo.GetYaxis().SetTitleSize(0.035)
     histo.GetXaxis().SetTitleOffset(1.85)
     histo.GetYaxis().SetTitleOffset(2.05)
     histo.GetYaxis().SetNdivisions(504)
     histo.GetXaxis().SetNdivisions(504)

c1 = TCanvas("ShapePlots","",720,720)
for fileName in ["sig_Hplus_Wh_m400","sig_Hplus_Wh_m800","sig_Hplus_Wh_m1600"]:
  #### [0]*exp(-0.5*((x-[1])/[2])**2) 
  gaussian_tf1 = TF1("gaussian_tf1","gaus(0)",-1,1)
  sigPars      = array( 'd', [0.0]*3)
  for HistoName in ["mass_resolution"]:
    for Region in ["Resolved_SR"]:
    ##  for bTagStrategy in ["Incl","FourPlusTags","ThreeTags","TwoTags"]: 
      for bTagStrategy in ["Incl"]:
         ReBin = False
         YAxisScale = 1.4
         Xaxis_label = "#frac{m^{reco}_{W^{+}h}-m^{truth}_{W^{+}h}}{m^{truth}_{W^{+}h}}"
         file1       = TFile.Open("../PlotFiles/MassResolution/"+fileName+"-0_70p.root","READ")
         dir1        = file1.GetDirectory("Nominal").GetDirectory(HistoName)
         h_sig_Hplus = dir1.Get(fileName+"-0_"+HistoName+"_"+Region+"_"+bTagStrategy+"_Nominal")
         h_sig_Hplus.SetLineColor(kBlack)
         h_sig_Hplus.SetLineStyle(1)
              
         nbins=20
         ymax=0
         NormalizeHisto(h_sig_Hplus)
         if ymax<h_sig_Hplus.GetMaximum():
            ymax=h_sig_Hplus.GetMaximum()
         h_sig_Hplus.Draw("HIST")
         MassPoint="" 
         if "400" in fileName:
             MassPoint = "400GeV"     
         if "800" in fileName:
             MassPoint = "800GeV"
       	 if "1600" in fileName:
       	     MassPoint = "1600GeV"

         leg = TLegend(0.7,0.65,0.925,0.855)
         ATLAS_LABEL(0.20,0.885," Simulation Internal",1,0.19);
         myText(0.785,0.825,1,"139 fb^{-1}")
         myText(0.20,0.825,1,"m_{W^{+}h} = "+MassPoint)
         leg.SetShadowColor(kWhite)
         leg.SetFillColor(kWhite)
         leg.SetLineColor(kWhite)
         ##leg.AddEntry(h_sig_Hplus_m800,  "H^{+}#rightarrow hW^{+} (m_{H^{+}} = 800GeV)","L")
         #leg.Draw()

         h_sig_Hplus.GetYaxis().SetTitle(y_axis_label)
         h_sig_Hplus.GetXaxis().SetTitle(Xaxis_label)
         h_sig_Hplus.GetYaxis().SetRangeUser(0.001,round(ymax*1.4,3)+0.001)
      
         fitStatus =  h_sig_Hplus.Fit("gaussian_tf1", "QW", "", -1, 1)
         myfunc2   =  h_sig_Hplus.GetFunction("gaussian_tf1")
         myfunc2.GetParameters(sigPars);
         myfunc2.SetLineColor(kBlue)
         myfunc2.SetLineWidth(3)
         myfunc2.SetLineStyle(7)
         myfunc2.Draw("SAMEL")
         print "1: ",sigPars[0] ,"2:",sigPars[1],"3:", sigPars[2]         
         myText(0.20,0.765,1,"#sigma_{res} = "+ str(round(sigPars[2],2))+"%")

         c1.RedrawAxis()
         c1.Update()
         c1.RedrawAxis()
         c1.SaveAs("../Plots/MassResolution_%s.pdf" % (HistoName+"_"+MassPoint))
