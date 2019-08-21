from oauth2client.service_account import ServiceAccountCredentials

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
wireless_table = "wireless_accounts"
server_username = ""
server_password = ""
notify_from_email = server_username
server_host = ""
server_port = 587
to_email = [""]
paypal = ""
btc = ""
usernameSprint = ""
passwordSprint = ""
sprint_plan_limit = 120

special_lines = {}
