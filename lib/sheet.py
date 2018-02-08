import csv


def get_delimiter(file_path):
    if file_path.endswith(".csv"):
        return ","
    elif file_path.endswith(".tsv"):
        return "\t"
    else:
        return ","


class Sheet:
    class Row:
        def __init__(self, sheet, row):
            self.row = row
            self.sheet = sheet

        def get_value(self, column_name):
            if column_name not in self.sheet.headers:
                return ""
            index = self.sheet.headers[column_name]
            return self.row[index]

        def __len__(self):
            return len(self.row)

    def __init__(self, file_path, **filter):
        self.sheet_name = file_path.split("/")[-1]
        self.filter = filter
        self.rows = []
        self.headers = {}
        with open(file_path) as file:
            delimiter = get_delimiter(file_path)
            reader = csv.reader(file, delimiter=delimiter)
            for i, row in enumerate(reader):
                if i == 0:
                    self.set_headers(row)
                else:
                    self.add_row(row)

    def add_row(self, row):
        temp_row = self.Row(self, row)
        if len(self.headers) != len(temp_row):
            return
        for k in self.filter:
            if temp_row.get_value(k) != self.filter[k]:
                return
        self.rows.append(temp_row)

    def set_headers(self, first_row):
        for i, c in enumerate(first_row):
            self.headers[c] = i

    def get_row(self, row_num):
        return self.rows[row_num]


class OutputSheet:
    def __init__(self, headers):
        self.headers = headers
