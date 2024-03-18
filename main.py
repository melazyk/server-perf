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


class YABS(object):
    def __init__(self):
        self.data = []
        
    def AddFile(self, filename: str):
        self.data.append(load_file(filename))


    
def main(path: str):
    yabs := YABS()
    for file in glob.glob(path):
        yabs.AddFile(file)
        
        
if __name__ == "__main__":
    main("results/*/*.json")