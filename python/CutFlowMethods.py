def prepareCutHolder(cutHolder, cutParameters, btagStrategies):
    for parameter in cutParameters:
        cutHolder[parameter] = {}
        for channel in ["jjbb", "lvbb"]:
            cutHolder[parameter][channel] = {}
            for btagStrategy in btagStrategies:
                cutHolder[parameter][channel][btagStrategy] = []
            cutHolder[parameter][channel]["Total"] = []
    return cutHolder


def cutFlowExtraction(content, cutParameters, btagStrategies, cutHolder):
    for index, parameter in enumerate(cutParameters):
        jjbb_values, lvbb_values = content[index].split("=")[1].split("|")
        for tagged_values in [(jjbb_values.split(","), "jjbb"), (lvbb_values.split(","), "lvbb")]:
            if tagged_values[0][-1] == "0":  # Some cut parameters don't cut anythign
                for btagStrategy in btagStrategies:
                    cutHolder[parameter][tagged_values[1]
                                         ][btagStrategy].append("0")
                cutHolder[parameter][tagged_values[1]]["Total"].append("0")
                continue
            for tagging, cutFlowValue in enumerate(tagged_values[0]):
                if tagged_values[0][tagging] == tagged_values[0][-1]:
                    cutHolder[parameter][tagged_values[1]
                                         ]["Total"].append(cutFlowValue)
                else:
                    cutHolder[parameter][tagged_values[1]][btagStrategies[tagging]].append(
                        cutFlowValue)


def cutFlowPercentExtraction(content, cutParameters, btagStrategies, cutHolder):
    total_events = []
    for index, parameter in enumerate(cutParameters):
        jjbb_values, lvbb_values = content[index].split("=")[1].split("|")
        for tagged_values in [(jjbb_values.split(","), "jjbb"), (lvbb_values.split(","), "lvbb")]:
            if tagged_values[0][-1] == "0":  # Some cut parameters don't cut anythign
                for btagStrategy in btagStrategies:
                    cutHolder[parameter][tagged_values[1]
                                         ][btagStrategy].append("0")
                cutHolder[parameter][tagged_values[1]]["Total"].append("0")
                continue
            if parameter[-11:] == "TotalEvents":
                total_events = [float(i) for i in tagged_values[0]]
                for tagging, cutFlowValue in enumerate(tagged_values[0]):
                    if tagged_values[0][tagging] == tagged_values[0][-1]:
                        cutHolder[parameter][tagged_values[1]
                                             ]["Total"].append(cutFlowValue)
                    else:
                        cutHolder[parameter][tagged_values[1]][btagStrategies[tagging]].append(
                            cutFlowValue)
                continue
            for tagging, cutFlowValue in enumerate(tagged_values[0]):
                if tagged_values[0][tagging] == tagged_values[0][-1]:
                    cutHolder[parameter][tagged_values[1]]["Total"].append(
                        str((float(cutFlowValue)/total_events[-1])*100))
                else:
                    cutHolder[parameter][tagged_values[1]][btagStrategies[tagging]].append(
                        str((float(cutFlowValue)/total_events[tagging])*100))


def sumPercent(total_list, percents):
    flat_values = []
    for index, total in enumerate(total_list):
        if percents[index] == 0:
            continue
        flat_values.append(total*percents[index])
    if flat_values == []:
        return 0
    else:
        return (sum(flat_values)/sum(total_list))


def cutFlowInsertion(file, data_set, dataPeriodes, btagStrategies, cutParameters, cutHolder, Percent="disable"):
    for periodindex, dataPeriod in enumerate(dataPeriodes):
        for btagStrategy in btagStrategies:
            for channel in ["jjbb", "lvbb"]:
                rowData = [data_set, dataPeriod, btagStrategy, channel]
                rowValues = []
                total_events = 0
                for parameter in cutParameters:
                    if parameter[-11:] == "TotalEvents":
                        total_events = float(
                            cutHolder[parameter][channel][btagStrategy][periodindex])
                    rowValues.append(
                        float(cutHolder[parameter][channel][btagStrategy][periodindex]))
                    rowData.append(
                        str(cutHolder[parameter][channel][btagStrategy][periodindex]))
                file.write(",".join(rowData) + "," +
                           str(sum(rowValues) - total_events) + "\n")
        for channel in ["jjbb", "lvbb"]:
            rowData = [data_set, dataPeriod, "All_Tagging", channel]
            rowValues = []
            total_events = 0
            for parameter in cutParameters:
                if parameter[-11:] == "TotalEvents":
                    total_events = float(
                        cutHolder[parameter][channel]["Total"][periodindex])
                rowValues.append(
                    float(cutHolder[parameter][channel]["Total"][periodindex]))
                rowData.append(
                    str(cutHolder[parameter][channel]["Total"][periodindex]))
            file.write(",".join(rowData) + "," +
                       str(sum(rowValues) - total_events) + "\n")
    for btagStrategy in btagStrategies:
        for channel in ["jjbb", "lvbb"]:
            rowData = [data_set, "All_Data_Periods", btagStrategy, channel]
            rowValues = []
            total_events = 0
            total_events_list = []
            for parameter in cutParameters:
                if Percent == "enable":
                    if parameter[-11:] == "TotalEvents":
                        total_events_list = [
                            float(i) for i in cutHolder[parameter][channel][btagStrategy]]
                        valueAllPeriods = sum(
                            [float(i) for i in cutHolder[parameter][channel][btagStrategy]])
                    else:
                        valueAllPeriods = sumPercent(total_events_list, [float(
                            i) for i in cutHolder[parameter][channel][btagStrategy]])
                else:
                    if parameter[-11:] == "TotalEvents":
                        total_events = sum([float(i)
                                            for i in cutHolder[parameter][channel][btagStrategy]])
                    valueAllPeriods = sum([float(i)
                                           for i in cutHolder[parameter][channel][btagStrategy]])
                rowValues.append(float(valueAllPeriods))
                rowData.append(str(valueAllPeriods))
            if Percent == "enable":
                file.write(",".join(rowData) + "," +
                           str(sum(rowValues) - sum(total_events_list)) + "\n")
            else:
                file.write(",".join(rowData) + "," +
                           str(sum(rowValues) - total_events) + "\n")
    for channel in ["jjbb", "lvbb"]:
        rowData = [data_set, "All_Data_Periods", "All_Tagging", channel]
        rowValues = []
        total_events = 0
        for parameter in cutParameters:
            if Percent == "enable":
                if parameter[-11:] == "TotalEvents":
                    total_events_list = [float(i)
                                         for i in cutHolder[parameter][channel]["Total"]]
                    valueAllPeriods = sum([float(i)
                                           for i in cutHolder[parameter][channel]["Total"]])
                else:
                    valueAllPeriods = sumPercent(total_events_list, [float(
                        i) for i in cutHolder[parameter][channel]["Total"]])
            else:
                if parameter[-11:] == "TotalEvents":
                    total_events = sum([float(i)
                                        for i in cutHolder[parameter][channel]["Total"]])
                valueAllPeriods = sum([float(i)
                                       for i in cutHolder[parameter][channel]["Total"]])
            rowValues.append(float(valueAllPeriods))
            rowData.append(str(valueAllPeriods))

        if Percent == "enable":
            file.write(",".join(rowData) + "," +
                       str(sum(rowValues) - sum(total_events_list)) + "\n")
        else:
            file.write(",".join(rowData) + "," +
                       str(sum(rowValues) - total_events) + "\n")
