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
server_username = "no-reply@dslrentals.com"
server_password = "winc4920520"
notify_from_email = server_username
server_host = "gator4059.hostgator.com"
server_port = 587
to_email = ["artsiom.lubinsky@gmail.com"]
paypal = "info@worldintercom.net"
btc = "https://pastebin.com/5pg6S7U2"
usernameSprint = "worldintercom1"
passwordSprint = "W663300w.1"
sprint_plan_limit = 120

special_lines = {"9178228005":"Art","9177676186":"Work","9292617744":"Anton"}