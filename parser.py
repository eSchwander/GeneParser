import csv
import os
from lib.sheet import Sheet
from lib.gene_stats import GeneStats

# Declaring file paths for later usage
file_types = ["csv", "tsv"]
input_path = "./input"
output_path = "./output"
processed_path = './processed'
old_summary_file = output_path + "/summary.csv"
new_summary_file = output_path + '/new_summary.csv'

# Reading in input files
input_files = []
for root, dirs, files in os.walk(input_path):
    for f in files:
        extension = f.split(".")[-1]
        if extension in file_types:
            input_files.append((root, f))

# Main loop
for path, input_file in input_files:

    # Gene map to be used later
    genes = {}
    totals = GeneStats("TOTAL")

    # Read input sheet
    input_file_path = path + "/" + input_file
    sheet = Sheet(input_file_path, PEAK="AGGREGATE")

    # Go through input rows and store gene info
    for row in sheet.rows:
        gene_name = row.get_value("#GENE")
        int_type = row.get_value("INTTYPE")
        odds_ratio = row.get_value("ODDSRATIO")
        if int_type != "WHOLE":
            if gene_name not in genes:
                genes[gene_name] = GeneStats(gene_name)
            genes[gene_name].values[int_type].append(float(odds_ratio))

    # Calculate mean values for each gene
    for gene_name in genes:
        gene = genes[gene_name]
        gene.find_means()
        # Store totals
        for mean in gene.means:
            totals.values[mean].append(gene.means[mean])

    # Calculate total means and store in gene map
    totals.find_means()
    genes["TOTAL"] = totals

    # Determining new headers
    new_summary_headers = []
    for name in genes:
        new_summary_headers.append(name + "_BEG")
        new_summary_headers.append(name + "_MID")
        new_summary_headers.append(name + "_END")

    # If an old summary sheet exists, add old headers to new headers and create Sheet to be used later
    old_sheet = None
    if old_summary_file.split("/")[-1] in os.listdir(output_path):
        old_sheet = Sheet(old_summary_file)
        old_summary_headers = old_sheet.headers
        for header in old_summary_headers:
            if header not in new_summary_headers:
                new_summary_headers.insert(0, header)

    # Write the new summary file
    with open(new_summary_file, mode='w', newline='') as new_summary:
        writer = csv.writer(new_summary)
        # Write headers
        writer.writerow(new_summary_headers)

        # Write old information to new sheet
        if old_sheet is not None:
            for row in old_sheet.rows:
                row_to_write = []
                for header in new_summary_headers:
                    row_to_write.append(row.get_value(header))
                writer.writerow(row_to_write)

        # Write new info to the summary file
        new_summary_row = []
        for header in new_summary_headers:
            gene_name = header.split("_")[0]
            bme = header.split("_")[1]
            if gene_name in genes:
                value = genes[gene_name].means[bme]
            else:
                value = ""
            new_summary_row.append(value)
        writer.writerow(new_summary_row)

    # Remove old file if it exists and rename new file
    if old_summary_file.split("/")[-1] in os.listdir(output_path):
        os.remove(old_summary_file)
    os.rename(new_summary_file, old_summary_file)

    # Move input file elsewhere
    os.rename(input_file_path, processed_path + "/" + input_file)
