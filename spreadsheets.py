import gspread
import credentials
import xlrd
import itertools
from datetime import datetime

gc = gspread.authorize(credentials.google_credentials)
sheet = gc.open("Balance Sheet")


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


class SpreadSheets:
    class online:
        class BalanceSheet:
            class Verizon:
                def __init__(self):
                    self.verizon_table = sheet.worksheet("Verizon")

                def write(self, data):
                    length = len(data) + 1
                    cell_list = self.verizon_table.range('A2:H{0}'.format(length))
                    for cell, value in zip(cell_list, list(itertools.chain.from_iterable(data))):
                        cell.value = value
                    self.verizon_table.update_cells(cell_list)

            class ATT:
                def __init__(self):
                    self.att_table = sheet.worksheet("ATT")

                def write(self, data):
                    length = len(data) + 1
                    cell_list = self.att_table.range('A2:E{0}'.format(length))
                    for cell, value in zip(cell_list, list(itertools.chain.from_iterable(data))):
                        cell.value = value
                    self.att_table.update_cells(cell_list)

            class Other:
                def __init__(self):
                    self.other_table = sheet.worksheet("Other")

                def write(self, data):
                    length = len(data) + 1
                    cell_list = self.other_table.range('A2:C{0}'.format(length))
                    for cell, value in zip(cell_list, list(itertools.chain.from_iterable(data))):
                        cell.value = value
                    self.other_table.update_cells(cell_list)

            class Overview:
                def __init__(self):
                    self.overview_table = sheet.worksheet("Overview")

                def refresh_last_update_time(self):
                    self.overview_table.update_cell(value=str(datetime.today().strftime("%m/%d/%Y")), col=1, row=2)
                    print()

    class offline:
        class AccessDetails:
            verizon = get_account(0)
            att = get_account(1)
            comcast = get_account(2)[0]
            vz_wireless = get_account(3)[0]
            spectrum = get_account(4)


