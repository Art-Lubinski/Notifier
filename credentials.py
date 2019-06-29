from oauth2client.service_account import ServiceAccountCredentials

mode = "prod"
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
google_credentials = ServiceAccountCredentials.from_json_keyfile_name(r"C:\Program Files\Notifier\Notifier-a4445923504c.json", scope)
sheet_name_dsl = "DSL Servers"
sheet_name_4g = "4G Servers"
sheet_sprint = "Sprint"
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
