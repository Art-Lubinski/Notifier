import db
import emails
import credentials
import datetime
import reports
import calendar
import smtplib
import logs
import usage
import gspread

gc = gspread.authorize(credentials.google_credentials)
sh = gc.open(credentials.main_table)
sh1 = gc.open(credentials.sold_lines)
wks_sold_lines_table = sh1.worksheet(credentials.sheet_sold_lines)
wks_main_table = sh.worksheet(credentials.sheet_name_4g)
main_table_4g = wks_main_table.get_all_values()
wks_main_table = sh.worksheet(credentials.sheet_name_dsl)
main_table_dsl = wks_main_table.get_all_values()

sh = gc.open(credentials.wireless_table)
wks_sprint = sh.worksheet(credentials.sheet_sprint)
sprint_table = wks_sprint.get_all_values()
wks_att = sh.worksheet(credentials.sheet_att)
att_table = wks_att.get_all_values()
wks_verizon = sh.worksheet(credentials.sheet_verizon)
verizon_table = wks_verizon.get_all_values()

table_4g = []
table_dsl = []

due_date_in_two_days = datetime.date.today() + datetime.timedelta(days=2)
due_date_today = datetime.date.today()
due_date_yesturday = datetime.date.today() - datetime.timedelta(days=1)


errors = db.check_errors(main_table_4g, main_table_dsl)
problem_list = db.get_lines_by_status("broken", main_table_4g, main_table_dsl)
sold_today = db.get_sold_lines_today(main_table_4g, main_table_dsl)
customers_to_close = db.get_customers(due_date_yesturday, main_table_4g, main_table_dsl)
customers_due_date_today = db.get_customers(due_date_today, main_table_4g, main_table_dsl)
customers_due_date_in_two_days = db.get_customers(due_date_in_two_days, main_table_4g, main_table_dsl)
sprint_less_used, sprint_most_used, success, shared_usage = usage.check_data_usage(main_table_4g)
verizon_usage, verizon_total_usage = usage.check_verizon_data_usage(main_table_4g)
usage.update_table_wireless_accounts("ATT", main_table_4g, att_table, wks_att)
usage.update_table_wireless_accounts("SPRINT", main_table_4g, sprint_table, wks_sprint)
usage.update_table_wireless_accounts("VERIZON", main_table_4g, verizon_table, wks_verizon)

try:
    email_conn = smtplib.SMTP(credentials.server_host, credentials.server_port)
    email_conn.ehlo()
    email_conn.starttls()
    email_conn.login(credentials.server_username, credentials.server_password)
    if credentials.mode == "prod" or credentials.mode == "test_all":
        emails.send_reminders(email_conn, customers_due_date_today, due_date_today)
        emails.send_reminders(email_conn, customers_due_date_in_two_days, due_date_in_two_days)
    emails.send_daily_report(email_conn, errors, customers_to_close, problem_list, sold_today, sprint_less_used, sprint_most_used, shared_usage, success, verizon_usage, verizon_total_usage)
    if datetime.datetime.now().weekday() == 0:
        weekly_report_start_date = datetime.date.today() - datetime.timedelta(days=7)
        table_purchase_4g, table_renewed_4g, table_purchase_dsl, table_renewed_dsl, table_purchase_CAN, table_renewed_CAN, table_purchase_AUS, table_renewed_AUS = reports.get_sales_report(weekly_report_start_date, due_date_yesturday)
        emails.send_sales_report(email_conn, weekly_report_start_date, due_date_yesturday, table_purchase_4g, table_renewed_4g, table_purchase_dsl, table_renewed_dsl,  "weekly")
    monthly_start_date = datetime.datetime(datetime.datetime.now().year, due_date_yesturday.month, 1)
    if datetime.datetime.now().day == 1:
        monthly_start_date = datetime.datetime(datetime.datetime.now().year, due_date_yesturday.month, 1)
        table_purchase_4g, table_renewed_4g, table_purchase_dsl, table_renewed_dsl, table_purchase_CAN, table_renewed_CAN, table_purchase_AUS, table_renewed_AUS = reports.get_sales_report(monthly_start_date.date(), due_date_yesturday)
        reports.update_sold_lines(due_date_yesturday, wks_sold_lines_table, table_purchase_4g, table_purchase_dsl, table_purchase_CAN, table_purchase_AUS, "sold")
        reports.update_sold_lines(due_date_yesturday, wks_sold_lines_table, table_renewed_4g, table_renewed_dsl, table_renewed_CAN, table_renewed_AUS, "renewed")
        emails.send_sales_report(email_conn, monthly_start_date, due_date_yesturday, table_purchase_4g, table_renewed_4g, table_purchase_dsl, table_renewed_dsl, "monthly")
    email_conn.quit()

except smtplib.SMTPException:
    print("Connection to the server {0} has been failed for some reason..".format(credentials.server_username))
    logs.write_to_errors("Connection to the server {0} has been failed for some reason..".format(credentials.server_username))