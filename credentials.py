from oauth2client.service_account import ServiceAccountCredentials
import datetime
from dateutil.relativedelta import relativedelta

mode = "prod"
# test_all - sends reminders and ALL emails to Art
# test - sends emails to Art(except reminders). Doesnt write to log file
# prod - production

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
google_credentials = ServiceAccountCredentials.from_json_keyfile_name(r"C:\Program Files\Notifier\Notifier-a4445923504c.json", scope)
sheet_name_dsl = "DSL Servers"
sheet_name_4g = "4G Servers"
sheet_sprint = "Sprint"
sheet_att = "ATT"
sheet_verizon = "Verizon"
main_table = "DSL Rentals Servers"
sold_lines = "Sold lines"
sheet_sold_lines = "Auto report"
wireless_table = "wireless_accounts"
server_username = "no-reply@dslrentals.com"
server_password = "winc4920520"
notify_from_email = server_username
server_host = "87.237.138.67"
server_port = 588
to_email = ["artsiom.lubinsky@gmail.com"]
paypal = "info@worldintercom.net"
btc = "https://pastebin.com/5pg6S7U2"
usernameSprint = "worldintercom1"
passwordSprint = "W663300w.123"
sprint_plan_limit = 120
sprint_bill = 16
quote_form_tab = "Quote form requests"
panel_sheet = "Panel form"

date = datetime.date.today()
sprint_billing_date = datetime.date(date.year, date.month, sprint_bill)
if date.day >= sprint_bill:
    sprint_billing_date = sprint_billing_date + relativedelta(months=+1)


special_lines = {"9178228005":"Art","9177676186":"Work","9292617744":"Anton","6464139553":"Contract"}