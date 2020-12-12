#define EventLoop_cxx
#define _USE_MATH_DEFINES
#include <cmath>
#include "EventLoop.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>

void EventLoop::Loop()
{
    if (fChain == 0)
        return;
    // This takes the entries from fchain, fchain is set up in the "main.C" file. These entries are event data, each entry is 1 collition.
    Long64_t nentries = fChain->GetEntriesFast();
    Long64_t nbytes = 0, nb = 0;
    for (Long64_t jentry = 0; jentry < nentries; jentry++)
    {
        // This for loop takes each collition in the form of a tree data structure. After initilising the tags of the Higgs and 2 other tags I don't know yet, this code selects the jet's that may
        // contain the higgs though numerous methods that identify the expected value against the value seen.
        Long64_t ientry = LoadTree(jentry);
        if (ientry < 0)
            break;
        nb = fChain->GetEntry(jentry);
        nbytes += nb;

        if (EventReadout != 0)
        {
            if (jentry % EventReadout == 0)
            {
                std::cout << "Processing " << jentry << " events!!!" << std::endl;
            }
        }
        for (auto sel : mySel)
        {
            pass_sel[sel] = false;
        }
        m_NTags = 0;
        m_NTags_caloJ = 0;
        m_NTags_trkJ = 0;
        m_NTags_Higgs = 0;
        m_ntagsOutside = 0;
        m_MassTruth = 0;
        m_EventWeights.clear();
        m_EventWeights.push_back(EventWeight);
        //this

        SetJetVectors();
        bool status_W = false;
        bool status = false;
        m_mWT = GetMwt();
        m_MassTruth = GetTruthMass();
        Wminus = GetWBoson(status_W);
        // Key: Positively or a negatively charged lepton (LepN or LepP), a fat jet ("Merged"),  slimmer jets ("resolved"), background-enriched ("CR"), signal enriched ("SR").
        // This bool ensures that fat or slim jets are passed
        bool passed_merged_preselection = PassEventSelectionBoosted(met_ptv, lep_ptv, jet0_ptv, jet1_ptv, lep_jet0_angle, lep_jet1_angle, hw_angle, solo_jet_ptv);
        bool passed_resovled_preselction = PassEventSelectionResolved();
        if (!passed_merged_preselection && !passed_resovled_preselction)
            continue;

        /*if(Jets.size() >= 4 && Lepton_Charge < 0){
          MatchTruthParticlesToJets();
      }*/

        if (passed_merged_preselection)
        {
            if (Lepton_Charge > 0)
            {
                if ((Higgs.M() * 0.001 > hmlb && Higgs.M() * 0.001 < hmub))
                    pass_sel["Merged_LepP_SR"] = true;
                if (!(Higgs.M() * 0.001 > hmlb && Higgs.M() * 0.001 < hmub))
                    pass_sel["Merged_LepP_CR"] = true;
            }
            else if (Lepton_Charge < 0)
            {
                if (((Higgs.M() * 0.001 > hmlb && Higgs.M() * 0.001 < hmub) && (Wplus.M() * 0.001 > wmlb && Wplus.M() * 0.001 < wmub)))
                    pass_sel["Merged_LepN_SR"] = true;
                if (!((Higgs.M() * 0.001 > hmlb && Higgs.M() * 0.001 < hmub) && (Wplus.M() * 0.001 > wmlb && Wplus.M() * 0.001 < wmub)))
                    pass_sel["Merged_LepN_CR"] = true;
            }
        }

        // Look at ttthis
        passed_resovled_preselction = false;

        if (passed_resovled_preselction && !pass_sel["Merged_LepP_SR"] && !pass_sel["Merged_LepN_SR"])
        {
            if (Lepton_Charge > 0)
            {
                if (m_MaxMVA_Response > 0.7)
                {
                    pass_sel["Resolved_LepP_SR"] = true;
                    if (pass_sel["Merged_LepP_CR"] == true)
                        pass_sel["Merged_LepP_CR"] = false;
                }
                if (!pass_sel["Merged_LepP_CR"] && m_MaxMVA_Response > -0.5 && m_MaxMVA_Response < 0.3)
                    pass_sel["Resolved_LepP_CR"] = true;
            }
            else if (Lepton_Charge < 0)
            {
                if (m_MaxMVA_Response > -2.0)
                {
                    pass_sel["Resolved_LepN_SR"] = true;
                    if (pass_sel["Merged_LepN_CR"] == true)
                        pass_sel["Merged_LepN_CR"] = false;
                }
                if (!pass_sel["Merged_LepN_CR"] && m_MaxMVA_Response < 0.5)
                    pass_sel["Resolved_LepN_CR"] = true;
            }
        }

        if (pass_sel["Merged_LepN_CR"] || pass_sel["Resolved_LepN_CR"] || pass_sel["Merged_LepP_CR"] || pass_sel["Resolved_LepP_CR"] || pass_sel["Merged_LepN_SR"] || pass_sel["Resolved_LepN_SR"] || pass_sel["Merged_LepP_SR"] || pass_sel["Resolved_LepP_SR"])
        {
            h_MET->Fill(MET->Pt() * 0.001, m_EventWeights, pass_sel, m_NTags);
            h_METSig->Fill(METSig, m_EventWeights, pass_sel, m_NTags);
            h_Lepton_Eta->Fill(Lepton4vector->Eta(), m_EventWeights, pass_sel, m_NTags);
            h_Lepton_Pt->Fill(Lepton4vector->Pt() * 0.001, m_EventWeights, pass_sel, m_NTags);
            h_NBtags->Fill(m_NTags, m_EventWeights, pass_sel, m_NTags);
            h_Njets->Fill(Jets.size(), m_EventWeights, pass_sel, m_NTags);
            h_Mwt->Fill(m_mWT, m_EventWeights, pass_sel, m_NTags);
            h_MinDeltaPhiJETMET->Fill(m_min_DeltaPhiJETMET, m_EventWeights, pass_sel, m_NTags);
            h_HT->Fill(m_HT, m_EventWeights, pass_sel, m_NTags);
            h_HT_bjets->Fill(m_HT_bjets, m_EventWeights, pass_sel, m_NTags);
            h_HT_bjets_Lepton_Pt->Fill(m_HT_bjets + Lepton4vector->Pt() * 0.001, m_EventWeights, pass_sel, m_NTags);
            h_pTWminus->Fill(Wminus.Pt() * 0.001, m_EventWeights, pass_sel, m_NTags);
            h_mVH->Fill(m_mVH, m_EventWeights, pass_sel, m_NTags);
            h_DeltaPhi_HW->Fill(m_DeltaPhi_HW, m_EventWeights, pass_sel, m_NTags);
            h_maxMVAResponse->Fill(m_MaxMVA_Response, m_EventWeights, pass_sel, m_NTags);
            h_pTH->Fill(Higgs.Pt() * 0.001, m_EventWeights, pass_sel, m_NTags);
            h_pTWplus->Fill(Wplus.Pt() * 0.001, m_EventWeights, pass_sel, m_NTags);
            h_pTH_over_mVH->Fill(Higgs.Pt() * 0.001 / m_mVH, m_EventWeights, pass_sel, m_NTags);
            h_pTW_over_mVH->Fill(Wplus.Pt() * 0.001 / m_mVH, m_EventWeights, pass_sel, m_NTags);
            h_mH->Fill(Higgs.M() * 0.001, m_EventWeights, pass_sel, m_NTags);
            h_mWplus->Fill(Wplus.M() * 0.001, m_EventWeights, pass_sel, m_NTags);
            h_tagCategory->Fill(m_bTagCategory, m_EventWeights, pass_sel, m_NTags);
            h_mass_resolution->Fill((m_mVH - m_MassTruth) / m_MassTruth, m_EventWeights, pass_sel, m_NTags);
            h_MET_over_sqrtHT->Fill((MET->Pt() * 0.001) / (std::sqrt(m_HT)), m_EventWeights, pass_sel, m_NTags);
        }
        ////WriteMVAInput();
    }
}

int EventLoop::GetBTagCategoryShort(int NTags_InHiggsJet, int NTags_OutsideHiggsJet)
{
    int category = -1;
    if (NTags_InHiggsJet == 0 && NTags_OutsideHiggsJet >= 2)
        category = 2;
    if (NTags_InHiggsJet == 1 && NTags_OutsideHiggsJet == 1)
        category = 2;
    if (NTags_InHiggsJet >= 2 && NTags_OutsideHiggsJet == 0)
        category = 2;
    if (NTags_InHiggsJet == 1 && NTags_OutsideHiggsJet >= 2)
        category = 3;
    if (NTags_InHiggsJet >= 2 && NTags_OutsideHiggsJet == 1)
        category = 3;
    if (NTags_InHiggsJet >= 2 && NTags_OutsideHiggsJet >= 2)
        category = 4;
    return category;
}

int EventLoop::GetBTagCategory(int NTags_InHiggsJet, int NTags_OutsideHiggsJet)
{
    int category = -1;
    if (NTags_InHiggsJet == 0 && NTags_OutsideHiggsJet == 0)
        category = 0;
    if (NTags_InHiggsJet == 0 && NTags_OutsideHiggsJet == 1)
        category = 1;
    if (NTags_InHiggsJet == 0 && NTags_OutsideHiggsJet >= 2)
        category = 2;
    if (NTags_InHiggsJet == 1 && NTags_OutsideHiggsJet == 0)
        category = 3;
    if (NTags_InHiggsJet == 1 && NTags_OutsideHiggsJet == 1)
        category = 4;
    if (NTags_InHiggsJet == 1 && NTags_OutsideHiggsJet >= 2)
        category = 5;
    if (NTags_InHiggsJet >= 2 && NTags_OutsideHiggsJet == 0)
        category = 6;
    if (NTags_InHiggsJet >= 2 && NTags_OutsideHiggsJet == 1)
        category = 7;
    if (NTags_InHiggsJet >= 2 && NTags_OutsideHiggsJet >= 2)
        category = 8;
    return category;
}

void EventLoop::initializeMVA_qqbb()
{
    m_reader_qqbb = new TMVA::Reader("!Color:!Silent");
    m_reader_qqbb->AddVariable("btagjH1", &m_btagjH1);
    m_reader_qqbb->AddVariable("btagjH2", &m_btagjH2);
    m_reader_qqbb->AddVariable("btagjW1", &m_btagjWp1);
    m_reader_qqbb->AddVariable("btagjW2", &m_btagjWp2);
    m_reader_qqbb->AddVariable("H_mass", &m_H_mass);
    m_reader_qqbb->AddVariable("Wp_mass", &m_Wp_mass);
    m_reader_qqbb->AddVariable("Phi_HW", &m_Phi_HW);
    m_reader_qqbb->AddVariable("H_pT/mass_VH", &m_pTH_over_mvH);
    m_reader_qqbb->AddVariable("Wp_pT/mass_VH", &m_ptW_over_mvH);
    m_reader_qqbb->BookMVA("BDT", "dataset/weights/TMVAClassificationCategory_WpH_Tagger_v2.weights.xml");
}

void EventLoop::initializeMVA_lvbb()
{
    m_reader_lvbb = new TMVA::Reader("!Color:!Silent");
    m_reader_lvbb->AddVariable("btagjH1", &m_btagjH1);
    m_reader_lvbb->AddVariable("btagjH2", &m_btagjH2);
    m_reader_lvbb->AddVariable("H_mass", &m_H_mass);
    m_reader_lvbb->AddVariable("Phi_HW", &m_Phi_HW);
    m_reader_lvbb->AddVariable("pTHmvH", &m_pTH_over_mvH);
    m_reader_lvbb->AddVariable("pTWmvH", &m_ptW_over_mvH);
    m_reader_lvbb->BookMVA("BDT", "dataset/weights/TMVAClassificationCategory_WpH_Tagger_lvbb.weights.xml");
}

double EventLoop::EvaluateMVAResponse_qqbb(int i_H1, int i_H2, int i_w1, int i_w2)
{
    m_H_mass = (Jets.at(i_H1) + Jets.at(i_H2)).M() * 0.001;
    m_Wp_mass = (Jets.at(i_w1) + Jets.at(i_w2)).M() * 0.001;
    m_btagjH1 = (float)JetIsTagged.at(i_H1);
    m_btagjH2 = (float)JetIsTagged.at(i_H2);
    m_btagjWp1 = (float)JetIsTagged.at(i_w1);
    m_btagjWp2 = (float)JetIsTagged.at(i_w2);
    m_Phi_HW = fabs((Jets.at(i_H1) + Jets.at(i_H2)).DeltaPhi((Jets.at(i_w1) + Jets.at(i_w2))));
    m_pTH_over_mvH = (Jets.at(i_H1) + Jets.at(i_H2)).Pt() / (Jets.at(i_H1) + Jets.at(i_H2) + Jets.at(i_w1) + Jets.at(i_w2)).M();
    m_ptW_over_mvH = (Jets.at(i_w1) + Jets.at(i_w2)).Pt() / (Jets.at(i_H1) + Jets.at(i_H2) + Jets.at(i_w1) + Jets.at(i_w2)).M();
    return m_reader_qqbb->EvaluateMVA("BDT");
}

double EventLoop::EvaluateMVAResponse_lvbb(int i, int j, TLorentzVector W)
{
    TLorentzVector H = Jets.at(i) + Jets.at(j);
    TLorentzVector vH = H + W;
    m_btagjH1 = (float)JetIsTagged.at(i);
    m_btagjH2 = (float)JetIsTagged.at(j);
    m_H_mass = (Jets.at(i) + Jets.at(j)).M() * 0.001;
    m_Phi_HW = fabs((Jets.at(i) + Jets.at(j)).DeltaPhi(W));
    m_pTH_over_mvH = H.Pt() / vH.M();
    m_ptW_over_mvH = W.Pt() / vH.M();
    return m_reader_lvbb->EvaluateMVA("BDT");
}

void EventLoop::WriteMVAInput()
{
    m_MET = MET->Pt() * 0.001;
    m_Lep_PT = Lepton4vector->Pt() * 0.001;
    m_Wleptonic_pT = Wminus.Pt() * 0.001;
    m_Wleptonic_Eta = fabs(Wminus.Eta());
    m_is_Signal = 1;
    m_myTree->Fill();
}

double EventLoop::GetTruthMass()
{
    if (Higgs_LV)
    {
        return (*Higgs_LV + *Wplus_LV).M() * 0.001;
    }
    return 999;
}

void EventLoop::MatchTruthParticlesToJets()
{
    m_index_H1 = -99;
    m_index_H2 = -99;
    m_index_W1 = -99;
    m_index_W2 = -99;
    m_min_dRTruth = 999;
    bool status = false;
    if (Jets.size() < 4)
        return;
    for (unsigned int i = 0; i < Jets.size(); i++)
    {
        for (unsigned int j = i + 1; j < Jets.size(); j++)
        {
            for (unsigned int k = 0; k < Jets.size(); k++)
            {
                for (unsigned int l = k + 1; l < Jets.size(); l++)
                {
                    if (l == k || l == j || l == i || k == j || k == i || j == i)
                        continue;
                    TLorentzVector H = Jets.at(i) + Jets.at(j);
                    TLorentzVector W = Jets.at(k) + Jets.at(l);
                    double dRTruth = sqrt(pow(H.DeltaR(*Higgs_LV), 2) + pow(W.DeltaR(*Wplus_LV), 2));
                    if (m_min_dRTruth > dRTruth && H.DeltaR(*Higgs_LV) < 0.3 && W.DeltaR(*Wplus_LV) < 0.3)
                    {
                        m_min_dRTruth = dRTruth;
                        if (status == true)
                            FillMVATree(m_index_H1, m_index_H2, m_index_W1, m_index_W2, false);
                        m_index_H1 = i;
                        m_index_H2 = j;
                        m_index_W1 = k;
                        m_index_W2 = l;
                        status = true;
                    }
                    else
                    {
                        FillMVATree(i, j, k, l, false);
                    }
                }
            }
        }
    }
    if (status == true)
        FillMVATree(m_index_H1, m_index_H2, m_index_W1, m_index_W2, true);
}

void EventLoop::FillMVATree(int i_H1, int i_H2, int i_w1, int i_w2, bool is_signal)
{
    m_H_mass = (Jets.at(i_H1) + Jets.at(i_H2)).M() * 0.001;
    m_H_pT = (Jets.at(i_H1) + Jets.at(i_H2)).Pt() * 0.001;
    m_pTjH1 = Jets.at(i_H1).Pt() * 0.001;
    m_pTjH2 = Jets.at(i_H2).Pt() * 0.001;
    m_btagjH1 = (float)JetIsTagged.at(i_H1);
    m_btagjH2 = (float)JetIsTagged.at(i_H2);
    m_dRjjH = Jets.at(i_H1).DeltaR(Jets.at(i_H2));
    m_Wp_mass = (Jets.at(i_w1) + Jets.at(i_w2)).M() * 0.001;
    m_Wp_pT = (Jets.at(i_w1) + Jets.at(i_w2)).Pt() * 0.001;
    m_pTjWp1 = Jets.at(i_w1).Pt() * 0.001;
    m_pTjWp2 = Jets.at(i_w2).Pt() * 0.001;
    m_btagjWp1 = (float)JetIsTagged.at(i_w1);
    m_btagjWp2 = (float)JetIsTagged.at(i_w2);
    m_dRjjWp = Jets.at(i_H1).DeltaR(Jets.at(i_H2));
    m_Phi_HW = fabs((Jets.at(i_H1) + Jets.at(i_H2)).DeltaPhi((Jets.at(i_w1) + Jets.at(i_w2))));
    m_mass_VH = (Jets.at(i_H1) + Jets.at(i_H2) + Jets.at(i_w1) + Jets.at(i_w2)).M() * 0.001;
    m_is_Signal = is_signal;
    m_myTree->Fill();
}

bool EventLoop::FindFJetPair()
{
    bool status_W = false;
    bool status = false;
    if (Lepton_Charge < 0.)
    {
        if (nTaggedVRTrkJetsInFJet.at(0) != nTaggedVRTrkJetsInFJet.at(1))
        {
            Higgs = nTaggedVRTrkJetsInFJet.at(0) > nTaggedVRTrkJetsInFJet.at(1) ? FJets.at(0) : FJets.at(1);
            Wplus = nTaggedVRTrkJetsInFJet.at(0) < nTaggedVRTrkJetsInFJet.at(1) ? FJets.at(0) : FJets.at(1);
            m_NTags_Higgs = nTaggedVRTrkJetsInFJet.at(0) > nTaggedVRTrkJetsInFJet.at(1) ? nTaggedVRTrkJetsInFJet.at(0) : nTaggedVRTrkJetsInFJet.at(1);
        }
        else
        {
            Higgs = FJets.at(0).M() > FJets.at(1).M() ? FJets.at(0) : FJets.at(1);
            Wplus = FJets.at(0).M() < FJets.at(1).M() ? FJets.at(0) : FJets.at(1);
            m_NTags_Higgs = FJets.at(0).M() > FJets.at(1).M() ? nTaggedVRTrkJetsInFJet.at(0) : nTaggedVRTrkJetsInFJet.at(1);
        }
        m_ntagsOutside = m_NTags_trkJ - (nTaggedVRTrkJetsInFJet.at(0) + nTaggedVRTrkJetsInFJet.at(1));
        m_bTagCategory = GetBTagCategory(m_NTags_Higgs, m_ntagsOutside);
        m_NTags = GetBTagCategoryShort(m_NTags_Higgs, m_ntagsOutside);
        if (Higgs.Pt() > 250000)
            status = true;
    }
    else if (Lepton_Charge > 0.)
    {
        Higgs = FJets.at(0);
        Wplus = GetWBoson(status_W);
        if (status_W)
            status = true;
        m_ntagsOutside = m_NTags_trkJ - nTaggedVRTrkJetsInFJet.at(0);
        m_bTagCategory = GetBTagCategory(m_NTags_Higgs, m_ntagsOutside);
        m_NTags = m_NTags_trkJ;
    }
    m_DeltaPhi_HW = fabs(Wplus.DeltaPhi(Higgs));
    m_mVH = (Wplus + Higgs).M() * 0.001;
    return status;
}

bool EventLoop::FindJetPair_qqbb()
{
    m_index_H1 = -99;
    m_index_H2 = -99;
    m_index_W1 = -99;
    m_index_W2 = -99;
    bool status = false;
    m_MaxMVA_Response = -2;
    for (unsigned int i = 0; i < (Jets.size() < 6 ? Jets.size() : 6); i++)
    {
        for (unsigned int j = i + 1; j < (Jets.size() < 6 ? Jets.size() : 6); j++)
        {
            for (unsigned int k = 0; k < (Jets.size() < 6 ? Jets.size() : 6); k++)
            {
                for (unsigned int l = k + 1; l < (Jets.size() < 6 ? Jets.size() : 6); l++)
                {
                    if (l == k || l == j || l == i || k == j || k == i || j == i)
                        continue;
                    double mva_response = EvaluateMVAResponse_qqbb(i, j, k, l);
                    TLorentzVector H = Jets.at(i) + Jets.at(j);
                    TLorentzVector W = Jets.at(k) + Jets.at(l);
                    if (m_MaxMVA_Response < mva_response)
                    {
                        m_MaxMVA_Response = mva_response;
                        m_index_H1 = i;
                        m_index_H2 = j;
                        m_index_W1 = k;
                        m_index_W2 = l;
                        Wplus = Jets.at(m_index_W1) + Jets.at(m_index_W2);
                        Higgs = Jets.at(m_index_H1) + Jets.at(m_index_H2);
                        status = true;
                    }
                }
            }
        }
    }
    Set_Jet_observables();
    m_DeltaPhi_HW = fabs(Wplus.DeltaPhi(Higgs));
    m_mVH = (Wplus + Higgs).M() * 0.001;
    for (unsigned int i = 0; i < Jets.size(); i++)
    {
        if (i == m_index_H1 || i == m_index_H2 || i == m_index_W1 || i == m_index_W2)
            continue;
        if (JetIsTagged.at(i) >= m_btagCategoryBin)
            m_ntagsOutside++;
    }
    m_NTags_Higgs = (JetIsTagged.at(m_index_H1) >= m_btagCategoryBin) + (JetIsTagged.at(m_index_H2) >= m_btagCategoryBin);
    m_bTagCategory = GetBTagCategory(m_NTags_Higgs, m_ntagsOutside);
    m_NTags = GetBTagCategoryShort(m_NTags_Higgs, m_ntagsOutside);
    return status;
}

bool EventLoop::FindJetPair_lvbb()
{
    m_index_H1 = 1;
    m_index_H2 = 1;
    bool status = false;
    bool status_W = false;
    m_MaxMVA_Response = -2;
    for (int i = 0; i < Jets.size(); i++)
    {
        for (int j = i + 1; j < Jets.size(); j++)
        {
            if (i == j)
                continue;
            TLorentzVector W = GetWBoson(status_W);
            TLorentzVector H = Jets.at(i) + Jets.at(j);
            double mva_response_lvbb = EvaluateMVAResponse_lvbb(i, j, W);
            if (m_MaxMVA_Response < mva_response_lvbb)
            {
                m_MaxMVA_Response = mva_response_lvbb;
                m_index_H1 = i;
                m_index_H2 = j;
                Wplus = W;
                Higgs = H;
                status = true;
            }
        }
    }
    Set_Jet_observables();
    m_DeltaPhi_HW = fabs(Wplus.DeltaPhi(Higgs));
    m_mVH = (Wplus + Higgs).M() * 0.001;
    for (unsigned int i = 0; i < Jets.size(); i++)
    {
        if (i == m_index_H1 || i == m_index_H2)
            continue;
        if (JetIsTagged.at(i) >= m_btagCategoryBin)
            m_ntagsOutside++;
    }
    m_NTags_Higgs = (JetIsTagged.at(m_index_H1) >= m_btagCategoryBin) + (JetIsTagged.at(m_index_H2) >= m_btagCategoryBin);
    m_bTagCategory = GetBTagCategory(m_NTags_Higgs, m_ntagsOutside);
    m_NTags = m_NTags_caloJ;
    return status;
}

TLorentzVector EventLoop::GetWBoson(bool &status)
{
    status = false;
    TLorentzVector Wleptonic;
    std::vector<TLorentzVector *> neutrinoVector = GetNeutrinos(Lepton4vector, MET);
    for (auto neutrino : neutrinoVector)
    {
        Wleptonic = (*neutrino + *Lepton4vector);
        status = true;
    }
    return Wleptonic;
}

std::vector<TLorentzVector *> EventLoop::GetNeutrinos(TLorentzVector *L, TLorentzVector *MET)
{
    std::vector<TLorentzVector *> neutrinoVector;
    neutrinoVector = m_NeutrinoBuilder->candidatesFromWMass_Rotation(L, MET, true);
    bool m_isRotatedSol = m_NeutrinoBuilder->m_isRotated;
    double m_r = m_NeutrinoBuilder->m_r;
    return neutrinoVector;
}

void EventLoop::Set_Jet_observables()
{
    m_min_DeltaPhiJETMET = 999;
    m_HT = 0;
    m_HT_bjets = 0;
    m_maxEta_bjets = 0;
    m_maxPT_bjets = 0;
    int i = 0;
    for (auto jet : Jets)
    {
        double DeltaPhiJETMET = fabs(jet.DeltaPhi(*MET));
        if (DeltaPhiJETMET < m_min_DeltaPhiJETMET)
        {
            m_min_DeltaPhiJETMET = DeltaPhiJETMET;
        }
        m_HT += jet.Pt() * 0.001;
        if (JetIsTagged.at(i) >= m_btagCategoryBin)
        {
            m_HT_bjets += jet.Pt() * 0.001;
            if (m_maxEta_bjets < fabs(jet.Eta()))
            {
                m_maxEta_bjets = fabs(jet.Eta());
            }
            if (m_maxPT_bjets < jet.Pt() * 0.001)
            {
                m_maxPT_bjets = jet.Pt() * 0.001;
            }
        }
        i++;
    }
}

bool EventLoop::PassEventSelectionBoosted(Float_t met_ptv, Float_t lep_ptv, Float_t jet0_ptv, Float_t jet1_ptv, Float_t lep_jet0_angle, Float_t lep_jet1_angle,
                                          Float_t hw_angle, Float_t solo_jet_ptv)
{
    if (MET->Pt() < met_ptv)
        return false;
    if (Lepton4vector->Pt() < lep_ptv)
        return false;
    if (Lepton_Charge < 0)
    {
        if (FJets.size() < 2)
            return false;
        if (FJets.at(0).Pt() < jet0_ptv)
            return false;
        if (FJets.at(1).Pt() < jet1_ptv)
            return false;
        if (FJets.at(0).DeltaR(*Lepton4vector) < lep_jet0_angle)
            return false;
        if (FJets.at(1).DeltaR(*Lepton4vector) < lep_jet1_angle)
            return false;
        if (!FindFJetPair())
            return false;
        if (m_DeltaPhi_HW < hw_angle)
            return false;
    }
    else
    {
        ///if(MET->Pt() < 30000)return false;             ///  increase MET pT cut !?!?!
        ///if(Lepton4vector->Pt() < 30000)return false;   ///  increase lepton pT cut ?!?!
        if (FJets.size() < 1)
            return false;
        if (FJets.at(0).Pt() < solo_jet_ptv)
            return false;
        if (!FindFJetPair())
            return false;
    }
    return true;
}

bool EventLoop::PassEventSelectionResolved()
{
    if (MET->Pt() < 0.)
        return false;
    if (Lepton4vector->Pt() < 30000)
        return false;
    if (Lepton_Charge < 0)
    {
        if (m_NTags_caloJ < 2)
            return false;
        if (Jets.size() < 4)
            return false;
        ///if(Jets.size()   < 5)return false;
        if (FindJetPair_qqbb() == false)
            return false;
        ////if(Higgs.Pt()*0.001 < 100.)return false;
        ////if(Wplus.Pt()*0.001 < 100.)return false;
        return true;
    }
    else
    {
        if (m_NTags_caloJ < 2)
            return false;
        if (Jets.size() < 4)
            return false;
        if (FindJetPair_lvbb() == false)
            return false;
        if (Higgs.Pt() * 0.001 < 100.)
            return false;
        if (Wplus.Pt() * 0.001 < 120.)
            return false;
        return true;
    }
    return true;
}

double EventLoop::GetMwt()
{
    return 0.001 * sqrt(2. * Lepton4vector->Pt() * MET->Pt() * (1. - cos(Lepton4vector->DeltaPhi(*MET))));
}

void EventLoop::SetJetVectors()
{
    Jets.clear();
    JetIsTagged.clear();
    TrkJets.clear();
    TrkJetIsTagged.clear();
    FJets.clear();
    nTaggedVRTrkJetsInFJet.clear();
    TLorentzVector jet, trkjet;
    for (int i = 0; i < signal_Jet_PT->size(); i++)
    {
        jet.SetPtEtaPhiM(signal_Jet_PT->at(i), signal_Jet_Eta->at(i), signal_Jet_Phi->at(i), signal_Jet_M->at(i));
        Jets.push_back(jet);
        JetIsTagged.push_back(GetTagWeightBin(btag_score_signalJet->at(i)));
        if (btag_score_signalJet->at(i) > m_btagCut_value_CaloJets)
            m_NTags_caloJ++;
    }
    for (int i = 0; i < forward_Jet_PT->size(); i++)
    {
        jet.SetPtEtaPhiM(forward_Jet_PT->at(i), forward_Jet_Eta->at(i), forward_Jet_Phi->at(i), forward_Jet_M->at(i));
        Jets.push_back(jet);
        JetIsTagged.push_back(GetTagWeightBin(btag_score_forwardJet->at(i)));
        if (btag_score_forwardJet->at(i) > m_btagCut_value_CaloJets)
            m_NTags_caloJ++;
    }
    for (int i = 0; i < FatJet_M->size(); i++)
    {
        if (FatJet_PT->at(i) < 200000)
            continue;
        if (FatJet_M->at(i) < 50000)
            continue;
        jet.SetPtEtaPhiM(FatJet_PT->at(i), FatJet_Eta->at(i), FatJet_Phi->at(i), FatJet_M->at(i));
        FJets.push_back(jet);
        int nMatchedAndTaggedJets = 0;
        for (int i = 0; i < TrackJet_PT->size(); i++)
        {
            trkjet.SetPtEtaPhiM(TrackJet_PT->at(i), TrackJet_Eta->at(i), TrackJet_Phi->at(i), TrackJet_M->at(i));
            if (jet.DeltaR(trkjet) < 1.0 && TrackJet_btagWeight->at(i) > m_btagCut_value_trkJets)
                nMatchedAndTaggedJets++;
        }
        nTaggedVRTrkJetsInFJet.push_back(nMatchedAndTaggedJets);
    }
    for (int i = 0; i < TrackJet_PT->size(); i++)
    {
        jet.SetPtEtaPhiM(TrackJet_PT->at(i), TrackJet_Eta->at(i), TrackJet_Phi->at(i), TrackJet_M->at(i));
        TrkJets.push_back(jet);
        if (TrackJet_btagWeight->at(i) > m_btagCut_value_trkJets)
        {
            TrkJetIsTagged.push_back(1);
            m_NTags_trkJ++;
        }
        else
        {
            TrkJetIsTagged.push_back(0);
        }
    }
    Sort_Jets(&FJets, &nTaggedVRTrkJetsInFJet);
    Sort_Jets(&Jets, &JetIsTagged);
}

int EventLoop ::GetTagWeightBin(double btag_score)
{
    if (btag_score < 0.11)
        return 0; /// 100% - 85%
    if (btag_score < 0.64)
        return 1; /// 85%  - 77%
    if (btag_score < 0.83)
        return 2; /// 77%  - 70%
    if (btag_score < 0.94)
        return 3; /// 70%  - 60%
    return 4;     /// 60%
}

void EventLoop ::Sort_Jets(std::vector<TLorentzVector> *Jets, std::vector<int> *is_tagged)
{
    bool bDone = false;
    while (!bDone)
    {
        bDone = true;
        for (unsigned int i = 0; i < Jets->size() - 1 && Jets->size() > 0; i++)
        {
            if (Jets->at(i).Pt() < Jets->at(i + 1).Pt())
            {
                TLorentzVector tmp_jet = Jets->at(i);
                Jets->at(i) = Jets->at(i + 1);
                Jets->at(i + 1) = tmp_jet;
                int tmp_tagging_info = is_tagged->at(i);
                is_tagged->at(i) = is_tagged->at(i + 1);
                is_tagged->at(i + 1) = tmp_tagging_info;
                bDone = false;
            }
        }
    }
}

void EventLoop::Write(TDirectory *dir, std::string dirname)
{
    h_MET->Write(dir, ("MET"));
    h_METSig->Write(dir, ("METSig"));
    h_MinDeltaPhiJETMET->Write(dir, ("MinDeltaPhiJETMET"));
    h_Mwt->Write(dir, ("Mwt"));
    h_Lepton_Eta->Write(dir, ("Lepton_Eta"));
    h_Lepton_Pt->Write(dir, ("Lepton_Pt"));
    h_Njets->Write(dir, ("nJets"));
    h_NBtags->Write(dir, ("nBTags"));
    h_HT->Write(dir, ("HT"));
    h_HT_bjets->Write(dir, ("HT_bjets"));
    h_HT_bjets_Lepton_Pt->Write(dir, ("HT_bjets_Lepton_Pt"));
    h_mVH->Write(dir, ("mVH"));
    h_DeltaPhi_HW->Write(dir, ("DeltaPhi_HW"));
    h_pTH->Write(dir, ("pTH"));
    h_pTH_over_mVH->Write(dir, ("pTH_over_mVH"));
    h_pTWplus->Write(dir, ("pTWplus"));
    h_pTW_over_mVH->Write(dir, ("pTW_over_mVH"));
    h_pTWminus->Write(dir, ("pTWminus"));
    h_mH->Write(dir, ("mH"));
    h_mWplus->Write(dir, ("mWplus"));
    h_maxMVAResponse->Write(dir, ("maxMVAResponse"));
    h_tagCategory->Write(dir, ("BtagCategory"));
    h_mass_resolution->Write(dir, ("mass_resolution"));
    h_MET_over_sqrtHT->Write(dir, ("MET_over_rootHT"));
    dir->cd();
    m_myTree->Write();
}
