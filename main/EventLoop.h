//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Fri Nov 15 13:27:20 2019 by ROOT version 6.18/00
// from TTree Nominal/Nominal
// found on file: ../my_analysis_dir/run/submitDir_HIGG5D2_1L-MC16a-HVT-32-14-TCC-Wplus-2019-11-15_12h09/data-EasyTree/ttbar_nonallhad_PwPy8.root
//////////////////////////////////////////////////////////

#ifndef EventLoop_h
#define EventLoop_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.
#include "string"
#include "TLorentzVector.h"
#include "vector"
#include <iostream>
#include <fstream>

#include "utilis/Chi2_minimization.h"
#include "utilis/NeutrinoBuilder.h"
#include "TLorentzVector.h"
#include "TH1F.h"

#include "TH1Fs/TH1Fs.h"
#include "TMVA/Reader.h"
#include <unordered_map>
#include <string>

class EventLoop
{
public:
   TTree *fChain;               //!pointer to the analyzed TTree or TChain
   Int_t fCurrent;              //!current Tree number in a TChain
   TTree *m_myTree;             //!pointer to the output TTree
   TMVA::Reader *m_reader_qqbb; //!
   TMVA::Reader *m_reader_lvbb; //!

   // Fixed size dimensions of array or collections stored in the TTree if any.

   // Declaration of leaf types
   Int_t nJet;
   Int_t nFatJets;
   Int_t RunNumber;
   Int_t Lepton_Charge;
   Float_t METSig;
   Float_t ActualMu;
   Float_t EventWeight;
   std::string *Description;
   TLorentzVector *MET;
   TLorentzVector *Top_LV;
   TLorentzVector *Higgs_LV;
   TLorentzVector *Wplus_LV;
   TLorentzVector *Wminus_LV;
   TLorentzVector *Lepton4vector;
   std::vector<float> *FatJet_M;
   std::vector<float> *FatJet_PT;
   std::vector<float> *FatJet_Eta;
   std::vector<float> *FatJet_Phi;
   std::vector<float> *signal_Jet_M;
   std::vector<float> *forward_Jet_M;
   std::vector<float> *signal_Jet_PT;
   std::vector<float> *forward_Jet_PT;
   std::vector<float> *signal_Jet_Eta;
   std::vector<float> *signal_Jet_Phi;
   std::vector<float> *forward_Jet_Eta;
   std::vector<float> *forward_Jet_Phi;
   std::vector<float> *btag_score_selectJet;
   std::vector<float> *btag_score_signalJet;
   std::vector<float> *btag_score_forwardJet;
   std::vector<float> *TrackJet_PT;
   std::vector<float> *TrackJet_Eta;
   std::vector<float> *TrackJet_Phi;
   std::vector<float> *TrackJet_M;
   std::vector<float> *TrackJet_btagWeight;
   std::vector<TLorentzVector *> NeutrinoVec;
   map<TString, bool> pass_sel;

   // List of branches
   TBranch *b_nJet;                  //!
   TBranch *b_nFatJets;              //!
   TBranch *b_RunNumber;             //!
   TBranch *b_Lepton_Charge;         //!
   TBranch *b_METSig;                //!
   TBranch *b_ActualMu;              //!
   TBranch *b_EventWeight;           //!
   TBranch *b_Description;           //!
   TBranch *b_MET;                   //!
   TBranch *b_Top_LV;                //!
   TBranch *b_Higgs_LV;              //!
   TBranch *b_Wplus_LV;              //!
   TBranch *b_Wminus_LV;             //!
   TBranch *b_Lepton4vector;         //!
   TBranch *b_FatJet_M;              //!
   TBranch *b_FatJet_PT;             //!
   TBranch *b_FatJet_Eta;            //!
   TBranch *b_FatJet_Phi;            //!
   TBranch *b_signal_Jet_M;          //!
   TBranch *b_forward_Jet_M;         //!
   TBranch *b_signal_Jet_PT;         //!
   TBranch *b_forward_Jet_PT;        //!
   TBranch *b_signal_Jet_Eta;        //!
   TBranch *b_signal_Jet_Phi;        //!
   TBranch *b_forward_Jet_Eta;       //!
   TBranch *b_forward_Jet_Phi;       //!
   TBranch *b_btag_score_selectJet;  //!
   TBranch *b_btag_score_signalJet;  //!
   TBranch *b_btag_score_forwardJet; //!
   TBranch *b_TrackJet_PT;           //!
   TBranch *b_TrackJet_Eta;          //!
   TBranch *b_TrackJet_Phi;          //!
   TBranch *b_TrackJet_M;            //!
   TBranch *b_TrackJet_btagWeight;   //!

   EventLoop(TTree *tree = 0, TString sampleName = "", TString ExpUncertaintyName = "Nominal", TString WP = "", int EventReadout = 0,
             bool flatCutFlow = true, bool realCutFlow = true, bool flatAltCutFlow = false, bool realAltCutFlow = false,
             Float_t hmlb = 90., Float_t hmub = 140., Float_t wmlb = 70., Float_t wmub = 100., Float_t met_ptv = 30000.,
             Float_t lep_ptv = 30000., Float_t jet0_ptv = 200000., Float_t jet1_ptv = 200000., Float_t lep_jet0_angle = 1.0,
             Float_t lep_jet1_angle = 1.0, Float_t hw_angle = 2.5, Float_t solo_jet_ptv = 250000.);

   EventLoop(TTree *tree, TString ExpUncertaintyName, TString outFileName, std::unordered_map<std::string, std::string> config);

   void Write(TDirectory *dir, std::string dirname);
   void FillMVATree(int i_H1, int i_H2, int i_w1, int i_w2, bool is_signal);
   void Sort_Jets(std::vector<TLorentzVector> *Jets, std::vector<int> *is_tagged);
   void Set_Jet_observables();
   void SetJetVectors();
   void WriteMVAInput();
   void MatchTruthParticlesToJets();
   void initializeMVA_qqbb();
   void initializeMVA_lvbb();
   double GetMwt();
   double GetTruthMass();
   double EvaluateMVAResponse_qqbb(int i_H1, int i_H2, int i_w1, int i_w2);
   double EvaluateMVAResponse_lvbb(int i_H1, int i_H2, TLorentzVector W);
   bool FindJetPair_qqbb();
   bool FindJetPair_lvbb();
   bool FindFJetPair(Float_t jet0_ptv, Float_t jet1_ptv, Float_t lep_jet0_angle, Float_t lep_jet1_angle,
                     Float_t hw_angle, Float_t solo_jet_ptv);

   void SetJetPair();
   bool PassEventSelectionResolved();
   bool PassEventSelectionBoosted(Float_t met_ptv, Float_t lep_ptv, Float_t jet0_ptv, Float_t jet1_ptv, Float_t lep_jet0_angle, Float_t lep_jet1_angle, Float_t hw_angle,
                                  Float_t solo_jet_ptv);
   int GetBTagCategory(int NTags_InHiggsJet, int NTags_OutsideHiggsJet);
   int GetBTagCategoryShort(int NTags_InHiggsJet, int NTags_OutsideHiggsJet);
   int GetTagWeightBin(double btag_score);
   TLorentzVector GetWBoson(bool &status);
   TLorentzVector BuildLeptonicTop();
   std::vector<TLorentzVector *> GetNeutrinos(TLorentzVector *L, TLorentzVector *MET);
   virtual ~EventLoop();
   virtual Int_t Cut(Long64_t entry);
   virtual Int_t GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void Init(TTree *tree, TString sampleName, TString ExpUncertaintyName);
   virtual void Loop();
   virtual Bool_t Notify();
   virtual void Show(Long64_t entry = -1);

   Chi2_minimization *myMinimizer = new Chi2_minimization("MeV");
   NeutrinoBuilder *m_NeutrinoBuilder;

   TH1Fs *h_NBtags;
   TH1Fs *h_MET;
   TH1Fs *h_METSig;
   TH1Fs *h_Lepton_Eta;
   TH1Fs *h_Lepton_Pt;
   TH1Fs *h_Njets;
   TH1Fs *h_NFjets;
   TH1Fs *h_Mwt;
   TH1Fs *h_MinDeltaPhiJETMET;
   TH1Fs *h_HT;
   TH1Fs *h_HT_bjets;
   TH1Fs *h_HT_bjets_Lepton_Pt;
   TH1Fs *h_mVH;
   TH1Fs *h_DeltaPhi_HW;
   TH1Fs *h_maxMVAResponse;
   TH1Fs *h_pTH;
   TH1Fs *h_pTH_over_mVH;
   TH1Fs *h_pTWplus;
   TH1Fs *h_pTW_over_mVH;
   TH1Fs *h_pTWminus;
   TH1Fs *h_mH;
   TH1Fs *h_mWplus;
   TH1Fs *h_tagCategory;
   TH1Fs *h_mass_resolution;
   TH1Fs *h_MET_over_sqrtHT;
   TH1Fs *h_m_NTags_trkJ;

   vector<double> m_EventWeights;
   vector<TString> m_UncNames;
   vector<TString> mySel;

   std::vector<TLorentzVector> Jets;
   std::vector<TLorentzVector> FJets;
   std::vector<TLorentzVector> TrkJets;
   std::vector<int> JetIsTagged;
   std::vector<int> TrkJetIsTagged;
   std::vector<int> nTaggedVRTrkJetsInFJet;

   TLorentzVector Top;
   TLorentzVector Higgs;
   TLorentzVector Wplus;
   TLorentzVector Wminus;
   int m_is_Signal;
   int m_NTags;
   int m_NTags_caloJ;
   int m_NTags_trkJ;
   int m_NTags_Higgs;
   int m_NTags_Wplus;
   int m_ntagsOutside;
   int m_bTagCategory;
   int m_btagCategoryBin;
   int m_index_H1;
   int m_index_H2;
   int m_index_W1;
   int m_index_W2;
   double m_min_dRTruth;
   double m_min_chi2;
   double m_min_DeltaPhiJETMET;
   double m_MaxMVA_Response;
   double m_HT;
   double m_HT_bjets;
   double m_maxEta_bjets;
   double m_maxPT_bjets;
   double m_MET;
   double m_mWT;
   double m_Lep_PT;
   double m_mVH;
   double m_DeltaPhi_HW;
   double m_Wleptonic_pT;
   double m_Wleptonic_Eta;
   double m_MassTruth;
   float m_H_mass;
   float m_H_pT;
   float m_pTjH1;
   float m_pTjH2;
   float m_btagjH1;
   float m_btagjH2;
   float m_dRjjH;
   float m_Wp_mass;
   float m_Wp_pT;
   float m_pTjWp1;
   float m_pTjWp2;
   float m_btagjWp1;
   float m_btagjWp2;
   float m_dRjjWp;
   float m_Phi_HW;
   float m_mass_VH;
   float m_btagCut_value_trkJets;
   float m_btagCut_value_CaloJets;
   float m_pTH_over_mvH;
   float m_ptW_over_mvH;
   // Higgs and W mass bounds
   Float_t hmlb = 90.;
   Float_t hmub = 140.;
   Float_t wmlb = 70.;
   Float_t wmub = 100.;
   // Variables for cuts, here is the key: What the value is called in the code, What it is called in physics, the lable I am using for it's value.
   // MET->pt(), missing transverse momentum, met_ptv,
   // Lepton4vector->Pt(), lepton transverse momentum, lep_ptv.
   // I refer to the jet that is asigned to FJets.at(0) as jet 0 and the FJets.at(1) jet as jet 1,
   // FJets.at(0)->pt(), transverse momenta of fat bjet 0, jet0_ptv,
   // FJets.at(0).DeltaR(*Lepton4vector), angle of fat bjet 0 and lepton, lep_jet0_angle,
   // m_DeltaPhi_HW, angle of higgs and wboson, hw_angle
   // FJets.at(0).Pt() in the seperate if statment, the single fat b jet when the othet dosn't generate, solo_jet_ptv
   Float_t met_ptv = 30000.;
   Float_t lep_ptv = 30000.;
   Float_t jet0_ptv = 200000.;
   Float_t jet1_ptv = 200000.;
   Float_t lep_jet0_angle = 1.0;
   Float_t lep_jet1_angle = 1.0;
   Float_t hw_angle = 2.5;
   Float_t solo_jet_ptv = 250000.;
   int EventReadout = 0;
   bool flatCutFlow = true;
   bool realCutFlow = true;
   bool flatAltCutFlow = false;
   bool realAltCutFlow = false;

   //cutflow of config parameters
   ofstream m_cutFlowFileStream;
   ofstream m_cutFlowFileStreamAlt;
   TString m_cutFlowFileName;
   TString m_cutFlowFileNameAlt;
   bool jjbb;
   struct CutFlowType
   {
      int jjbb_twoTags = 0;
      int jjbb_threeTags = 0;
      int jjbb_fourPlusTags = 0;
      int lvbb_twoTags = 0;
      int lvbb_threeTags = 0;
      int lvbb_fourPlusTags = 0;
      Float_t jjbb_weightedTwoTags = 0;
      Float_t jjbb_weightedThreeTags = 0;
      Float_t jjbb_weightedFourPlusTags = 0;
      Float_t lvbb_weightedTwoTags = 0;
      Float_t lvbb_weightedThreeTags = 0;
      Float_t lvbb_weightedFourPlusTags = 0;

      int jjbb_Total() const
      {
         return jjbb_twoTags + jjbb_threeTags + jjbb_fourPlusTags;
      }

      Float_t jjbb_WeightedTotal() const
      {
         return jjbb_weightedTwoTags + jjbb_weightedThreeTags + jjbb_weightedFourPlusTags;
      }

      int lvbb_Total() const
      {
         return lvbb_twoTags + lvbb_threeTags + lvbb_fourPlusTags;
      }

      Float_t lvbb_WeightedTotal() const
      {
         return lvbb_weightedTwoTags + lvbb_weightedThreeTags + lvbb_weightedFourPlusTags;
      }
   };

   void altCutFlow(Float_t met_ptv, Float_t lep_ptv, Float_t jet0_ptv, Float_t jet1_ptv, Float_t lep_jet0_angle, Float_t lep_jet1_angle,
                   Float_t hw_angle, Float_t solo_jet_ptv);
   void CutFlowAssignment(CutFlowType &cutVariable, bool XflatCutFlow, bool XrealCutFlow);
   void CutFlowParser(ofstream &File, const CutFlowType &cutVariable, const std::string cutName, bool XflatCutFlow, bool XrealCutFlow);
   CutFlowType m_TotalEvents;
   CutFlowType m_noJets;
   CutFlowType m_HadronicCutFlow;
   CutFlowType m_LeptonicCutFlow;
   CutFlowType m_METCutFlow;
   CutFlowType m_LeptonPtCutFlow;
   CutFlowType m_HiggsPtCutFlow;
   CutFlowType m_WplusPtCutFlow;
   CutFlowType m_Higgs_LeptonAngleCutflow;
   CutFlowType m_Wplus_LeptonAngleCutflow;
   CutFlowType m_Higgs_WplusAngleCutflow;
   CutFlowType m_PositiveLepWCutflow;
   CutFlowType m_PositiveLepHiggsPtCutFlow;
   CutFlowType m_HiggsMassCutFlow;
   CutFlowType m_WplusMassCutFlow;
   //Below is the alternate cutflow
   CutFlowType m_ChannelFlexCutFlow;
   CutFlowType m_HiggsPtAltCutFlow;
   CutFlowType m_Higgs_LeptonAngleAltCutflow;
   CutFlowType m_Wplus_LeptonAngleAltCutflow;
   CutFlowType m_Higgs_WplusAngleAltCutflow;
   CutFlowType m_PositiveLepWAltCutflow;
   CutFlowType m_PositiveLepHiggsPtAltCutFlow;
   CutFlowType m_HiggsMassAltCutFlow;
   CutFlowType m_WplusMassAltCutFlow;
};

#endif

#ifdef EventLoop_cxx

EventLoop::EventLoop(TTree *tree, TString ExpUncertaintyName, TString outFileName, std::unordered_map<std::string, std::string> config) : fChain(0)
{
   if (tree == 0)
   {
      std::cerr << "Error in EventLoop::EventLoop(): tree is nullptr" << std::endl;
      return;
   }

   if (config["Higgs_mass_lower_bound"] != "")
   {
      hmlb = std::stof(config["Higgs_mass_lower_bound"]);
   }
   if (config["Higgs_mass_upper_bound"] != "")
   {
      hmub = std::stof(config["Higgs_mass_upper_bound"]);
   }
   if (config["Wboson_mass_lower_bound"] != "")
   {
      wmlb = std::stof(config["Wboson_mass_lower_bound"]);
   }
   if (config["Wboson_mass_upper_bound"] != "")
   {
      wmub = std::stof(config["Wboson_mass_upper_bound"]);
   }
   if (config["Higgs_Wboson_angle"] != "")
   {
      hw_angle = std::stof(config["Higgs_Wboson_angle"]);
   }
   if (config["Missing_transverse_momentum"] != "")
   {
      met_ptv = std::stof(config["Missing_transverse_momentum"]);
   }
   if (config["Lepton_transverse_momentum"] != "")
   {
      lep_ptv = std::stof(config["Lepton_transverse_momentum"]);
   }
   if (config["2Jets_Jet1_transverse_momentum"] != "")
   {
      jet0_ptv = std::stof(config["2Jets_Jet1_transverse_momentum"]);
   }
   if (config["2Jets_Jet2_transverse_momentum"] != "")
   {
      jet1_ptv = std::stof(config["2Jets_Jet2_transverse_momentum"]);
   }
   if (config["2Jets_Jet1_lepton_angle"] != "")
   {
      lep_jet0_angle = std::stof(config["2Jets_Jet1_lepton_angle"]);
   }
   if (config["2Jets_Jet2_lepton_angle"] != "")
   {
      lep_jet1_angle = std::stof(config["2Jets_Jet2_lepton_angle"]);
   }
   if (config["1Jet_Jet_transverse_momentum"] != "")
   {
      solo_jet_ptv = std::stof(config["1Jet_Jet_transverse_momentum"]);
   }
   if (config["EventReadout"] != "")
   {
      EventReadout = std::stoi(config["EventReadout"]);
   }
   if (config["FlatCutFlow"] != "")
   {
      if (config["FlatCutFlow"] == "Enable" || config["FlatCutFlow"] == "enable")
      {
         flatCutFlow = true;
      }
      else
      {
         flatCutFlow = false;
      }
   }
   if (config["RealCutFlow"] != "")
   {
      if (config["RealCutFlow"] == "Enable" || config["RealCutFlow"] == "enable")
      {
         realCutFlow = true;
      }
      else
      {
         realcutFlow = false;
      }
   }
   if (config["FlatAlternateCutFlow"] != "")
   {
      if (config["FlatAlternateCutFlow"] == "Enable" || config["FlatAlternateCutFlow"] == "enable")
      {
         flatAltCutFlow = true;
      }
      else
      {
         flatAltCutFlow = false;
      }
   }
   if (config["RealAlternateCutFlow"] != "")
   {
      if (config["RealAlternateCutFlow"] == "Enable" || config["RealAlternateCutFlow"] == "enable")
      {
         realAltCutFlow = true;
      }
      else
      {
         realAltCutFlow = false;
      }
   }
   if (config["SampleName"] == "")
   {
      throw std::runtime_error(std::string("Error: No SampleName given"));
   }
   if (config["WP"] == "")
   {
      throw std::runtime_error(std::string("Error: No WP given"));
   }

   TString SampleName = config["SampleName"];
   TString WP = config["WP"];

   m_btagCut_value_trkJets = -1.;
   if (WP == "85p")
   {
      m_btagCut_value_trkJets = 0.05;
      m_btagCut_value_CaloJets = 0.11;
      m_btagCategoryBin = 1;
   }
   if (WP == "77p")
   {
      m_btagCut_value_trkJets = 0.58;
      m_btagCut_value_CaloJets = 0.64;
      m_btagCategoryBin = 2;
   }
   if (WP == "70p")
   {
      m_btagCut_value_trkJets = 0.79;
      m_btagCut_value_CaloJets = 0.83;
      m_btagCategoryBin = 3;
   }
   if (WP == "60p")
   {
      m_btagCut_value_trkJets = 0.92;
      m_btagCut_value_CaloJets = 0.94;
      m_btagCategoryBin = 4;
   }
   outFileName.ReplaceAll(".root", "-cutFlow.txt");
   m_cutFlowFileName = outFileName;
   outFileName.ReplaceAll("-cutFlow.txt", "-cutFlowAlt.txt");
   m_cutFlowFileNameAlt = outFileName;
   Init(tree, SampleName, ExpUncertaintyName);
}

EventLoop::EventLoop(TTree *tree, TString sampleName, TString ExpUncertaintyName, TString WP, int EventReadout, bool flatCutFlow,
                     bool realCutFlow, bool flatAltCutFlow, bool realAltCutFlow, Float_t hmlb, Float_t hmub, Float_t wmlb,
                     Float_t wmub, Float_t met_ptv, Float_t lep_ptv, Float_t jet0_ptv, Float_t jet1_ptv, Float_t lep_jet0_angle,
                     Float_t lep_jet1_angle, Float_t hw_angle, Float_t solo_jet_ptv) : fChain(0),
                                                                                       hmlb(hmlb),
                                                                                       hmub(hmub),
                                                                                       wmlb(wmlb),
                                                                                       wmub(wmub),
                                                                                       met_ptv(met_ptv),
                                                                                       lep_ptv(lep_ptv),
                                                                                       jet0_ptv(jet0_ptv),
                                                                                       jet1_ptv(jet1_ptv),
                                                                                       lep_jet0_angle(lep_jet0_angle),
                                                                                       lep_jet1_angle(lep_jet1_angle),
                                                                                       hw_angle(hw_angle),
                                                                                       solo_jet_ptv(solo_jet_ptv)
{

   // if parameter tree is not specified (or zero), connect the file
   // used to generate this class and read the Tree.
   if (tree == 0)
   {
      std::cerr << "Error in EventLoop::EventLoop(): tree is nullptr" << std::endl;
      return;
   }
   m_btagCut_value_trkJets = -1.;
   if (WP == "85p")
   {
      m_btagCut_value_trkJets = 0.05;
      m_btagCut_value_CaloJets = 0.11;
      m_btagCategoryBin = 1;
   }
   if (WP == "77p")
   {
      m_btagCut_value_trkJets = 0.58;
      m_btagCut_value_CaloJets = 0.64;
      m_btagCategoryBin = 2;
   }
   if (WP == "70p")
   {
      m_btagCut_value_trkJets = 0.79;
      m_btagCut_value_CaloJets = 0.83;
      m_btagCategoryBin = 3;
   }
   if (WP == "60p")
   {
      m_btagCut_value_trkJets = 0.92;
      m_btagCut_value_CaloJets = 0.94;
      m_btagCategoryBin = 4;
   }

   std::cout << "Using WP = " << WP << " corresponding to w_{MVA} > " << m_btagCut_value_trkJets << std::endl;

   Init(tree, sampleName, ExpUncertaintyName);
}

void EventLoop::CutFlowParser(ofstream &File, const CutFlowType &cutVariable, const std::string cutName, bool XflatCutFlow, bool XrealCutFlow)
{
   if (XflatCutFlow == true)
   {
      File << cutName << "=" << cutVariable.jjbb_twoTags << "," << cutVariable.jjbb_threeTags << ","
           << cutVariable.jjbb_fourPlusTags << "," << cutVariable.jjbb_Total() << "|" << cutVariable.lvbb_twoTags
           << "," << cutVariable.lvbb_threeTags << "," << cutVariable.lvbb_fourPlusTags << ","
           << cutVariable.lvbb_Total() << "\n"
   }
   if (XrealCutFlow == true)
   {
      File << "real" << cutName << "=" << cutVariable.jjbb_weightedTwoTags << "," << cutVariable.jjbb_weightedThreeTags
           << "," << cutVariable.jjbb_weightedFourPlusTags << "," << cutVariable.jjbb_WeightedTotal() << "|"
           << cutVariable.lvbb_weightedTwoTags << "," << cutVariable.lvbb_weightedThreeTags << ","
           << cutVariable.lvbb_weightedFourPlusTags << "," << cutVariable.lvbb_WeightedTotal() << "\n";
   }
}

EventLoop::~EventLoop()
{
   if (flatCutFlow == true || realCutFlow == true)
   {
      m_cutFlowFileStream.open(m_cutFlowFileName);
      CutFlowParser(m_cutFlowFileStream, m_TotalEvents, "TotalEvents", flatCutFlow, realCutFlow);
      CutFlowParser(m_cutFlowFileStream, m_HadronicCutFlow, "Hadronic_rejected", flatCutFlow, realCutFlow);
      CutFlowParser(m_cutFlowFileStream, m_LeptonicCutFlow, "Leptonic_rejected", flatCutFlow, realCutFlow);
      CutFlowParser(m_cutFlowFileStream, m_METCutFlow, "MET", flatCutFlow, realCutFlow);
      CutFlowParser(m_cutFlowFileStream, m_LeptonPtCutFlow, "Lepton_momentum", flatCutFlow, realCutFlow);
      CutFlowParser(m_cutFlowFileStream, m_HiggsPtCutFlow, "Higgs_momentum", flatCutFlow, realCutFlow);
      CutFlowParser(m_cutFlowFileStream, m_WplusPtCutFlow, "Wboson_momentum", flatCutFlow, realCutFlow);
      CutFlowParser(m_cutFlowFileStream, m_Higgs_LeptonAngleCutflow, "Higgs_Lepton_Angle", flatCutFlow, realCutFlow);
      CutFlowParser(m_cutFlowFileStream, m_Wplus_LeptonAngleCutflow, "Wboson_Lepton_Angle", flatCutFlow, realCutFlow);
      CutFlowParser(m_cutFlowFileStream, m_Higgs_WplusAngleCutflow, "Higgs_Wboson_Angle", flatCutFlow, realCutFlow);
      CutFlowParser(m_cutFlowFileStream, m_PositiveLepWCutflow, "PositiveLep_Wboson_bool", flatCutFlow, realCutFlow);
      CutFlowParser(m_cutFlowFileStream, m_PositiveLepHiggsPtCutFlow, "PositiveLep_Higgs_momentum", flatCutFlow, realCutFlow);
      CutFlowParser(m_cutFlowFileStream, m_HiggsMassCutFlow, "Higgs_Mass", flatCutFlow, realCutFlow);
      CutFlowParser(m_cutFlowFileStream, m_WplusMassCutFlow, "Wplus_Mass", flatCutFlow, realCutFlow);
      if (flatCutFlow == true)
      {
         m_cutFlowFileStream << "noFatJets"
                             << "=" << m_noJets.jjbb_Total() << "," << m_noJets.lvbb_Total() << "\n"
      }
      if (realCutFlow == true)
      {
         m_cutFlowFileStream << "real"
                             << "noFatJets"
                             << "=" << m_noJets.jjbb_WeightedTotal() << "," << m_noJets.lvbb_WeightedTotal() << "\n";
      }
      m_cutFlowFileStream.close();
   }

   if (flatAltCutFlow == true || realAltCutFlow == true)
   {
      m_cutFlowFileStreamAlt.open(m_cutFlowFileNameAlt);
      CutFlowParser(m_cutFlowFileStreamAlt, m_TotalEvents, "TotalEvents", flatAltCutFlow, realAltCutFlow);
      CutFlowParser(m_cutFlowFileStreamAlt, m_HadronicCutFlow, "Hadronic_rejected", flatAltCutFlow, realAltCutFlow);
      CutFlowParser(m_cutFlowFileStreamAlt, m_LeptonicCutFlow, "Leptonic_rejected", flatAltCutFlow, realAltCutFlow);
      CutFlowParser(m_cutFlowFileStreamAlt, m_ChannelFlexCutFlow, "jjbb_OR_lvbb_rejected", flatAltCutFlow, realAltCutFlow);
      CutFlowParser(m_cutFlowFileStreamAlt, m_HiggsPtAltCutFlow, "Higgs_momentum", flatAltCutFlow, realAltCutFlow);
      CutFlowParser(m_cutFlowFileStreamAlt, m_Higgs_LeptonAngleAltCutflow, "Higgs_Lepton_Angle", flatAltCutFlow, realAltCutFlow);
      CutFlowParser(m_cutFlowFileStreamAlt, m_Wplus_LeptonAngleAltCutflow, "Wboson_Lepton_Angle", flatAltCutFlow, realAltCutFlow);
      CutFlowParser(m_cutFlowFileStreamAlt, m_Higgs_WplusAngleAltCutflow, "Higgs_Wboson_Angle", flatAltCutFlow, realAltCutFlow);
      CutFlowParser(m_cutFlowFileStreamAlt, m_PositiveLepWAltCutflow, "PositiveLep_Wboson_bool", flatAltCutFlow, realAltCutFlow);
      CutFlowParser(m_cutFlowFileStreamAlt, m_PositiveLepHiggsPtAltCutFlow, "PositiveLep_Higgs_momentum", flatAltCutFlow, realAltCutFlow);
      CutFlowParser(m_cutFlowFileStreamAlt, m_HiggsMassAltCutFlow, "Higgs_Mass", flatAltCutFlow, realAltCutFlow);
      CutFlowParser(m_cutFlowFileStreamAlt, m_WplusMassAltCutFlow, "Wplus_Mass", flatAltCutFlow, realAltCutFlow);
      if (flatAltCutFlow == true)
      {
         m_cutFlowFileStreamAlt << "noFatJets"
                                << "=" << m_noJets.jjbb_Total() << "," << m_noJets.lvbb_Total() << "\n"
      }
      if (realAltCutFlow == true)
      {
         m_cutFlowFileStreamAlt << "real"
                                << "noFatJets"
                                << "=" << m_noJets.jjbb_WeightedTotal() << "," << m_noJets.lvbb_WeightedTotal() << "\n";
      }
      m_cutFlowFileStreamAlt.close();
   }

   if (!fChain)
      return;
   delete fChain->GetCurrentFile();
}

Int_t EventLoop::GetEntry(Long64_t entry)
{
   // Read contents of entry.
   if (!fChain)
      return 0;
   return fChain->GetEntry(entry);
}
Long64_t EventLoop::LoadTree(Long64_t entry)
{
   // Set the environment to read one entry
   if (!fChain)
      return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0)
      return centry;
   if (fChain->GetTreeNumber() != fCurrent)
   {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void EventLoop::Init(TTree *tree, TString sampleName, TString ExpUncertaintyName)
{

   initializeMVA_qqbb();
   initializeMVA_lvbb();

   m_NeutrinoBuilder = new NeutrinoBuilder("MeV");
   sampleName.Resize(sampleName.Index(".root"));

   m_UncNames = {""};
   mySel = {"Merged_LepP_SR", "Merged_LepP_CR", "Merged_LepN_SR", "Merged_LepN_CR"};

   h_MET = new TH1Fs(sampleName + "_MET", "", 30, 0, 600, mySel, m_UncNames, ExpUncertaintyName);
   h_METSig = new TH1Fs(sampleName + "_METSig", "", 30, 0, 30, mySel, m_UncNames, ExpUncertaintyName);
   h_Lepton_Eta = new TH1Fs(sampleName + "_Lepton_Eta", "", 25, -2.5, 2.5, mySel, m_UncNames, ExpUncertaintyName);
   h_Lepton_Pt = new TH1Fs(sampleName + "_Lepton_Pt", "", 25, 0, 600, mySel, m_UncNames, ExpUncertaintyName);
   h_NBtags = new TH1Fs(sampleName + "_nBTags", "", 7, -0.5, 6.5, mySel, m_UncNames, ExpUncertaintyName);
   h_Njets = new TH1Fs(sampleName + "_nJets", "", 13, -0.5, 12.5, mySel, m_UncNames, ExpUncertaintyName);
   h_NFjets = new TH1Fs(sampleName + "_nJets_(Fat)", "", 13, -0.5, 12.5, mySel, m_UncNames, ExpUncertaintyName);
   h_Mwt = new TH1Fs(sampleName + "_Mwt", "", 30, 0, 300, mySel, m_UncNames, ExpUncertaintyName);
   h_MinDeltaPhiJETMET = new TH1Fs(sampleName + "_MinDeltaPhiJETMET", "", 32, 0, 3.2, mySel, m_UncNames, ExpUncertaintyName);
   h_HT = new TH1Fs(sampleName + "_HT", "", 30, 0, 1500, mySel, m_UncNames, ExpUncertaintyName);
   h_HT_bjets = new TH1Fs(sampleName + "_HT_bjets", "", 30, 0, 1200, mySel, m_UncNames, ExpUncertaintyName);
   h_HT_bjets_Lepton_Pt = new TH1Fs(sampleName + "_HT_bjets_Lepton_Pt", "", 30, 0, 1200, mySel, m_UncNames, ExpUncertaintyName);
   h_mVH = new TH1Fs(sampleName + "_mVH", "", 30, 0, 2400, mySel, m_UncNames, ExpUncertaintyName);
   h_DeltaPhi_HW = new TH1Fs(sampleName + "_DeltaPhi_HW", "", 32, 0, 3.2, mySel, m_UncNames, ExpUncertaintyName);
   h_maxMVAResponse = new TH1Fs(sampleName + "_maxMVAResponse", "", 20, -1, 1, mySel, m_UncNames, ExpUncertaintyName);
   h_pTH = new TH1Fs(sampleName + "_pTH", "", 25, 0, 800, mySel, m_UncNames, ExpUncertaintyName);
   h_pTH_over_mVH = new TH1Fs(sampleName + "_pTH_over_mVH", "", 25, 0, 1, mySel, m_UncNames, ExpUncertaintyName);
   h_pTWplus = new TH1Fs(sampleName + "_pTWplus", "", 25, 0, 800, mySel, m_UncNames, ExpUncertaintyName);
   h_pTW_over_mVH = new TH1Fs(sampleName + "_pTW_over_mVH", "", 25, 0, 1, mySel, m_UncNames, ExpUncertaintyName);
   h_pTWminus = new TH1Fs(sampleName + "_pTWminus", "", 25, 0, 800, mySel, m_UncNames, ExpUncertaintyName);
   h_mH = new TH1Fs(sampleName + "_mH", "", 30, 50, 200, mySel, m_UncNames, ExpUncertaintyName);
   h_mWplus = new TH1Fs(sampleName + "_mWplus", "", 30, 50, 200, mySel, m_UncNames, ExpUncertaintyName);
   h_tagCategory = new TH1Fs(sampleName + "_BtagCategory", "", 11, -0.5, 10.5, mySel, m_UncNames, ExpUncertaintyName);
   h_mass_resolution = new TH1Fs(sampleName + "_mass_resolution", "", 20, -1.0, 1.0, mySel, m_UncNames, ExpUncertaintyName);
   h_MET_over_sqrtHT = new TH1Fs(sampleName + "_MET_over_rootHT", "", 30, 0, 600, mySel, m_UncNames, ExpUncertaintyName);
   h_m_NTags_trkJ = new TH1Fs(sampleName + "_m_NTags_trkJ", "", 13, -0.5, 12.5, mySel, m_UncNames, ExpUncertaintyName);

   // Set object pointer
   Description = 0;
   MET = 0;
   Top_LV = 0;
   Higgs_LV = 0;
   Wplus_LV = 0;
   Wminus_LV = 0;
   Lepton4vector = 0;
   FatJet_M = 0;
   FatJet_PT = 0;
   FatJet_Eta = 0;
   FatJet_Phi = 0;
   signal_Jet_M = 0;
   forward_Jet_M = 0;
   signal_Jet_PT = 0;
   forward_Jet_PT = 0;
   signal_Jet_Eta = 0;
   signal_Jet_Phi = 0;
   forward_Jet_Eta = 0;
   forward_Jet_Phi = 0;
   btag_score_selectJet = 0;
   btag_score_signalJet = 0;
   btag_score_forwardJet = 0;
   TrackJet_PT = 0;
   TrackJet_Eta = 0;
   TrackJet_Phi = 0;
   TrackJet_M = 0;
   TrackJet_btagWeight = 0;
   // Set branch addresses and branch pointers
   if (!tree)
      return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("nJet", &nJet, &b_nJet);
   fChain->SetBranchAddress("nFatJets", &nFatJets, &b_nFatJets);
   fChain->SetBranchAddress("RunNumber", &RunNumber, &b_RunNumber);
   fChain->SetBranchAddress("Lepton_Charge", &Lepton_Charge, &b_Lepton_Charge);
   fChain->SetBranchAddress("METSig", &METSig, &b_METSig);
   fChain->SetBranchAddress("ActualMu", &ActualMu, &b_ActualMu);
   fChain->SetBranchAddress("EventWeight", &EventWeight, &b_EventWeight);
   fChain->SetBranchAddress("Description", &Description, &b_Description);
   fChain->SetBranchAddress("MET", &MET, &b_MET);
   fChain->SetBranchAddress("Top_LV", &Top_LV, &b_Top_LV);
   fChain->SetBranchAddress("Higgs_LV", &Higgs_LV, &b_Higgs_LV);
   fChain->SetBranchAddress("Wplus_LV", &Wplus_LV, &b_Wplus_LV);
   fChain->SetBranchAddress("Wminus_LV", &Wminus_LV, &b_Wminus_LV);
   fChain->SetBranchAddress("Lepton4vector", &Lepton4vector, &b_Lepton4vector);
   fChain->SetBranchAddress("FatJet_M", &FatJet_M, &b_FatJet_M);
   fChain->SetBranchAddress("FatJet_PT", &FatJet_PT, &b_FatJet_PT);
   fChain->SetBranchAddress("FatJet_Eta", &FatJet_Eta, &b_FatJet_Eta);
   fChain->SetBranchAddress("FatJet_Phi", &FatJet_Phi, &b_FatJet_Phi);
   fChain->SetBranchAddress("signal_Jet_M", &signal_Jet_M, &b_signal_Jet_M);
   fChain->SetBranchAddress("forward_Jet_M", &forward_Jet_M, &b_forward_Jet_M);
   fChain->SetBranchAddress("signal_Jet_PT", &signal_Jet_PT, &b_signal_Jet_PT);
   fChain->SetBranchAddress("forward_Jet_PT", &forward_Jet_PT, &b_forward_Jet_PT);
   fChain->SetBranchAddress("signal_Jet_Eta", &signal_Jet_Eta, &b_signal_Jet_Eta);
   fChain->SetBranchAddress("signal_Jet_Phi", &signal_Jet_Phi, &b_signal_Jet_Phi);
   fChain->SetBranchAddress("forward_Jet_Eta", &forward_Jet_Eta, &b_forward_Jet_Eta);
   fChain->SetBranchAddress("forward_Jet_Phi", &forward_Jet_Phi, &b_forward_Jet_Phi);
   fChain->SetBranchAddress("btag_score_selectJet", &btag_score_selectJet, &b_btag_score_selectJet);
   fChain->SetBranchAddress("btag_score_signalJet", &btag_score_signalJet, &b_btag_score_signalJet);
   fChain->SetBranchAddress("btag_score_forwardJet", &btag_score_forwardJet, &b_btag_score_forwardJet);
   fChain->SetBranchAddress("TrackJet_PT", &TrackJet_PT, &b_TrackJet_PT);
   fChain->SetBranchAddress("TrackJet_Eta", &TrackJet_Eta, &b_TrackJet_Eta);
   fChain->SetBranchAddress("TrackJet_Phi", &TrackJet_Phi, &b_TrackJet_Phi);
   fChain->SetBranchAddress("TrackJet_M", &TrackJet_M, &b_TrackJet_M);
   fChain->SetBranchAddress("TrackJet_btagWeight", &TrackJet_btagWeight, &b_TrackJet_btagWeight);
   Notify();

   m_myTree = new TTree("MVATree", "");
   /*
   m_myTree->Branch("nJet",	     &nJet);
   m_myTree->Branch("nBJet",         &m_NTags);
   m_myTree->Branch("HT_bjets",	     &m_HT_bjets);
   m_myTree->Branch("maxEta_bjets",  &m_maxEta_bjets);
   m_myTree->Branch("maxPT_bjets",   &m_maxPT_bjets);
   m_myTree->Branch("Wleptonic_pT",  &m_Wleptonic_pT);
   m_myTree->Branch("Wleptonic_Eta", &m_Wleptonic_Eta);
   m_myTree->Branch("Lep_PT",        &m_Lep_PT);
   m_myTree->Branch("MET",           &m_MET);
   m_myTree->Branch("Lepton_Charge", &Lepton_Charge);
   m_myTree->Branch("is_Signal",     &m_is_Signal);
   m_myTree->Branch("EventWeight",   &EventWeight);*/

   m_myTree->Branch("btagjH1", &m_btagjH1);
   m_myTree->Branch("btagjH2", &m_btagjH2);
   m_myTree->Branch("btagjW1", &m_btagjWp1);
   m_myTree->Branch("btagjW2", &m_btagjWp2);
   m_myTree->Branch("H_mass", &m_H_mass);
   m_myTree->Branch("Wp_mass", &m_Wp_mass);
   m_myTree->Branch("H_pT", &m_H_pT);
   m_myTree->Branch("Wp_pT", &m_Wp_pT);
   m_myTree->Branch("pTjH1", &m_pTjH1);
   m_myTree->Branch("pTjH2", &m_pTjH2);
   m_myTree->Branch("pTjWp1", &m_pTjWp1);
   m_myTree->Branch("pTjWp2", &m_pTjWp2);
   m_myTree->Branch("dRjjH", &m_dRjjH);
   m_myTree->Branch("dRjjWp", &m_dRjjWp);
   m_myTree->Branch("Phi_HW", &m_Phi_HW);
   m_myTree->Branch("mass_VH", &m_mass_VH);
   m_myTree->Branch("is_Signal", &m_is_Signal);
   m_myTree->Branch("EventWeight", &EventWeight);
}

Bool_t EventLoop::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void EventLoop::Show(Long64_t entry)
{
   // Print contents of entry.
   // If entry is not specified, print current entry
   if (!fChain)
      return;
   fChain->Show(entry);
}
Int_t EventLoop::Cut(Long64_t entry)
{
   // This function may be called from Loop.
   // returns  1 if entry is accepted.
   // returns -1 otherwise.
   return 1;
}
#endif // #ifdef EventLoop_cxx
