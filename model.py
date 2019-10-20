import xlrd
import itertools
from datetime import datetime
import gsheets as gs


def get_account(index):
    sheet = xlrd.open_workbook(r"C:\Program Files\Notifier\Accounts scraper\access_details.xls").sheet_by_index(index)
    accounts = []
    for row in range(sheet.nrows):
        temp = []
        for column in range(sheet.ncols):
            cell_val = sheet.cell_value(rowx=row, colx=column)
            temp.append(cell_val)
        accounts.append(temp)
    return accounts

def _write(table, _range, data):
    length = len(data) + 1
    cell_list = table.range(f'{_range}{length}')
    for cell, value in zip(cell_list, list(itertools.chain.from_iterable(data))):
        cell.value = value
    return cell_list

class Model:
    class online:
        class BalanceSheet:
            class Verizon:
                def __init__(self):
                    self.verizon_table = gs.GoogleSheets.bs().worksheet("Verizon")

                def write(self, data):
                    cell_list = _write(self.verizon_table, 'A2:H', data)
                    self.verizon_table.update_cells(cell_list)

            class ATT:
                def __init__(self):
                    self.att_table = gs.GoogleSheets.bs().worksheet("ATT")

                def write(self, data):
                    cell_list = _write(self.att_table, 'A2:E', data)
                    self.att_table.update_cells(cell_list)

            class Other:
                def __init__(self):
                    self.other_table = gs.GoogleSheets.bs().worksheet("Other")

                def write(self, data):
                    cell_list = _write(self.other_table, 'A2:C', data)
                    self.other_table.update_cells(cell_list)

            class Overview:
                def __init__(self):
                    self.overview_table = gs.GoogleSheets.bs().worksheet("Overview")

                def refresh_last_update_time(self):
                    self.overview_table.update_cell(value=str(datetime.today().strftime("%m/%d/%Y")), col=1, row=2)

    class local:
        # returns list of login/password for each provider
        class AccessDetails:
            verizon = get_account(0)
            att = get_account(1)
            comcast = get_account(2)[0]
            vz_wireless = get_account(3)[0]
            spectrum = get_account(4)


