def configParser(path):
    config = {}
    with open(path) as fp:
        for line in fp:
            key_val = line.replace(" ", "").replace("\n", "").split("=")
            config[key_val[0]] = key_val[1]
    del config["-----------"]
    del config["------------"]
    return config


# var is either Stack_ , Plot_ , Graph_ , Btag_ that give dataPeriodes, Plotting event catagories, Graph names, Btagging choice respectively.
def getConfigData(config, var):
    DataPeriodes = [key.replace(
        var, "") for key in config if var in key and config[key] == "Enable"]
    return DataPeriodes


def getPlotFiles(config, MCDataPeriode):
    Plots_Enabled = getConfigData(config, "Plot_")
    PlotFile_Paths = {}
    for i in Plots_Enabled:
        PlotFile_Paths[i] = str(i + "_" + config["WP"] + "_" + MCDataPeriode + "_" + config["Higgs_mass_lower_bound"] + "-" + config["Higgs_mass_upper_bound"] + "-" +
                                config["Wboson_mass_lower_bound"] + "-" + config["Wboson_mass_upper_bound"] + "-" + config["Missing_transverse_momentum"] + "-" +
                                config["Lepton_transverse_momentum"] + "-" + config["2Jets_Jet1_transverse_momentum"] + "-" +
                                config["2Jets_Jet2_transverse_momentum"] + "-" + config["2Jets_Jet1_lepton_angle"] + "-" + config["2Jets_Jet2_lepton_angle"] + "-" +
                                config["Higgs_Wboson_angle"] + "-" + config["1Jet_Jet_transverse_momentum"] + ".root")
    return PlotFile_Paths


# This function is put here to make the plotting fiels cleaner
def getXaxisLabel(HistoName):
    if "MET" in HistoName:
        Xaxis_label = "Missing Transverse Momentum [GeV]"
    elif "METSig" in HistoName:
        Xaxis_label = "E_{T}^{mis.} significance"
    elif "MinDeltaPhiJETMET" in HistoName:
        Xaxis_label = "Jet Multiplicity"
    elif "Mwt" in HistoName:
        Xaxis_label = "Transverse W-boson Mass [GeV]"
    elif "Lepton_Eta" in HistoName:
        Xaxis_label = "Lepton Scalar Transverse Momentum Sum [GeV]"
    elif "Lepton_Pt" in HistoName:
        Xaxis_label = "Lepton Scalar Transverse Momentum Sum [GeV]"
    elif "nJets" in HistoName:
        Xaxis_label = "b-Tag Multiplicity"
    elif "nBTags" in HistoName:
        Xaxis_label = "Number of b-tags"
    elif "HT" in HistoName:
        Xaxis_label = "Transverse Jet Mass [GeV]"
    elif "HT_bjets" in HistoName:
        Xaxis_label = "Transverse Jet Mass [GeV]"
    elif "mVH" in HistoName:
        Xaxis_label = "Wplus + Higgs Mass [GeV]"
    elif "DeltaPhi_HW" in HistoName:
        Xaxis_label = "DeltaPhi of Higgs and W-boson"
    elif "pTH" in HistoName:
        Xaxis_label = "Higgs Scalar Transverse Momentum Sum [GeV]"
    elif "pTH_over_mVH" in HistoName:
        Xaxis_label = "Higgs Transverse Momentum over Wplus + Higgs Mass [GeV]"
    elif "pTWplus" in HistoName:
        Xaxis_label = "Transverse Wplus-boson Mass [GeV]"
    elif "pTW_over_mVH" in HistoName:
        Xaxis_label = "Wplus-boson Transverse Momentum over Wplus + Higgs Mass [GeV]"
    elif "pTWminus" in HistoName:
        Xaxis_label = "Transverse Wminus-boson Mass [GeV]"
    elif "mH" in HistoName:
        Xaxis_label = "Higgs Mass [GeV]"
    elif "mWplus" in HistoName:
        Xaxis_label = "Wplus Mass [GeV]"
    elif "maxMVAResponse" in HistoName:
        Xaxis_label = "maxMVAResponse"
    elif "mass_resolution" in HistoName:
        Xaxis_label = "mass_resolution"
    elif "MET_over_rootHT" in HistoName:
        Xaxis_label = "Missing Transverse Momentum over Transverse Jet Mass [GeV]"
    return Xaxis_label
