bool EventLoop::PassEventSelectionBoosted()
{
    if (MET->Pt() < 30000)
        return false;
    if (Lepton4vector->Pt() < 30000)
        return false;
    if (Lepton_Charge < 0)
    {
        if (FJets.size() < 2)
            return false;
        if (FJets.at(0).Pt() < 200000)
            return false;
        if (FJets.at(1).Pt() < 200000)
            return false;
        if (FJets.at(0).DeltaR(*Lepton4vector) < 1.0)
            return false;
        if (FJets.at(1).DeltaR(*Lepton4vector) < 1.0)
            return false;
        if (!FindFJetPair())
            return false;
        if (m_DeltaPhi_HW < 2.5)
            return false;
    }
    else
    {
        ///if(MET->Pt() < 30000)return false;             ///  increase MET pT cut !?!?!
        ///if(Lepton4vector->Pt() < 30000)return false;   ///  increase lepton pT cut ?!?!
        if (FJets.size() < 1)
            return false;
        if (FJets.at(0).Pt() < 250000)
            return false;
        if (!FindFJetPair())
            return false;
    }
    return true;
}