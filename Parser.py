import os
import numpy
from Sheet import Sheet


class Gene_Stats:
    def __init__(self, name):
        self.name = name
        self.values = {"BEG": [], "MID": [], "END": []}
        self.means = {"BEG": 0, "MID": 0, "END": 0}

    def find_means(self):
        for k in self.values:
            self.means[k] = numpy.mean(self.values[k])


input_path = "./input"
input_files = []
for root, dirs, files in os.walk(input_path):
    for f in files:
        if f.endswith(".csv"):
            input_files.append(root + "/" + f)

print(input_files)

genes = {}
totals = Gene_Stats("Totals")

for file in input_files:
    sheet = Sheet(file, PEAK="AGGREGATE")
    for row in sheet.rows:
        gene_name = row.get_value("#GENE")
        int_type = row.get_value("INTTYPE")
        odds_ratio = row.get_value("ODDSRATIO")
        if int_type != "WHOLE":
            if gene_name not in genes:
                genes[gene_name] = Gene_Stats(gene_name)
            genes[gene_name].values[int_type].append(float(odds_ratio))

for gene_name in genes:
    gene = genes[gene_name]
    gene.find_means()
    for mean in gene.means:
        totals.values[mean].append(gene.means[mean])

totals.find_means()

summary_headers = []
for name in genes:
    summary_headers.append(name + "_BEG")
    summary_headers.append(name + "_MID")
    summary_headers.append(name + "_END")
summary_headers.append("TOTAL_BEG")
summary_headers.append("TOTAL_MID")
summary_headers.append("TOTAL_END")
