import os
from Sheet import Sheet

class Gene_Stats:
    def __init__(self, name):
        self.name = name
        self.b = []
        self.m = []
        self.e = []

input_path = "./input"
input_files = []
for root, dirs, files in os.walk(input_path):
    for f in files:
        if f.endswith(".csv"):
            input_files.append(root + "/" + f)

print(input_files)

genes = {}

for file in input_files:
    sheet = Sheet(file, PEAK="AGGREGATE")
    for row in sheet.rows:
        gene_name = row.get_value("#GENE")
        if gene_name not in genes:
            genes[gene_name] = Gene_Stats(gene_name)
        if