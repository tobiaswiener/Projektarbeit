import json
import os
import FFNN

directory = "input"


def lineToParas(input):
    L = input



for filename in os.scandir(directory):
    if(filename.path.endswith(".ip")):
        with open(filename) as f:
            data = json.load(f)
            FFNN.runFFNNFile(input=data)

