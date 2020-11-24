import sys
import os

_, hmlb, hmub, wmlb, wmub = sys.argv


def getChosenFiles(chosenFiles, path, hmlb, hmub, wmlb, wmub):
    varNums = path.split("_")[-1].replace(".root", "")
    var1, var2, var3, var4 = varNums.split("-")
    if hmlb in var1 and hmub in var2 and wmlb in var3 and wmub in var4:
        for key in chosenFiles:
            if key in path:
                chosenFiles[key] = path


def getDataFiles(hmlb, hmub, wmlb, wmub):
    chosenFiles = {"sig_Hplus_Wh_m400-0": 0,
                   "sig_Hplus_Wh_m800-0": 0,
                   "sig_Hplus_Wh_m1600-0": 0,
                   "ttbarSherpa": 0,
                   "Wjets": 0,
                   "diboson": 0,
                   "singleTop": 0}
    arr = os.listdir("../PlotFiles")
    for i in arr:
        getChosenFiles(chosenFiles, i, hmlb, hmub, wmlb, wmub)

    for key in chosenFiles:
        if chosenFiles[key] == 0:
            raise Exception("all files not found" + key)
    return chosenFiles


files = getDataFiles(hmlb, hmub, wmlb, wmub)
print(files)
