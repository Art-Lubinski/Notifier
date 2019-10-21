from oauth2client.service_account import ServiceAccountCredentials
import datetime
from dateutil.relativedelta import relativedelta
import os
import sys
# path
__current_dir = os.path.realpath(__file__)
folder_path = __current_dir[:-11]
account_scraper_folder_path = folder_path + "Accounts scraper/"
data_folder_path = folder_path + "Data/"
sqlconnection_string = r'DSN=DSLRENTALS; UID=Test;PWD=Mp2664311'
webdriver_path = r"/Users/artlubinski/PycharmProjects/Notifier/chromedriver-2"
sql_alchemy = "mssql+pyodbc://Test:Mp2664311@DSLRENTALS"
print("helo", webdriver_path)
if sys.platform == "win32":
    folder_path = folder_path.replace("/","\\")
    account_scraper_folder_path = account_scraper_folder_path.replace("/","\\")
    data_folder_path = data_folder_path.replace("/", "\\")
    sqlconnection_string = r'DRIVER={ODBC Driver 13 for SQL Server}; Server=tcp:192.168.0.197\WIN-JHM3H4KID52,1433;Database=Dslrentals;Trusted_connection=no;UID=Test;PWD=Mp2664311'
    webdriver_path = r"C:\Program Files\Notifier_v2\chromedriver.exe"
    sql_alchemy = "mssql+pyodbc://Test:Mp2664311@192.168.0.197:1433/Dslrentals?driver=ODBC+Driver+13+for+SQL+Server"

# test_all - sends reminders and ALL emails to Art
# test - sends emails to Art(except reminders). Doesnt write to log file
# prod - production
mode = "test"

# Google authorization
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
google_credentials = ServiceAccountCredentials.from_json_keyfile_name(folder_path+'Notifier-a4445923504c.json', scope)

# Files, Tables, and Sheets names
sheet_name_dsl = "DSL Servers"
sheet_name_4g = "4G Servers"
sheet_sprint = "Sprint"
sheet_att = "ATT"
sheet_verizon = "Verizon"
main_table = "DSL Rentals Servers"
sold_lines = "Sold lines"
sheet_sold_lines = "Auto report"
wireless_table = "wireless_accounts"
balance_sheet = "Balance"
panel_sheet = "Panel form"
quote_form_tab = "Quote form requests"

# Mail server settings
server_username = "no-reply@dslrentals.com"
server_password = "winc4920520"
server_host = "gator4059.hostgator.com"
server_port = 587
notify_from_email = server_username
to_email = ["artsiom.lubinsky@gmail.com"]

# Verizon settings
usernameVerizon = "WORLDINC4G"
passwordVerizon = "W663300w"


# Sprint settings
usernameSprint = "worldintercom1"
passwordSprint = "W663300w.1"
sprint_plan_limit = 120
sprint_bill = 16
date = datetime.date.today()
sprint_billing_date = datetime.date(date.year, date.month, sprint_bill)
if date.day >= sprint_bill:
    sprint_billing_date = sprint_billing_date + relativedelta(months=+1)
special_lines = {"9178228005": "Art", "9177676186": "Work", "9292617744": "Anton", "6464139553": "Contract"}


# Other
paypal = "info@worldintercom.net"
btc = "https://pastebin.com/5pg6S7U2"










