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
  TApplication theApp("evsel", &argc, argv);
  auto config = parseConfig(theApp.Argv(1));
  TString path;
  TString MCDataPeriode;
  TString SampleName = config["SampleName"];
  TString WP = config["WP"];
  TString OUTPUTDIR = config["OUTPUTDIR"];
  bool batchMode = atoi(config["batchMode"].c_str());
  TString OutFileName = SampleName;
  // This is where we initialise TreeNames as an empty vector of
  // strings.
  std::vector<std::string> TreeNames;
  TreeNames.push_back("Nominal");

  std::string stdpath = config["path"];
  auto MCDataPeriodes = parseDataPeriodes(config);
  auto index = stdpath.find("MC16");
  if (index == std::string::npos)
  {
    throw std::runtime_error(std::string("Error: not in path"));
  }

  for (auto stdMCDataPeriode : MCDataPeriodes)
  {
    path = TString(stdpath.replace(index, 5, stdMCDataPeriode));
    MCDataPeriode = TString(stdMCDataPeriode);
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
  }
  return 0;
}
