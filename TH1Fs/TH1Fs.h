#include "TH1F.h"
#include "TFile.h"
#include "TList.h"
#include <iostream>
#include <vector>
#include <map>

using namespace std;

class TH1Fs {
  
    map<TString,std::vector<TH1F*> > m_histos_twoTag;
    map<TString,std::vector<TH1F*> > m_histos_threeTag;
    map<TString,std::vector<TH1F*> > m_histos_fourTag;
    TString m_name;
    TString m_title;
    std::vector<TString> m_UncertaintyNames;  

 public:
    
    TH1Fs(){};
    TH1Fs(TString histname, TString title, int nbins, double xlow, double xup, vector<TString> sel, std::vector<TString> UncertaintyNames,TString ExpUncertaintyName){
        
        m_UncertaintyNames = UncertaintyNames;
        vector<TString> names_all;
        for (auto s : sel){
            names_all.push_back(s+"_TwoTags");
            names_all.push_back(s+"_ThreeTags");
            names_all.push_back(s+"_FourPlusTags");
        }

        TString appo_name_incl;
        TString appo_title_incl;
        for(int j=0; j < m_UncertaintyNames.size(); j++){
            for(int i=0; i < names_all.size(); i++){
               appo_name_incl  = histname + "_" + names_all.at(i);
               appo_title_incl = title    + " " + names_all.at(i);
               TH1F * h_appo   = new TH1F(appo_name_incl+m_UncertaintyNames.at(j)+"_"+ExpUncertaintyName, "", nbins, xlow, xup);
               if(names_all.at(i).Contains("TwoTags")){
                  m_histos_twoTag[names_all.at(i)].push_back((TH1F*) h_appo->Clone());
                  m_histos_twoTag[names_all.at(i)].at(j)->SetDefaultSumw2();
               }else if(names_all.at(i).Contains("ThreeTags")){
                  m_histos_threeTag[names_all.at(i)].push_back((TH1F*) h_appo->Clone());
                  m_histos_threeTag[names_all.at(i)].at(j)->SetDefaultSumw2();
               }else if(names_all.at(i).Contains("FourPlusTags")){
                  m_histos_fourTag[names_all.at(i)].push_back((TH1F*) h_appo->Clone());
                  m_histos_fourTag[names_all.at(i)].at(j)->SetDefaultSumw2();
               }
               delete h_appo;
            }
        }
    };        

    TH1Fs(TString histname, int nbins, double* xarray, vector<TString> sel, std::vector<TString> UncertaintyNames, TString ExpUncertaintyName){

        m_UncertaintyNames = UncertaintyNames;
        vector<TString> names_all;
        for (auto s : sel){
            names_all.push_back(s+"_TwoTags");
            names_all.push_back(s+"_ThreeTags");
            names_all.push_back(s+"_FourPlusTags");
        }

	TString appo_name_incl;
        for(int j=0; j < m_UncertaintyNames.size(); j++){
            for(int i=0; i < names_all.size(); i++){
               appo_name_incl  = histname + "_" + names_all.at(i) + m_UncertaintyNames.at(j) + "_" + ExpUncertaintyName;
               TH1F * h_appo   = new TH1F(appo_name_incl,"", nbins, xarray);
               if(names_all.at(i).Contains("TwoTags")){
                  m_histos_twoTag[names_all.at(i)].push_back((TH1F*) h_appo->Clone());
                  m_histos_twoTag[names_all.at(i)].at(j)->SetDefaultSumw2();
               }else if(names_all.at(i).Contains("ThreeTags")){
                  m_histos_threeTag[names_all.at(i)].push_back((TH1F*) h_appo->Clone());
                  m_histos_threeTag[names_all.at(i)].at(j)->SetDefaultSumw2();
               }else if(names_all.at(i).Contains("FourPlusTags")){
                  m_histos_fourTag[names_all.at(i)].push_back((TH1F*) h_appo->Clone());
                  m_histos_fourTag[names_all.at(i)].at(j)->SetDefaultSumw2();
               }
               delete h_appo;
            }
        }
    };

  void Fill(double val, std::vector<double> weight, map<TString, bool>sel, int NTags);	
  void Write(TDirectory *dir, std::string dirname);
};

