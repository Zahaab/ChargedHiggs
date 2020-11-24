#include "main/EventLoop.h"
#include "TApplication.h"
#include <TSystemDirectory.h>
#include <TList.h>
#include <TCollection.h>
#include <TChain.h>
#include <TFile.h>
#include <TH1F.h>
#include <TTree.h>
#include <TString.h>
#include <fstream>
#include <iostream>
#include <vector>
#include <string>
#include <ctime>

int main(int argc, char** argv){
  clock_t begin = clock();
  // Argv means the  parameters being passed into the executable, 
  // E.G ./execute "data/MC16a" "ttbarSherpa.root" "77p"  "."  0
  TApplication theApp("evsel", &argc, argv);
  TString path          =  theApp.Argv(1);
  TString SampleName    =  theApp.Argv(2);
  TString WP            =  theApp.Argv(3);
  TString OUTPUTDIR     =  theApp.Argv(4);
  // Argv(5) is a number 0 or 1 stored as a string, atoi converts
  // a string into an int. Here it's then assigned to a bool
  // 0 is false and 1 is true.
  bool    batchMode     =  atoi(theApp.Argv(5));
  Float_t hmlb          =  stof(theApp.Argv(6));
  Float_t hmub          =  stof(theApp.Argv(7));
  Float_t wmlb          =  stof(theApp.Argv(8));
  Float_t wmub          =  stof(theApp.Argv(9));
  TString OutFileName   =  SampleName;
  TString MCDataPeriode = "";
  // This is where we initialise TreeNames as an empty vector of 
  // strings.
  std::vector<std::string> TreeNames;

  TreeNames.push_back("Nominal");
  if(path.Contains("MC16a"))MCDataPeriode = "MC16a";
  if(path.Contains("MC16d"))MCDataPeriode = "MC16d";
  if(path.Contains("MC16e"))MCDataPeriode = "MC16e";
  // This creates a file using event data changing the end of 
  // sample name.
  OutFileName.ReplaceAll(".root", "_" +WP+ "_" +MCDataPeriode+ "_" +std::to_string(hmlb)+ "-" +std::to_string(hmub) + "-" +std::to_string(wmlb) + "-" +std::to_string(wmub)+ ".root");
  if(!batchMode){
      OutFileName = OUTPUTDIR+"/PlotFiles/"+OutFileName;
  }
  TFile* outfile = TFile::Open(OutFileName,"RECREATE");
  for(unsigned int i=0; i < TreeNames.size(); i++){
     // This is where TreeNames.at(i) = TreeNames[i]
     TString TreeName  = TString(TreeNames.at(i));
     TChain* mych_data = new TChain (TreeName);
     // This adds the absolute path of the sampleName file to 
     // the Tchain 
     mych_data->Add(OUTPUTDIR+"/"+path+"/"+SampleName);
     // This prints GetEntries from the Tchain to the terminal
     std::cout<<mych_data->GetEntries()<<"  "<<path+"/"+SampleName<<std::endl;
     EventLoop *eventLoop = new EventLoop(mych_data,SampleName,TreeName,WP,hmlb,hmub,wmlb,wmub);
     eventLoop->Loop();
     std::string my_dir = TreeNames.at(i);
     TDirectory* subdir = outfile->mkdir(my_dir.c_str());
     eventLoop->Write(subdir,TreeNames.at(i));
     delete mych_data;
     delete eventLoop;
  }

  std::cout<<"Finished looping over the events"<<std::endl;  
  outfile->Close();
  return 0;
}



