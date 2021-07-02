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
  //clock_t begin = clock();
  TApplication theApp("evsel", &argc, argv);
  auto config = parseConfig(theApp.Argv(1));
  TString path;
  TString MCDataPeriode;
  TString SampleName = config["SampleName"];
  TString WP = config["WP"];
  TString OUTPUTDIR = config["OUTPUTDIR"];
  int EventReadout = stoi(config["EventReadout"]);
  bool batchMode = atoi(config["batchMode"].c_str());
  Long64_t minEvent = stoi(config["MinimumEvent"]);
  Long64_t maxEvent = stoi(config["MaximumEvent"]);
  std::string file_number = config["Partition"];
  TString TreeName = TString("Nominal");

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
    TString OutFileName = SampleName;
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
    std::string file_extention = +"_" + file_number + ".root";
    std::string ex_OutFileName = std::string(OutFileName);
    ex_OutFileName.replace(ex_OutFileName.end() - 5, ex_OutFileName.end(), file_extention);

    TFile *outfile = TFile::Open(ex_OutFileName.c_str(), "RECREATE");
    TChain *mych_data = new TChain(TreeName);
    mych_data->Add(path + "/" + SampleName);
    Long64_t nentries = mych_data->GetEntries();
    std::cout << "\n"
              << nentries << "  " << path + "/" + SampleName << "\n";
              
    EventLoop *eventLoop = new EventLoop(mych_data, TreeName, ex_OutFileName, config);
    if (mych_data == 0)
      continue;

    Long64_t nbytes = 0, nb = 0;

    if (minEvent == 0 && maxEvent == 0)
    {
      minEvent = 0;
      maxEvent = nentries;
    }
    else if (maxEvent > nentries)
    {
      maxEvent = nentries;
    }

    std::cout << "Start Event : " << minEvent << "\n"
              << "End Event : " << maxEvent << "\n";

    for (Long64_t jentry = minEvent; jentry < maxEvent; jentry++)
    {
      Long64_t ientry = eventLoop->LoadTree(jentry);

      if (ientry < 0 || !mych_data)
        break;

      nb = mych_data->GetEntry(jentry);
      nbytes += nb;
      if (EventReadout != 0)
      {
        if (jentry % EventReadout == 0)
        {
          std::cout << "Processing " << jentry << " events!!!"
                    << "\n";
          std::cout << "Data : " << nbytes << " Bytes"
                    << "\n"
                    << "Data : " << nbytes * 0.000000001 << " Gigabytes"
                    << "\n";
        }
      }

      eventLoop->analyseEvent();
    }
    std::string my_dir = std::string(TreeName);
    TDirectory *subdir = outfile->mkdir(my_dir.c_str());
    eventLoop->Write(subdir, std::string(TreeName));
    delete eventLoop;
    delete mych_data;
    outfile->Close();
    std::cout
        << "Finished looping over the events" << std::endl;
  }
  return 0;
}
