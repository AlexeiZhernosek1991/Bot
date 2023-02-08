import gspread


class Table:
    def __init__(self, credentials, table_name):
        self.credentials = credentials
        self.table_name = table_name

    def get_sheet_list(self):
        gc = gspread.service_account(filename=self.credentials)
        sh = gc.open(self.table_name)
        worksheet = sh.get_worksheet(0)
        return worksheet


def get_list_row(worksheet, name):
    cell_list = worksheet.findall(name)
    return list(worksheet.row_values(c.row) for c in cell_list)
