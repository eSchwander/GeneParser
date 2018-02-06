import csv

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

    def __init__(self, file_path, **filter):
        self.sheet_name = file_path.split("/")[-1]
        self.filter = filter
        self.rows = []
        self.headers = {}
        with open(file_path) as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                if i == 0:
                    self.set_headers(row)
                else:
                    self.filter_row(row)

    def filter_row(self, row):
        temp_row = self.Row(self, row)
        add_row = True
        for k in self.filter:
            if temp_row.get_value(k) != self.filter[k]:
                add_row = False
        if add_row:
            self.rows.append(temp_row)

    def set_headers(self, first_row):
        for i, c in enumerate(first_row):
            self.headers[c] = i

    def get_row(self, row_num):
        return self.rows[row_num]


class OutputSheet:
    def __init__(self, headers):
        self.headers = headers
