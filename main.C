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
  //int EventReadout = stoi(config["EventReadout"]);
  int EventReadout = 2000;
  bool batchMode = atoi(config["batchMode"].c_str());
  // This is where we initialise TreeNames as an empty vector of
  // strings.
  TString TreeName = TString("Nominal");
  Long64_t memoryLimit = 30000000; // 1000000000 = 1 Gigabyte, 1 = 1 Byte

  std::string stdpath = config["path"];
  auto MCDataPeriodes = parseDataPeriodes(config);
  auto index = stdpath.find("MC16");

  if (index == std::string::npos)
  {
    throw std::runtime_error(std::string("Error: not in path"));
  }

  for (auto stdMCDataPeriode : MCDataPeriodes)
  {
    std::cout << "\n"
              << "Working 1, data period : " << stdMCDataPeriode << "\n";
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
    std::cout << "\n"
              << "Working 2, OutFileName : " << OutFileName << "\n";
    if (!batchMode)
    {
      OutFileName = OUTPUTDIR + "/PlotFiles/" + OutFileName;
    }

    TFile *outfile = TFile::Open(OutFileName, "RECREATE");
    TChain *mych_data = new TChain(TreeName);
    mych_data->Add(path + "/" + SampleName);
    std::cout << "\n"
              << mych_data->GetEntries() << "  " << path + "/" + SampleName << "\n";
    EventLoop *eventLoop = new EventLoop(mych_data, TreeName, OutFileName, config);

    if (mych_data == 0)
      continue;
    // This takes the entries from mych_data, mych_data is set up in the "main.C" file. These entries are event data, each entry is 1 collition.
    Long64_t nentries = mych_data->GetEntriesFast();
    Long64_t nbytes = 0, nb = 0;
    int file_number = 0;
    std::cout << "\n"
              << "Working 3, nentries : " << nentries << "\n";
    for (Long64_t jentry = 0; jentry < nentries; jentry++)
    {
      if (nbytes == 0)
      {
        std::cout << "\n"
                  << "Working 4, nentries : " << nentries << "\n";
      }

      Long64_t ientry = eventLoop->LoadTree(jentry);
      if (nbytes == 0)
      {
        std::cout << "\n"
                  << "Working 5, ientry : " << ientry << "\n";
      }
      if (ientry < 0 || !mych_data)
        break;
      if (nbytes == 0)
      {
        std::cout << "\n"
                  << "Working 6, ientry : " << ientry << "\n";
      }
      nb = mych_data->GetEntry(jentry);
      if (nbytes == 0)
      {
        std::cout << "\n"
                  << "Working 7, ientry : " << ientry << "\n";
      }
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

      if (memoryLimit != 0)
      {
        if (nbytes > memoryLimit)
        {
          std::cout << "\n"
                    << "Working 8"
                    << "\n";
          std::string my_dir = std::string(TreeName);
          TDirectory *subdir = outfile->mkdir(my_dir.c_str());
          eventLoop->Write(subdir, std::string(TreeName));
          std::cout << "\n"
                    << "Working 9"
                    << "\n";
          delete eventLoop;
          std::cout << "\n"
                    << "Working 10"
                    << "\n";
          delete mych_data;
          std::cout << "\n"
                    << "Working 11"
                    << "\n";
          outfile->Close();
          std::cout << "\n"
                    << "Working 12"
                    << "\n";
          ++file_number;
          std::string file_extention = +"_" + std::to_string(file_number) + ".root";
          std::string ex_OutFileName = std::string(OutFileName);
          ex_OutFileName.replace(ex_OutFileName.end() - 5, ex_OutFileName.end(), file_extention);
          outfile = TFile::Open(ex_OutFileName.c_str(), "RECREATE");
          mych_data = new TChain(TreeName);
          mych_data->Add(path + "/" + SampleName);
          eventLoop = new EventLoop(mych_data, TreeName, ex_OutFileName, config);
          std::cout << "\n"
                    << "New output File " << ex_OutFileName << "\n";
          nbytes = 0;
        }
      }
    }
    std::cout << "\n"
              << "Working 13"
              << "\n";
    std::string my_dir = std::string(TreeName);
    TDirectory *subdir = outfile->mkdir(my_dir.c_str());
    eventLoop->Write(subdir, std::string(TreeName));
    std::cout << "\n"
              << "Working 14"
              << "\n";
    delete eventLoop;
    std::cout << "\n"
              << "Working 15"
              << "\n";
    delete mych_data;
    std::cout << "\n"
              << "Working 16"
              << "\n";
    outfile->Close();
    // This prints GetEntries from the Tchain to the terminal
    std::cout << "Finished looping over the events" << std::endl;
  }
  return 0;
}
