import time
from xlwt import Workbook
import re
import logs
import credentials
import accounts_scraper as scraper
from datetime import datetime
import spreadsheets as sp
logs = logs.write_to_balance_tracker
import usage_scraper_sql

try:
    # SPECTRUM
    print("\t\t\t\t*********** NEW **********")

    usage_scraper_sql.update_sprint_usage()
    # logs("INFO: scraping SPECTRUM")
    # logins = sp.SpreadSheets.offline.AccessDetails.spectrum
    # scraped_specs = []
    # for login in logins:
    #     success_spec, scraped_spec = scraper.scrape_spectrum(username=login[1], password=login[2], line=login[0])
    #     scraped_specs.append(scraped_spec)
    # print(scraped_specs)
    # ----------------------------------------------------------------------------------------------

    # logs("\n\t\t\tVZ Wireless\n================================================")
    # login = sp.SpreadSheets.offline.AccessDetails.vz_wireless
    # scraped_vz_w = scraper.scrape_verizon_wireless(login[0], login[1])
    # sp.SpreadSheets.online.BalanceSheet.Verizon().write_wireless(scraped_vz_w)
    #
    # logs("\n\t\t\t\tVZ DSL\n===================================================")
    # logins = sp.SpreadSheets.offline.AccessDetails.verizon
    # scraped_vz_d = []
    # for login in logins:
    #     scraped_acc = scraper.scrape_verizon_dsl(username=login[1], password=login[2], line=login[0], secret=login[3])
    #     scraped_vz_d.append(scraped_acc)
    # sp.SpreadSheets.online.BalanceSheet.Verizon().write_dsl(scraped_vz_d)
    #
    # logs("\n\t\t\tComcast\n===================================================")
    # login = sp.SpreadSheets.offline.AccessDetails.comcast
    # success, scraped_comc = scraper.scrape_comcast(username=login[0], password=login[1])
    # if success:
    #     sp.SpreadSheets.online.BalanceSheet.Other().write(scraped_comc)
    #
    # logs("\n\t\t\tATT DSL\n=====================================================")
    # logins = sp.SpreadSheets.offline.AccessDetails.att
    # scraped_att_d = []
    # for login in logins:
    #     print(login)
    #     success, scraped_att = scraper.scrape_att(username=login[1], password=login[2], line=login[0])
    #     scraped_att_d.append(scraped_att)
    # sp.SpreadSheets.online.BalanceSheet.ATT().write(scraped_att_d)
    # sp.SpreadSheets.online.BalanceSheet.Overview().refresh_last_update_time()
except Exception as ex:
    logs(f"Exception in main: {ex}")

