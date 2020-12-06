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
#include "utilis/configparser.h"

int main(int argc, char **argv)
{
  clock_t begin = clock();
  // Argv means the  parameters being passed into the executable,
  // E.G ./execute "data/MC16a" "ttbarSherpa.root" "77p"  "."  0
  TApplication theApp("evsel", &argc, argv);
  auto config = parseConfig(theApp.Argv(1));
  TString path = config["path"];
  TString SampleName = config["SampleName"];
  TString WP = config["WP"];
  TString OUTPUTDIR = config["OUTPUTDIR"];
  bool batchMode = atoi(config["batchMode"].c_str());
  // // Argv(5) is a number 0 or 1 stored as a string, atoi converts
  // // a string into an int. Here it's then assigned to a bool
  // // 0 is false and 1 is true.
  // Float_t hmlb = stof(theApp.Argv(6));
  // Float_t hmub = stof(theApp.Argv(7));
  // Float_t wmlb = stof(theApp.Argv(8));
  // Float_t wmub = stof(theApp.Argv(9));
  // Float_t met_ptv = stof(theApp.Argv(10));
  // Float_t lep_ptv = stof(theApp.Argv(11));
  // Float_t jet0_ptv = stof(theApp.Argv(12));
  // Float_t jet1_ptv = stof(theApp.Argv(13));
  // Float_t lep_jet0_angle = stof(theApp.Argv(14));
  // Float_t lep_jet1_angle = stof(theApp.Argv(15));
  // Float_t hw_angle = stof(theApp.Argv(16));
  // Float_t solo_jet_ptv = stof(theApp.Argv(17));
  // Argv(6) to Argv(17) are the 12 variables we are changing, they are always written in this order.
  TString OutFileName = SampleName;
  TString MCDataPeriode = "";
  // This is where we initialise TreeNames as an empty vector of
  // strings.
  std::vector<std::string> TreeNames;

  TreeNames.push_back("Nominal");
  if (path.Contains("MC16a"))
    MCDataPeriode = "MC16a";
  if (path.Contains("MC16d"))
    MCDataPeriode = "MC16d";
  if (path.Contains("MC16e"))
    MCDataPeriode = "MC16e";
  // This creates a file using event data changing the end of sample name.
  // The naming convention here is the name of the input data + WP + data period + the variation.
  OutFileName.ReplaceAll(".root", "_" + WP + "_" + MCDataPeriode + "_" + config["Higgs_mass_lower_bound"] + "-" + config["Higgs_mass_upper_bound"] + "-" +
                                      config["Wboson_mass_lower_bound"] + "-" + config["Wboson_mass_upper_bound"] + "-" + config["Missing_transverse_momentum"] + "-" +
                                      config["Lepton_transverse_momentum"] + "-" + config["2Jets_Jet1_transverse_momentum"] + "-" +
                                      config["2Jets_Jet2_transverse_momentum"] + "-" + config["2Jets_Jet1_lepton_angle"] + "-" + config["2Jets_Jet2_lepton_angle"] + "-" +
                                      config["Higgs_Wboson_angle"] + "-" + config["1Jet_Jet_transverse_momentum"] + ".root");
  if (!batchMode)
  {
    OutFileName = OUTPUTDIR + "/PlotFiles/" + OutFileName;
  }
  TFile *outfile = TFile::Open(OutFileName, "RECREATE");
  for (unsigned int i = 0; i < TreeNames.size(); i++)
  {
    // This is where TreeNames.at(i) = TreeNames[i]
    TString TreeName = TString(TreeNames.at(i));
    TChain *mych_data = new TChain(TreeName);
    // This adds the absolute path of the sampleName file to
    // the Tchain
    mych_data->Add(OUTPUTDIR + "/" + path + "/" + SampleName);
    // This prints GetEntries from the Tchain to the terminal
    std::cout << mych_data->GetEntries() << "  " << path + "/" + SampleName << std::endl;
    EventLoop *eventLoop = new EventLoop(mych_data, TreeName, config);
    eventLoop->Loop();
    std::string my_dir = TreeNames.at(i);
    TDirectory *subdir = outfile->mkdir(my_dir.c_str());
    eventLoop->Write(subdir, TreeNames.at(i));
    delete mych_data;
    delete eventLoop;
  }

  std::cout << "Finished looping over the events" << std::endl;
  outfile->Close();
  return 0;
}
