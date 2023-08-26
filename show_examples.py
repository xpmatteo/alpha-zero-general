import argparse
from pickle import Unpickler

parser = argparse.ArgumentParser()
parser.add_argument("examples_file", help="file to analyze")
args = parser.parse_args()

with open(args.examples_file, "rb") as f:
    data = Unpickler(f).load()
    print("Number of elements: " + str(len(data)))
    print("Last element: " + str(data[-1]))
