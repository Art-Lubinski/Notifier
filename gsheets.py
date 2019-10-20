import settings
import gspread


class _GSheets:
    __main_active = False
    __bs_active = False
    __soldlines_active = False
    __wirelessaccounts_active = False

    def __init__(self):
        self.gc = gspread.authorize(settings.google_credentials)

    # DSL Rentals servers file
    def main(self):
        if not self.__main_active:
            self.sh = self.gc.open(settings.main_table)
            self.__main_active = True
        return self.sh

    # Balance sheet file
    def bs(self):
        if not self.__bs_active:
            self.sh = self.gc.open(settings.balance_sheet)
            self.__bs_active = True
        return self.sh

    # Sold lines file
    def sold_lines(self):
        if not self.__soldlines_active:
            self.sh = self.gc.open(settings.sold_lines)
            print("sold lines called")
            self.__soldlines_active = True
        return self.sh

    # Wireless Accounts file
    def wireless_accounts(self):
        if not self.__wirelessaccounts_active:
            self.sh = self.gc.open(settings.wireless_table)
            self.__wirelessaccounts_active = True
        return self.sh


GoogleSheets = _GSheets()
