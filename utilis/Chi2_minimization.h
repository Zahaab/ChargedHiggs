	#ifndef Chi2_minimization_H
	#define Chi2_minimization_H
	
	#include<iostream>
	#include <string>
	#include <vector>
	#include "TLorentzVector.h"
	#include "NeutrinoBuilder.h"
	
	
	class Chi2_minimization{
	 public:
	  Chi2_minimization(std::string units="GeV");
	  virtual ~Chi2_minimization();
	
	  enum WReco {ROTATION, REALPART, DECREASING};
	  
	 //~ std::vector<TLorentzVector*> GetNeutrinos(TLorentzVector*, TLorentzVector*);
	 private:
	  Chi2_minimization(const Chi2_minimization&);
	  Chi2_minimization& operator=(const Chi2_minimization&);
	  
	  //~ std::vector<TLorentzVector*> GetNeutrinoPz(double MET, double MET_phi, const TLorentzVector &lepVec, double &nu_pz1, double &nu_pz2);
	  
	  
	  double MjjP,  SMjjP,  m_TopMinusW_had_mean,  m_TopMinusW_had_sigma,  m_Top_lep_mean,  m_Top_lep_sigma, m_PtDiff_mean, m_PtDiff_sigma, m_PtDiffRel_mean, m_PtDiffRel_sigma, m_PtDiffRelMass_mean, m_PtDiffRelMass_sigma, MTHJJ, STHJJ;
	  double m_WhChi2Value,m_ThWhChi2Value,m_TlChi2Value,m_PtDiffChi2Value;
	  int    m_debug;
	  WReco  m_WReco;
	  double m_Units;
	  NeutrinoBuilder* m_NeutrinoBuilder;
	  double m_highJetMass;
	  int m_category;
	  
	  double m_r;
	  bool m_isRotatedSol;
	  
	  
	  
	  double res_chi2All, res_chi2WH, res_chi2TopH, res_chi2TopL, res_Mtl, res_Mwh, res_Mth, res_Mtt;
	  TLorentzVector res_Tt;
	  int m_nChi2Values;

	 public:
	  void Init();
	  void Reset();

	
	  bool findMinChiSquare(TLorentzVector*,
                                const std::vector<TLorentzVector*>*, 
                                const std::vector<bool>*, 
                                TLorentzVector*, 
                                int&, 
                                int&, 
                                int&, 
                                int&, 
                                int&, 
                                double&, 
                                double&, 
                                double&);
          bool Reconstruct_HadronicSide(std::vector<TLorentzVector*>* jetVector, 
                                        int& i_q1_W, 
                                        int& i_q2_W, 
                                        int& i_b_had,
                                        double& chi2ming1H);
          
          bool Reconstruct_Hadronic_VH(std::vector<TLorentzVector*>* jetVector,
                                       int& i_q1_W,
                                       int& i_q2_W,
                                       int& i_b1_H,
                                       int& i_b2_H ,
                                       double& chi2ming1H);
	
          bool Reconstruct_LeptonicSide(TLorentzVector* L, 
                                        TLorentzVector* MET, 
                                        const std::vector<TLorentzVector*>* jetVector, 
                                        int& i_b_lep, 
                                        double& chi2ming1L);
          
          std::vector<TLorentzVector*> GetNeutrinos(TLorentzVector* L, TLorentzVector* MET);
         
	};
	
	
	#endif
