#!/usr/bin/env python3

import json
import glob


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


def YABStoSTAT(data: dict) -> dict:
    ndata = {
        "Provider": "",
        "Description": "",
        "CPU": {
            "freq": "",
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
    ndata["Description"] = "{}x {}".format(data["cpu"]["cores"], data["cpu"]["model"])
    ndata["CPU"]["freq"] = data["cpu"]["freq"]
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
    def __init__(self):
        self.data = []
        self.stat = []

    def AddFile(self, filename: str):
        data = load_file(filename)
        data["provider"] = filename.split("/")[1]
        self.data.append(data)

    def Calculate(self):
        for y in self.data:
            self.stat.append(YABStoSTAT(y))

    def Print(self):
        for s in self.stat:
            print(s)


def main(path: str):
    yabs = YABS()
    for file in glob.glob(path):
        yabs.AddFile(file)

    yabs.Calculate()
    yabs.Print()


if __name__ == "__main__":
    main("results/*/*.json")
