

#ifndef NeutrinoBuilder_H
#define NeutrinoBuilder_H

#include <iostream>
#include <string>

// ROOT classes
#include <TLorentzVector.h>
#include <TMinuit.h>
//#include <TUUID.h>

class NeutrinoBuilder{

 public:
  NeutrinoBuilder(std::string units);
  ~NeutrinoBuilder();
  NeutrinoBuilder(const NeutrinoBuilder&);
  NeutrinoBuilder& operator=(const NeutrinoBuilder&);
  
  inline void setdebuglevel(int level){m_debug = level;};
  
  Double_t getDiscriminant(const TLorentzVector*, const Double_t, const Double_t);
  // In case of negative discriminant, decrease the MET
  bool candidatesFromWMass_Scaling(const TLorentzVector*, double, Double_t, std::vector<TLorentzVector*>&);
  std::vector<TLorentzVector*> candidatesFromWMass_Scaling(const TLorentzVector*, const Double_t, const Double_t);
  std::vector<TLorentzVector*> candidatesFromWMass_Scaling(const TLorentzVector*, const TLorentzVector*);
  // In case of negative discriminant, rotate the MET
  std::vector<TLorentzVector*> candidatesFromWMass_Rotation(const TLorentzVector*,  const Double_t, const Double_t, const bool);
  std::vector<TLorentzVector*> candidatesFromWMass_Rotation(const TLorentzVector*,  const TLorentzVector*, const bool);
  // In case of negative discriminant, use the real part
  std::vector<TLorentzVector*> candidatesFromWMass_RealPart(const TLorentzVector*,  const Double_t, const Double_t, const bool);
  std::vector<TLorentzVector*> candidatesFromWMass_RealPart(const TLorentzVector*,  const TLorentzVector*, const bool);

  bool m_isRotated;
  double m_r;

 protected:
  double fitAlpha(const TLorentzVector*, const Double_t, const Double_t);
  int m_debug;
  double m_Units;  
  
};

#endif
