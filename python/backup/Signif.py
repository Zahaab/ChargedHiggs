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
y_axis_label="S/#sqrt(B)"
#############################
btagStrategy = "FourPlusTags"
btagStrategy = "ThreeTags"
btagStrategy = "Incl"
btagStrategy = "TwoTags"
Region       = "Resolved_SR"
############################

def SignificanceFunction2(s,b,rel_unc):
    n=s+b
    sigma=n*rel_unc
    print n,b,s,sigma
    #print n*math.log((n*(b+(sigma**2)))/((b**2)+n*(sigma**2)))
    #print(b**2)/(sigma**2)*math.log(1+((sigma**2)*(n-b))/(b*(b+(sigma**2))))
    if s<=0 or b<=0 :
        print("ERROR signal or background events is Zero!")
        return -1
    else:
        if b>=s:
            try:
                Z=math.sqrt(2*(n*math.log((n*(b+(sigma**2)))/((b**2)+n*(sigma**2)))-(b**2)/(sigma**2)*math.log(1+(((sigma**2)*(n-b))/(b*(b+(sigma**2)))))))
            except:
                Z=0
        else:
            Z=-1
            print "this is at n<b"
        return Z
        

def Loop():
    
    #for HistoName in ["MET","maxMVAResponse","pTH","METSig","nJets","Lepton_Pt","nBtagCategory","ntagsOutside","mH","DeltaPhi_HW","nBTags"]:
    #HistoName="MET"
    for HistoName in ["maxMVAResponse"]:
    #for HistoName in ["DeltaPhi_HW"]:

        c1=TCanvas("c1","",1200,900)                
        pad1=TPad()
        pad2=TPad()
        pad1.SetCanvas(c1)
        pad2.SetCanvas(c1)
        pad1.SetCanvasSize(1200,900)
        pad2.SetCanvasSize(1200,900)
        pad1.SetLeftMargin(0.15)
        pad2.SetLeftMargin(0.15)
        pad2.SetRightMargin(0.13)
        pad1.SetRightMargin(0.13)
        
        pad2.SetFillStyle(4000)
        pad2.SetFrameFillStyle(0)
        bin_breite=0

        file1=TFile.Open("../PlotFiles/ForOptimisation/sig_Hplus_Wh_m800-0.root","READ")
        dir1=file1.GetDirectory("Nominal").GetDirectory(HistoName)
        h_signalHisto_800=dir1.Get("sig_Hplus_Wh_m800-0_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
        
        file6=TFile.Open("../PlotFiles/ForOptimisation/sig_Hplus_Wh_m400-0.root","READ")
        dir6=file6.GetDirectory("Nominal").GetDirectory(HistoName)
        h_signalHisto_400=dir6.Get("sig_Hplus_Wh_m400-0_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
        
        file7=TFile.Open("../PlotFiles/ForOptimisation/sig_Hplus_Wh_m1600-0.root","READ")
        dir7=file7.GetDirectory("Nominal").GetDirectory(HistoName)
        h_signalHisto_1600=dir7.Get("sig_Hplus_Wh_m1600-0_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
        
        file5=TFile.Open("../PlotFiles/ForOptimisation/ttbar.root","READ")
        dir5=file5.GetDirectory("Nominal").GetDirectory(HistoName)
        h_backgHisto_t=dir5.Get("ttbar_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
        
        file2=TFile.Open("../PlotFiles/ForOptimisation/Wjets.root","READ")
        dir2=file2.GetDirectory("Nominal").GetDirectory(HistoName)
        h_backgHisto_W=dir2.Get("Wjets_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
        
        file3=TFile.Open("../PlotFiles/ForOptimisation/singleTop.root","READ")
        dir3=file3.GetDirectory("Nominal").GetDirectory(HistoName)
        h_backgHisto_single=dir3.Get("singleTop_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
        
        file4=TFile.Open("../PlotFiles/ForOptimisation/diboson.root","READ")
        dir4=file4.GetDirectory("Nominal").GetDirectory(HistoName)
        h_backgHisto_diboson=dir4.Get("diboson_"+HistoName+"_"+Region+"_"+btagStrategy+"_Nominal")
            
        h_backgHisto=h_backgHisto_t+h_backgHisto_W+h_backgHisto_single+h_backgHisto_diboson
        
        print h_signalHisto_400.Integral()/math.sqrt(h_backgHisto.Integral())

        x=array('d')
        y_800=array('d')
        y_400=array('d')
        y_1600=array('d')
        y_backg=array('d')
        z=array('d')
        z_800=array('d')
        z_400=array('d')
        z_400_5=array('d')
        z_400_25=array('d')
        z_400_10=array('d')
        z_1600=array('d')
        y=array('d')
        z_5=array('d')
        z_25=array('d')
        z_10=array('d')
        #x_bin_size=h_signalHisto_400.GetXaxis().GetXmax()/h_signalHisto_400.GetNbinsX()
        x_bin_size=h_signalHisto_400.GetBinWidth(2)
        
        for i in range(1,h_signalHisto_400.GetNbinsX()+1):
           
            h_signalHisto=h_signalHisto_400
            bin_breite=h_signalHisto.GetBinWidth(2)
            print (bin_breite-x_bin_size)
            
            n_sig=GetNumberOfEvents(i,h_signalHisto)
            n_backg=GetNumberOfEvents(i,h_backgHisto)
            if n_backg==0:
                continue
            x.append(h_signalHisto.GetBinCenter(i))
           # n_sig_800=GetNumberOfEvents(i,h_signalHisto_800)
           # n_sig_400=GetNumberOfEvents(i,h_signalHisto_1600)
           # n_sig_1600=GetNumberOfEvents(i,h_signalHisto_1600)
            
            #y_800.append((GetNumberOfEvents(i,h_signalHisto_1600)/math.sqrt(n_backg)))
            #y_400.append((GetNumberOfEvents(i,h_signalHisto_1600)/math.sqrt(n_backg)))
            #y_1600.append((GetNumberOfEvents(i,h_signalHisto_1600)/math.sqrt(n_backg)))
            #z_400.append(SignificanceFunction2(n_sig_800,n_backg,0.05))
            #z_400_5.append(SignificanceFunction2(n_sig_1600,n_backg,0.05))
            #z_400_25.append(SignificanceFunction2(n_sig_1600,n_backg,0.025))
            #z_400_10.append(SignificanceFunction2(n_sig_1600,n_backg,0.1))
            y.append(((n_sig)/math.sqrt(n_backg)))
            z_5.append(SignificanceFunction2(n_sig,n_backg,0.05))
            z_25.append(SignificanceFunction2(n_sig,n_backg,0.025))
            z_10.append(SignificanceFunction2(n_sig,n_backg,0.1))
            
            #z_800.append(SignificanceFunction2(n_sig_800,n_backg,0.05))
            #z_1600.append(SignificanceFunction2(n_sig_1600,n_backg,0.05))
            
          #  z.append(SignificanceFunction2(n_sig,n_backg,0.05))
         #   x_single.append(n_sig/math.sqrt(GetNumberOfEvents(i,h_backgHisto_single)))
          #  x_di.append(n_sig/math.sqrt(GetNumberOfEvents(i,h_backgHisto_diboson)))
           # x_W.append(n_sig/math.sqrt(GetNumberOfEvents(i,h_backgHisto_W)))
           # z_single.append(SignificanceFunction2(n_sig,GetNumberOfEvents(i,h_backgHisto_single),0.05))
            #z_W.append(SignificanceFunction2(n_sig,GetNumberOfEvents(i,h_backgHisto_W),0.05))
            #z_di.append(SignificanceFunction2(n_sig,GetNumberOfEvents(i,h_backgHisto_diboson),0.05))
        
        #graph_800_z=TGraph(len(x),x,z_800)
        #graph_400_z=TGraph(len(x),x,z_400)
        #graph_1600_z=TGraph(len(x),x,z_1600)
        #graph_800_sq=TGraph(len(x),x,y_800)
        graph_400_sq=TGraph(len(x),x,y)
        #graph_1600_sq=TGraph(len(x),x,y_1600)
        graph_400_25_z=TGraph(len(x),x,z_25)
        graph_400_5_z=TGraph(len(x),x,z_5)
        graph_400_10_z=TGraph(len(x),x,z_10)
        #graph_W=TGraph(len(x),x,z_W)
        #graph_single=TGraph(len(x),x,z_single)
        #graph_di=TGraph(len(x),x,z_di)
          #  print "GetMaximun:" 
           # print h_signalHisto.GetXaxis().GetXmax()
       # graph_z=TGraph(len(x),x,z_5)
        #graph_sq=TGraph(len(x),x,y)

           
        #c1.Divide(1,2,0,0)
        #c1.cd(1)
       # graph_1600_z.GetXaxis().SetTitle(HistoName)
       # graph_1600_z.GetYaxis().SetTitle("Z")
       # graph_1600_z.SetMarkerColor(kBlue)
       # graph_800_z.SetMarkerColor(kRed)
        #graph_400_z.SetMarkerColor(kGreen)

        #graph_1600_sq.SetMarkerColor(kBlue)
        #graph_800_sq.SetMarkerColor(kRed)
        graph_400_sq.SetMarkerColor(kBlack)
        graph_400_sq.GetXaxis().SetTitle("Lowerbound on:"+HistoName)
        graph_400_sq.GetYaxis().SetTitle("s/#sqrt{b}")
        graph_400_sq.GetYaxis().CenterTitle()
       
        graph_400_25_z.SetMarkerStyle(4)
        graph_400_25_z.GetYaxis().SetTitle("z")
        graph_400_25_z.GetYaxis().CenterTitle()
        graph_400_25_z.GetYaxis().SetLimits(-0.05,1)
        graph_400_5_z.SetMarkerStyle(25)
        graph_400_10_z.SetMarkerStyle(26)
        graph_400_sq.SetMarkerStyle(3)
        graph_400_5_z.SetMarkerColor(kBlue)
        graph_400_10_z.SetMarkerColor(kRed)
        graph_400_25_z.SetMarkerColor(kGreen)
    
        
       # graph_1600_z.Draw("AP")
       # graph_400_z.Draw("P")
       # graph_800_z.Draw("P")
        #c1.cd(2)
        
        pad1.Draw()
        pad1.cd()
        graph_400_sq.Draw("AP")
        #graph_800_sq.Draw("P")
        #graph_1600_sq.Draw("P")
        
        pad2.Draw()
        pad2.cd()
        graph_400_25_z.Draw("APY+")
        graph_400_10_z.Draw("P")
        graph_400_5_z.Draw("P")
        
        leg=TLegend(0.675,0.7,0.85,0.95)
        #leg=TLegend(0.175,0.7,0.35,0.95)
        leg.SetHeader("m=400GeV","C")
        leg.SetTextAlign(12)
        leg.AddEntry(graph_400_25_z,"z_{ 2.5%}","P")
        leg.AddEntry(graph_400_5_z,"z_{5%}","P")
        leg.AddEntry(graph_400_10_z,"z_{10%}","P")
        leg.AddEntry(graph_400_sq,"s/#sqrt{b}","P")
        
        leg.Draw()

        print x 
            

           # graphZ.Draw("ACP")
        c1.Update()
        c1.SaveAs("../Plots/Sig_Plots/m400/Combined_m400_test_%s.pdf"% (HistoName))
        pad1.Close()
        pad2.Close()
        c1.Close()
        
        
        max_sq=GetMaximumX(x,y)
        max_5=GetMaximumX(x,z_5)
        max_25=GetMaximumX(x,z_25)
        max_10=GetMaximumX(x,z_10)
        f=open("../max_z/max_m400.txt","a")
        f.write(HistoName+";"+str(max_sq)+";"+str(max_25)+";"+str(max_5)+";"+str(max_10)+";"+str(bin_breite)+"\n")
        f.close()

       
        


def GetNumberOfEvents(lowerBound,histo):
  #  x_lowerbound=histo.FindBin(lowerBound)
    x_lowerbound=lowerBound
    x_upperbound=histo.GetNbinsX()
    if x_lowerbound<1:
        return;
    n=histo.Integral(x_lowerbound,x_upperbound)
    return n

def GetNumberOfEventsRevers(upperBound,histo):
    x_lowerbound=1
    x_upperbound=upperBound
    if x_lowerbound<1:
        return;
    n=histo.Integral(x_lowerbound,x_upperbound)
    return n


def GetMaximumX(x,y):
    maximum=0
    x_maximum=0
    for i in range(0,len(x)):
        if y[i]>maximum:
            maximum=y[i]
            x_maximum=x[i]
    return x_maximum


Loop()
 
        



