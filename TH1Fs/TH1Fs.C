#include "TH1Fs.h"

void TH1Fs::Fill(double val, std::vector<double> weight, map<TString, bool>passed_selections, int NTags){

  if(NTags == 2){
     for(unsigned int i = 0; i < weight.size(); i++){
       for(auto pair : m_histos_twoTag){
          TString HistName = pair.first;
          HistName.Resize(HistName.Index("_TwoTags"));
          if(passed_selections[HistName]){
              pair.second.at(i)->Fill(val,weight.at(i));
          }
       }
     }
  }else if(NTags == 3){
     for(unsigned int i = 0; i < weight.size(); i++){
       for(auto pair : m_histos_threeTag){
          TString HistName = pair.first;
          HistName.Resize(HistName.Index("_ThreeTags"));
          if(passed_selections[HistName]){
              pair.second.at(i)->Fill(val,weight.at(i));
          }
       }
     }
  }else if(NTags > 3){
     for(unsigned int i = 0; i < weight.size(); i++){
       for(auto pair : m_histos_fourTag){
          TString HistName = pair.first;
          HistName.Resize(HistName.Index("_FourPlusTags"));
          if(passed_selections[HistName]){
              pair.second.at(i)->Fill(val,weight.at(i));
          }
       }
     }
  }
}


void TH1Fs::Write(TDirectory *dir, std::string dirname){
     TDirectory* subsubdir = dir->mkdir(dirname.c_str());
     subsubdir->cd();
     for(auto pair: m_histos_twoTag){
       for(unsigned int i = 0; i < pair.second.size(); i++){
          pair.second.at(i)->Write();
       }
     }
     for(auto pair: m_histos_threeTag){
       for(unsigned int i = 0; i < pair.second.size(); i++){
          pair.second.at(i)->Write();
       }
     }
     for(auto pair: m_histos_fourTag){
       for(unsigned int i = 0; i < pair.second.size(); i++){
          pair.second.at(i)->Write();
       }
     }
     subsubdir->Write();
};

