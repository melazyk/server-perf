#!/usr/bin/env python3

import json
import glob
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from time import sleep

def load_file(filename: str) -> dict:
    """
    Load a file into a dictionary
    """
    with open(filename) as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            pass

    return {}


def YABStoSTAT(data: dict, width: int) -> dict:
    """
    Convert YABS data to STAT data
    """
    ndata = {
        "Provider": "",
        "Description": "",
        "CPU": {
            "single": float(),
            "multi": float(),
        },
        "Units": "",
        "Speed": {
            "r": float(),
            "w": float(),
            "rw": float(),
        },
        "IOps": {
            "r": float(),
            "w": float(),
            "rw": float(),
        },
    }

    ndata["Provider"] = data["provider"]
    # width is the width of the longest provider name, but cpu count is always 3 digits
    ndata["Description"] = ("{:" + str(width) +"} {:3}x {}").format(data["provider"], data["cpu"]["cores"], data["cpu"]["model"])
    ndata["CPU"]["single"] = float(data["geekbench"][0]["single"])
    ndata["CPU"]["multi"] = float(data["geekbench"][0]["multi"]) / float(
        data["cpu"]["cores"]
    )

    row = data["fio"][0]

    ndata["Units"] = row["speed_units"]
    ndata["Speed"]["r"] = row["speed_r"]
    ndata["Speed"]["w"] = row["speed_w"]
    ndata["Speed"]["rw"] = row["speed_rw"]
    ndata["IOps"]["r"] = row["iops_r"]
    ndata["IOps"]["w"] = row["iops_w"]
    ndata["IOps"]["rw"] = row["iops_rw"]

    for row in data["fio"][1:]:
        ndata["Speed"]["r"] = max(row["speed_r"], ndata["Speed"]["r"])
        ndata["Speed"]["w"] = max(row["speed_w"], ndata["Speed"]["w"])
        ndata["Speed"]["rw"] = max(row["speed_rw"], ndata["Speed"]["rw"])
        ndata["IOps"]["r"] = max(row["iops_r"], ndata["IOps"]["r"])
        ndata["IOps"]["w"] = max(row["iops_w"], ndata["IOps"]["w"])
        ndata["IOps"]["rw"] = max(row["iops_rw"], ndata["IOps"]["rw"])

        if ndata["Units"] != row["speed_units"]:
            raise Exception("Wrong units")

    return ndata


class YABS(object):
    """
    YABS class

    This class is used to store YABS data and convert it to STAT data
    """
    def __init__(self):
        self.data = []
        self.stat = []
        self.round = 2
        self.provider_width = 0

    def AddFile(self, filename: str):
        data = load_file(filename)
        data["provider"] = filename.split("/")[1]

        # Find the longest provider name
        if len(data["provider"]) > self.provider_width:
            self.provider_width = len(data["provider"])

        self.data.append(data)

    def Calculate(self):
        for y in self.data:
            self.stat.append(YABStoSTAT(y, self.provider_width))

    def Print(self):
        for s in self.stat:
            print(s["Description"])


    def Plot(self, resources: list[str] = ["CPU"]):
        fig, axes = plt.subplots(ncols=len(resources), figsize=(14 * len(resources), 10 ))

        colors = sns.color_palette("colorblind", len(self.stat))

        for resource in resources:
            if resource not in ["CPU", "Speed", "IOps"]:
                raise ValueError("Invalid value for resource. Must be one of 'CPU', 'Speed', or 'IOps'.")

            bars = {}
            groups = []
            for s in self.stat:
                if s["Description"] not in bars:
                    bars[s["Description"]] = []

                for r in sorted(s[resource].keys()):
                    if r not in groups:
                        groups.append(r)
                    bars[s["Description"]].append(s[resource][r])

            count = len(self.stat)
            barWidth = round(1 / ( count + 1 ), self.round )
            brs = []
            brs.append(np.arange(len(groups)))

            axe = plt.axes(axes[resources.index(resource)])
            for i in range(count):
                label = self.stat[i]["Description"]
                axe.bar(brs[i], bars[label], color = colors[i], width= barWidth, edgecolor = 'grey', label = label )
                brs.append([round(x + barWidth, self.round) for x in brs[i]])


            axe.legend(prop={'family': 'monospace', 'size': 10}, shadow=False)
            axe.set_xticks([r + barWidth for r in range(len(groups))], groups)
            axe.set_title(resource, fontsize=20)

        plt.plot()
        # plt.show()
        plt.savefig("output.png")

def main(path: str):
    yabs = YABS()
    for file in glob.glob(path):
        yabs.AddFile(file)

    yabs.Calculate()
    yabs.Print()
    yabs.Plot(['CPU', 'Speed', 'IOps'])


if __name__ == "__main__":
    main("results/*/*.json")
