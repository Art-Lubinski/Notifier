import xlrd
import itertools
from datetime import datetime
import gsheets as gs
import settings


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

# Represents Google sheets, local database and sql server
class Model:
    class online:
        class BalanceSheet:
            class Verizon:
                def __init__(self):
                    self.sheet = gs.GoogleSheets.bs().worksheet("Verizon")

                def write(self, data):
                    cell_list = _write(self.sheet, 'A2:H', data)
                    self.sheet.update_cells(cell_list)

            class ATT:
                def __init__(self):
                    self.sheet = gs.GoogleSheets.bs().worksheet("ATT")

                def write(self, data):
                    cell_list = _write(self.sheet, 'A2:E', data)
                    self.sheet.update_cells(cell_list)

            class Other:
                def __init__(self):
                    self.sheet = gs.GoogleSheets.bs().worksheet("Other")

                def write(self, data):
                    cell_list = _write(self.sheet, 'A2:C', data)
                    self.sheet.update_cells(cell_list)

            class Overview:
                def __init__(self):
                    self.sheet = gs.GoogleSheets.bs().worksheet("Overview")

                def refresh_last_update_time(self):
                    self.sheet.update_cell(value=str(datetime.today().strftime("%m/%d/%Y")), col=1, row=2)
        class SoldLines:
            class AutoReport:
                def __init__(self):
                    self.sheet = gs.GoogleSheets.sold_lines().worksheet(settings.sheet_sold_lines)

        class WirelessAccounts:
            @staticmethod
            def update_table():
                update_table_wireless_accounts()

            class Verizon:
                def __init__(self):
                    self.sheet = gs.GoogleSheets.wireless_accounts().worksheet("Verizon")

            class ATT:
                def __init__(self):
                    self.sheet = gs.GoogleSheets.wireless_accounts().worksheet("ATT")

            class Sprint:
                def __init__(self):
                    self.sheet = gs.GoogleSheets.wireless_accounts().worksheet("Sprint")

        class Main:
            class SheetDSL:
                def __init__(self):
                    self.sheet = gs.GoogleSheets.main().worksheet(settings.sheet_name_dsl)

            class Sheet4G:
                def __init__(self):
                    self.sheet = gs.GoogleSheets.main().worksheet(settings.sheet_name_4g)



    class local:
        # returns list of login/password for each provider
        class AccessDetails:
            verizon = get_account(0)
            att = get_account(1)
            comcast = get_account(2)[0]
            vz_wireless = get_account(3)[0]
            spectrum = get_account(4)


def update_table_wireless_accounts():
    wks = Model.online.Main.Sheet4G().sheet
    main_table_4g = wks.get_all_values()
    for n in [0, 1, 2]:
        if n == 0:
            provider_table = Model.online.WirelessAccounts.Verizon().sheet
            provider_name = "VERIZON"
        elif n == 1:
            provider_table = Model.online.WirelessAccounts.Sprint().sheet
            provider_name = "SPRINT"
        else:
            provider_table = Model.online.WirelessAccounts.ATT().sheet
            provider_name = "ATT"
        provider_table.get_all_values()
        sprint_numbers_from_table = []
        for pc_name, provider, number, email, customer, if_panel, modem, if_broken in zip(main_table_4g[1],
                                                                                          main_table_4g[4],
                                                                                          main_table_4g[17],
                                                                                          main_table_4g[7],
                                                                                          main_table_4g[6],
                                                                                          main_table_4g[9],
                                                                                          main_table_4g[5],
                                                                                          main_table_4g[10]):
            if provider == provider_name:
                if number == "":
                    number = "not found"
                if email == "" and if_panel == "1":
                    customer = "panel"
                modem = modem.split()
                if len(modem) == 0:
                    modem = ""
                else:
                    modem = modem[0]
                pc = {"phone": number, "pc_name": pc_name, "email": email, "customer": customer, "modem": modem}
                sprint_numbers_from_table.append(pc)

        length = len(provider_table)

        numbers = wks.range('B2:B{0}'.format(length))
        lines = wks.range('A2:A{0}'.format(length))
        clients = wks.range('E2:E{0}'.format(length))
        modems = wks.range('D2:D{0}'.format(length))

        for phone, line, client, modem in zip(numbers, lines, clients, modems):
            line.value = "not found"
            client.value = ""
            modem.value = ""
            if phone.value in settings.special_lines:
                line.value = settings.special_lines[phone.value]
            for pc in sprint_numbers_from_table:
                if pc["phone"] == phone.value:
                    line.value = pc["pc_name"]
                    client.value = pc["customer"]
                    modem.value = pc["modem"]

        wks.update_cells(lines)
        wks.update_cells(clients)
        wks.update_cells(modems)


