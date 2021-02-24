directory = r"C:\Users\Zahaab\Desktop\Plots\PlotsFEB21"
WP = "85p"
print("\n" + "HERE IS " + WP + "\n")

subdir = directory + "\\" + WP + "\\" + "StackPlots"

totals85 = []
dataSet = 0

for folder in os.listdir(subdir):
    print("\n" + "NOW SHOWING " + folder + "\n")
    df = pd.read_csv(subdir + "\\" + folder + "\\" +
                     "cutflow.txt", delimiter=',')
    print(df)
    totals85.append(df["Total"].tolist())
    dataSet = df["Data-Set"].tolist()

print("Base-cut is ", " Higgs_mass_lower_bound = 0. ", "\n" + "Higgs_mass_upper_bound = 210. ", "\n",
      "Wboson_mass_lower_bound = 0. ", "\n", "Wboson_mass_upper_bound = 200. ", "\n", "Higgs_Wboson_angle = 2.5 ",
      "\n", "Missing_transverse_momentum = 40000. ", "\n", "Lepton_transverse_momentum = 30000. ", "\n",
      "2Jets_Jet1_transverse_momentum = 200000. ", "\n", "2Jets_Jet2_transverse_momentum = 200000. ", "\n",
      "2Jets_Jet1_lepton_angle = 1.0 ", "\n", "2Jets_Jet2_lepton_angle = 1.0 ", "\n"
      "1Jet_Jet_transverse_momentum = 250000.")

dftotals85 = pd.DataFrame.from_dict({"Data-Set": dataSet,
                                     "Base_cut": totals85[0],
                                     "MET_Pt = 40000.": totals85[1],
                                     "LEP_Pt = 40000.": totals85[2]})

dftotals85
