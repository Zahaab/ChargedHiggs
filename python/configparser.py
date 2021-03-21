def configParser(path):
    config = {}
    with open(path) as fp:
        for line in fp:
            key_val = line.replace(" ", "").strip().split("=")
            config[key_val[0]] = key_val[1]
    del config["-----------"]
    del config["------------"]
    return config


# var is either Stack_ , Plot_ , Graph_ , Btag_ that give dataPeriodes, Plotting event catagories, Graph names, Btagging choice respectively.
def getConfigData(config, var):
    # print(config)
    ConfigData = [key.replace(
        var, "") for key in config if var in key and config[key] == "Enable"]
    return ConfigData


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
def getaxisLabels(HistoName):
    Xaxis_label = ""
    legend_place = []
    text_place = []
    if "MET" == HistoName:
        Xaxis_label = "Missing Transverse Momentum [GeV]"
        legend_place = [0.65, 0.73, 0.91, 0.885]
        text_place = [0.65, 0.895]
    elif "METSig" == HistoName:
        Xaxis_label = "E_{T}^{mis.} significance"
        legend_place = [0.65, 0.73, 0.91, 0.885]
        text_place = [0.6, 0.895]
    elif "MinDeltaPhiJETMET" == HistoName:
        Xaxis_label = "Jet Multiplicity"
        legend_place = [0.65, 0.73, 0.91, 0.885]
        text_place = [0.4, 0.895]
    elif "Mwt" == HistoName:
        Xaxis_label = "m_{T}(W) [GeV]"
        legend_place = [0.65, 0.73, 0.91, 0.885]
        text_place = [0.65, 0.895]
    elif "Lepton_Eta" == HistoName:
        Xaxis_label = "Lepton #eta [Rad]"
        legend_place = [0.69, 0.795, 0.95, 0.95]
        text_place = [0.19, 0.895]
    elif "Lepton_Pt" == HistoName:
        Xaxis_label = "Lepton p_{T} [GeV]"
        legend_place = [0.65, 0.73, 0.91, 0.885]
        text_place = [0.56, 0.895]
    elif "nJets" == HistoName:
        Xaxis_label = "b-Tag Multiplicity"
        legend_place = [0.19, 0.73, 0.45, 0.885]
        text_place = [0.19, 0.895]
    elif "nJets_(Fat)" == HistoName:
        Xaxis_label = "(Fat)b-Tag Multiplicity"
        legend_place = [0.19, 0.73, 0.45, 0.885]
        text_place = [0.19, 0.895]
    elif "nBTags" == HistoName:
        Xaxis_label = "Number of b-tags"
        legend_place = [0.69, 0.795, 0.95, 0.95]
        text_place = [0.19, 0.895]
    elif "HT" == HistoName:
        Xaxis_label = "H_{T}(jet) [GeV]"
        legend_place = [0.19, 0.73, 0.45, 0.885]
        text_place = [0.19, 0.895]
    elif "HT_bjets" == HistoName:
        Xaxis_label = "H_{T}(Bjet) [GeV]"
        legend_place = [0.65, 0.73, 0.91, 0.885]
        text_place = [0.6, 0.895]
    elif "HT_bjets_Lepton_Pt" == HistoName:
        Xaxis_label = "H_{T}(Bjet) + Lepton p_{T} [GeV]"
        legend_place = [0.65, 0.73, 0.91, 0.885]
        text_place = [0.38, 0.895]
    elif "mVH" == HistoName:
        Xaxis_label = "m_{VH} [GeV]"
        legend_place = [0.69, 0.8, 0.93, 0.885]
        text_place = [0.69, 0.895]
    elif "DeltaPhi_HW" == HistoName:
        Xaxis_label = "#Delta#phi of Higgs and W-boson"
        legend_place = [0.19, 0.73, 0.45, 0.885]
        text_place = [0.19, 0.895]
    elif "pTH" == HistoName:
        Xaxis_label = "p_{T}(h) [GeV]"
        legend_place = [0.65, 0.73, 0.91, 0.885]
        text_place = [0.65, 0.895]
    elif "pTH_over_mVH" == HistoName:
        Xaxis_label = "p_{T}(h) / m_{VH} [GeV]"
        legend_place = [0.19, 0.73, 0.45, 0.885]
        text_place = [0.19, 0.895]
    elif "pTWplus" == HistoName:
        Xaxis_label = "p_{T}(W^{+}) [GeV]"
        legend_place = [0.69, 0.795, 0.95, 0.95]
        text_place = [0.19, 0.895]
    elif "pTW_over_mVH" == HistoName:
        Xaxis_label = "p_{T}(W) / m_{VH} [GeV]"
        legend_place = [0.69, 0.795, 0.95, 0.95]
        text_place = [0.19, 0.895]
    elif "pTWminus" == HistoName:
        Xaxis_label = "p_{T}(W^{-}) [GeV]"
        legend_place = [0.65, 0.73, 0.91, 0.885]
        text_place = [0.56, 0.895]
    elif "mH" == HistoName:
        Xaxis_label = "Higgs Mass [GeV]"
        legend_place = [0.65, 0.73, 0.91, 0.885]
        text_place = [0.65, 0.895]
    elif "mWplus" == HistoName:
        Xaxis_label = "W^{+} Mass [GeV]"
        legend_place = [0.65, 0.73, 0.91, 0.885]
        text_place = [0.6, 0.895]
    elif "maxMVAResponse" == HistoName:
        Xaxis_label = "maxMVAResponse"
        legend_place = [0.19, 0.73, 0.45, 0.885]
        text_place = [0.19, 0.895]
    elif "mass_resolution" == HistoName:
        Xaxis_label = "mass_resolution".replace("_", " ")
        legend_place = [0.65, 0.73, 0.91, 0.885]
        text_place = [0.47, 0.895]
    elif "MET_over_rootHT" == HistoName:
        Xaxis_label = "Missing p_{T} / H_{T}(jet) [GeV]"
        legend_place = [0.65, 0.73, 0.91, 0.885]
        text_place = [0.445, 0.895]
    elif "m_NTags_trkJ" == HistoName:
        Xaxis_label = "m_NTags_trkJ???"
        legend_place = [0.65, 0.73, 0.91, 0.885]
        text_place = [0.445, 0.895]
    return [Xaxis_label, legend_place, text_place]
