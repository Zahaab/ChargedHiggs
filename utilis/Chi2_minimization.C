
/* **********************************************************************
 *     Class   : Chi2_minimization
 *     Author  : LPC-ClermontFerrand team
 ************************************************************************/

#include "Chi2_minimization.h"

Chi2_minimization::Chi2_minimization(std::string units)
{
  m_debug = 0;
  m_WReco = ROTATION;
  m_r = 0.0;
  m_isRotatedSol = false;

  if (units == "MeV")
    m_Units = 1000.;
  else if (units == "GeV")
    m_Units = 1.;
  else
    std::cerr << "WARNING in Chi2_minimization: units different from GeV or MeV" << std::endl;
  m_NeutrinoBuilder = new NeutrinoBuilder(units);
  Init();
}

Chi2_minimization::~Chi2_minimization()
{
  if (m_debug > 0)
    std::cout << "in destructor " << std::endl;
  if (m_NeutrinoBuilder)
    delete m_NeutrinoBuilder;
}

void Chi2_minimization::Init()
{
  //Rel17.2: values obtained for Z' 0.5TeV-2 TeV including njets>=5 events
  //         LC jets + Jet Area correction
  //~ MjjP=82.41*m_Units;
  //~ SMjjP=9.553*m_Units;

  //~ m_TopMinusW_had_mean=89.01*m_Units;
  //~ m_TopMinusW_had_sigma=15.67*m_Units;

  //~ m_Top_lep_mean=166*m_Units;
  //~ m_Top_lep_sigma=17.48*m_Units;

  //~ m_PtDiff_mean=0.4305*m_Units;
  //~ m_PtDiff_sigma=46.07*m_Units;

  //~ m_PtDiffRel_mean=0.00144;
  //~ m_PtDiffRel_sigma=0.07837;

  //~ m_PtDiffRelMass_mean=0.0004532;
  //~ m_PtDiffRelMass_sigma=0.05112;

  //~ MTHJJ=171.8*m_Units;
  //~ STHJJ=16.04*m_Units;

  //~ switch (version){
  //~ case DATA2015_MC15C:{
  // TopAnalysis 2.4.12
  // Parton matching: HQTTtResonancesTools
  // Using MC15C derivations

  MjjP = 80.51 * m_Units;
  SMjjP = 12.07 * m_Units;

  m_TopMinusW_had_mean = 85.17 * m_Units;
  m_TopMinusW_had_sigma = 16.05 * m_Units;

  m_Top_lep_mean = 167.36 * m_Units;
  m_Top_lep_sigma = 25.41 * m_Units;

  m_PtDiff_mean = -0.23 * m_Units;
  m_PtDiff_sigma = 18.85 * m_Units;

  m_PtDiffRel_mean = -0.0012;
  m_PtDiffRel_sigma = 0.0048;

  m_PtDiffRelMass_mean = -0.0012;
  m_PtDiffRelMass_sigma = 0.0419;

  MTHJJ = 175.04 * m_Units;
  STHJJ = 14.87 * m_Units;
  //~ break;
  //~ }
  //~ case DATA2015_MC15:{
  //~ MjjP=83.65*m_Units;
  //~ SMjjP=8.37*m_Units;

  //~ m_TopMinusW_had_mean=91.58*m_Units;
  //~ m_TopMinusW_had_sigma=11.09*m_Units;

  //~ m_Top_lep_mean=167.56*m_Units;
  //~ m_Top_lep_sigma=21.82*m_Units;

  //~ m_PtDiff_mean=-0.75*m_Units;
  //~ m_PtDiff_sigma=34.69*m_Units;

  //~ m_PtDiffRel_mean=-0.0012;
  //~ m_PtDiffRel_sigma=0.0048;

  //~ m_PtDiffRelMass_mean=-0.0012;
  //~ m_PtDiffRelMass_sigma=0.0419;

  //~ MTHJJ=175.04*m_Units;
  //~ STHJJ=14.87*m_Units;
  //~ break;
  //~ }
  //~ }
}

bool Chi2_minimization::Reconstruct_HadronicSide(std::vector<TLorentzVector *> *jetVector, int &i_q1_W, int &i_q2_W, int &i_b_had, double &chi2ming1H)
{
  i_q1_W = -1;
  i_q2_W = -1;
  i_b_had = -1;
  chi2ming1H = 1e7;
  bool status = false;
  for (unsigned int i = 0; i < jetVector->size(); i++)
  {
    const TLorentzVector *I = jetVector->at(i);
    for (unsigned int j = i + 1; j < jetVector->size(); j++)
    {
      const TLorentzVector *J = jetVector->at(j);
      for (unsigned int k = 0; k < jetVector->size(); k++)
      {
        if (k == i || k == j)
          continue;
        const TLorentzVector *K = jetVector->at(k);
        TLorentzVector TopH = (*I) + (*J) + (*K);
        TLorentzVector Whad = (*I) + (*J);
        double chi2WH = pow((Whad.M() - MjjP) / SMjjP, 2);
        double chi2H = chi2WH + pow((TopH.M() - Whad.M() - m_TopMinusW_had_mean) / m_TopMinusW_had_sigma, 2);
        if (chi2ming1H > chi2H)
        {
          chi2ming1H = chi2H;
          i_q1_W = i;
          i_q2_W = j;
          i_b_had = k;
          status = true;
        }
      } /// end k
    }   /// end j
  }     /// end i
  return status;
}

bool Chi2_minimization::Reconstruct_Hadronic_VH(std::vector<TLorentzVector *> *jetVector, int &i_q1_W, int &i_q2_W, int &i_b1_H, int &i_b2_H, double &chi2ming1H)
{
  i_q1_W = -1;
  i_q2_W = -1;
  i_b1_H = -1;
  i_b2_H = -1;
  chi2ming1H = 1e7;
  bool status = false;
  for (unsigned int i = 0; i < jetVector->size(); i++)
  {
    const TLorentzVector *I = jetVector->at(i);
    for (unsigned int j = 0; j < jetVector->size(); j++)
    {
      const TLorentzVector *J = jetVector->at(j);
      if (j == i)
        continue;
      for (unsigned int k = 0; k < jetVector->size(); k++)
      {
        const TLorentzVector *K = jetVector->at(k);
        if (k == j || k == i)
          continue;
        for (unsigned int l = 0; l < jetVector->size(); l++)
        {
          const TLorentzVector *L = jetVector->at(k);
          if (l == k || l == j || l == i)
            continue;
          TLorentzVector Higgs = (*I) + (*J);
          TLorentzVector Whad = (*K) + (*L);
          double chi2WH = pow((Whad.M() - MjjP) / SMjjP, 2);
          double chi2Higgs = pow((Higgs.M() - 125. * m_Units) / SMjjP, 2); /// SMjjP -> Need to derive this value for hadronic Higgs decay !!!
          double chi2H = chi2WH + chi2Higgs;
          if (chi2ming1H > chi2H)
          {
            chi2ming1H = chi2H;
            i_q1_W = k;
            i_q2_W = l;
            i_b1_H = i;
            i_b2_H = j;
            status = true;
          }
        } /// end l
      }   /// end k
    }     /// end j
  }       /// end i
  return status;
}

bool Chi2_minimization::Reconstruct_LeptonicSide(TLorentzVector *L, TLorentzVector *MET, const std::vector<TLorentzVector *> *jetVector, int &i_b_lep, double &chi2ming1L)
{
  i_b_lep = -1;
  chi2ming1L = 1e7;
  bool status = false;
  if (L == NULL)
  {
    return false;
  }
  std::vector<TLorentzVector> Vecs;
  std::vector<TLorentzVector *> neutrinoVector = GetNeutrinos(L, MET);

  for (unsigned int n = 0; n < neutrinoVector.size(); n++)
  {
    TLorentzVector *N = neutrinoVector.at(n);
    TLorentzVector Wlv = (*N) + (*L);
    for (unsigned int m = 0; m < jetVector->size(); m++)
    {
      const TLorentzVector *M = jetVector->at(m);
      TLorentzVector Tlv = Wlv + (*M);
      double chi2L = pow((Tlv.M() - m_Top_lep_mean) / m_Top_lep_sigma, 2);
      if (chi2L < chi2ming1L)
      {
        chi2ming1L = chi2L;
        i_b_lep = m;
        MET = N;
        status = true;
      }
    }
  }

  return status;
}

//~ void Chi2_minimization::getNeutrinoPz (double MET, double MET_phi, const TLorentzVector &lepVec, double &nu_pz1, double &nu_pz2) {
//~ // This code gives results identical (except using a slightly different mW) to:
//~ // https://svnweb.cern.ch/trac/atlasphys-exa/browser/Physics/Exotic/Analysis/DibosonResonance/
//~ // Data2015/VV_JJ/Code/trunk/CxAODReader_DB/Root/AnalysisReader_DB.cxx?rev=239154#L812
//~ double mW = 80385.; // PDG 2014

//~ double el  = lepVec.E();
//~ double ptl = lepVec.Pt();
//~ double pzl = lepVec.Pz();

//~ TLorentzVector metVec;

//~ metVec.SetPtEtaPhiM(MET, 0, MET_phi, 0);

//~ double mu    = 0.5 * mW * mW + ptl * MET * cos(lepVec.DeltaPhi(metVec));
//~ double delta = (mu * mu * pzl * pzl / (pow(ptl, 4))) - (el * el * MET * MET - mu * mu) / (ptl * ptl);

//~ if (delta < 0) {
//~ delta = 0;
//~ }

//~ nu_pz1 = (mu * pzl / (ptl * ptl)) + sqrt(delta);
//~ nu_pz2 = (mu * pzl / (ptl * ptl)) - sqrt(delta);
//~ } // getNeutrinoPz

//~ std::vector<TLorentzVector> Chi2_minimization::getNeutrinoPz (double_t MET, double_t MET_phi, const TLorentzVector &lepVec) {
//~ double nu_pz1;
//~ double nu_pz2;
//~ getNeutrinoPz(MET, MET_phi, lepVec, nu_pz1, nu_pz2);
//~ std::vector<TLorentzVector> Vecs;
//~ TLorentzVector VecPz1, VecPz2;
//~ VecPz1.SetPtEtaPhiM(MET,0.0,MET_phi,0.0);
//~ VecPz2.SetPtEtaPhiM(MET,0.0,MET_phi,0.0);
//~ VecPz1.SetPz(nu_pz1);
//~ VecPz2.SetPz(nu_pz2);
//~ Vecs.push_back(VecPz1);
//~ Vecs.push_back(VecPz2);
//~ std::cout <<"pz "<< VecPz2.Pz()<<std::endl;
//~ std::cout <<"pt "<< VecPz2.Pt()<<std::endl;
//~ std::cout <<"M "<< VecPz2.M()<<std::endl;
//~ std::cout <<"phi "<< VecPz2.Phi()<<std::endl;

//~ return Vecs;
//~ if (fabs(nu_pz1) < fabs(nu_pz2)) {
//~ if (min) return VecPz1;

//~ return VecPz2;
//~ }
//~ if (min) return VecPz2;
//~ return VecPz1;
//~ }

std::vector<TLorentzVector *> Chi2_minimization::GetNeutrinos(TLorentzVector *L, TLorentzVector *MET)
{
  std::vector<TLorentzVector *> neutrinoVector;

  if (m_WReco == ROTATION)
  {
    neutrinoVector = m_NeutrinoBuilder->candidatesFromWMass_Rotation(L, MET, /*m_useSmallestPz=*/false);
    m_isRotatedSol = m_NeutrinoBuilder->m_isRotated;
    m_r = m_NeutrinoBuilder->m_r;
  }
  else if (m_WReco == REALPART)
    neutrinoVector = m_NeutrinoBuilder->candidatesFromWMass_RealPart(L, MET, /*m_useSmallestPz=*/false);
  else if (m_WReco == DECREASING)
    neutrinoVector = m_NeutrinoBuilder->candidatesFromWMass_Scaling(L, MET);

  return neutrinoVector;
}
