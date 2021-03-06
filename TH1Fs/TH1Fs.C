#include "TH1Fs.h"

void TH1Fs::Fill(double val, std::vector<double> weight, map<TString, bool> passed_selections, int NTags)
{

   if (NTags == 2)
   {
      for (unsigned int i = 0; i < weight.size(); i++)
      {
         for (auto pair : m_histos_twoTag)
         {
            TString HistName = pair.first;
            HistName.Resize(HistName.Index("_TwoTags"));
            if (passed_selections[HistName])
            {
               pair.second.at(i)->Fill(val, weight.at(i));
            }
         }
      }
   }
   else if (NTags == 3)
   {
      for (unsigned int i = 0; i < weight.size(); i++)
      {
         for (auto pair : m_histos_threeTag)
         {
            TString HistName = pair.first;
            HistName.Resize(HistName.Index("_ThreeTags"));
            if (passed_selections[HistName])
            {
               pair.second.at(i)->Fill(val, weight.at(i));
            }
         }
      }
   }
   else if (NTags > 3)
   {
      for (unsigned int i = 0; i < weight.size(); i++)
      {
         for (auto pair : m_histos_fourTag)
         {
            TString HistName = pair.first;
            HistName.Resize(HistName.Index("_FourPlusTags"));
            if (passed_selections[HistName])
            {
               pair.second.at(i)->Fill(val, weight.at(i));
            }
         }
      }
   }
}

void TH1Fs::Write(TDirectory *dir, std::string dirname)
{
   TDirectory *subsubdir = dir->mkdir(dirname.c_str());
   subsubdir->cd();
   for (auto pair : m_histos_twoTag)
   {
      for (unsigned int i = 0; i < pair.second.size(); i++)
      {
         pair.second.at(i)->Write();
      }
   }
   for (auto pair : m_histos_threeTag)
   {
      for (unsigned int i = 0; i < pair.second.size(); i++)
      {
         pair.second.at(i)->Write();
      }
   }
   for (auto pair : m_histos_fourTag)
   {
      for (unsigned int i = 0; i < pair.second.size(); i++)
      {
         pair.second.at(i)->Write();
      }
   }
   subsubdir->Write();
}

const map<TString, std::vector<TH1F *>> TH1Fs::GetTwoTagHistos() const { return m_histos_twoTag; }
const map<TString, std::vector<TH1F *>> TH1Fs::GetThreeTagHistos() const { return m_histos_threeTag; }
const map<TString, std::vector<TH1F *>> TH1Fs::GetFourTagHistos() const { return m_histos_fourTag; }

void TH1Fs::Sumw2()
{
   for (auto const &pair : m_histos_twoTag)
   {
      for (auto histo_two : m_histos_twoTag[pair.first])
      {
         histo_two->Sumw2();
      }
   }
   for (auto const &pair : m_histos_threeTag)
   {
      for (auto histo_three : m_histos_threeTag[pair.first])
      {
         histo_three->Sumw2();
      }
   }
   for (auto const &pair : m_histos_fourTag)
   {
      for (auto histo_four : m_histos_fourTag[pair.first])
      {
         histo_four->Sumw2();
      }
   }
}
