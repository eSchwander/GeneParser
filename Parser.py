from os import listdir
from os.path import isfile, join

input_path = "./input"

input_files = [f for f in listdir(input_path) if isfile(join(input_path, f))]

for file in input_files:
