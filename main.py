import db
import emails
import settings
import datetime
import reports
import smtplib
import logs
import usage
import gspread
import data_usage

# gc = gspread.authorize(settings.google_credentials)
# sh = gc.open(settings.main_table)
# wks_main_table = sh.worksheet(settings.sheet_name_4g)
# main_table_4g = wks_main_table.get_all_values()
#
# date_in_two_days = datetime.date.today() + datetime.timedelta(days=2)
# date_today = datetime.date.today()
# date_yesterday = datetime.date.today() - datetime.timedelta(days=1)


# errors = db.check_errors()
# problem_list = db.get_lines_by_status("broken")
# sold_today = db.get_sold_lines_today()
# customers_to_close = db.get_customers(date_yesterday)
# customers_to_remind_today = db.get_customers(date_today)

# data_usage.update_sprint_usage()

data_usage.update_verizon_usage()
#
# try:
#     email_conn = smtplib.SMTP(settings.server_host, settings.server_port)
#     email_conn.ehlo()
#     email_conn.starttls()
#     email_conn.login(settings.server_username, settings.server_password)
#     if settings.mode == "prod" or settings.mode == "test_all":
#         emails.send_reminders(email_conn, customers_to_remind_today, date_today)
#         emails.send_reminders(email_conn, customers_to_remind_two_days, date_in_two_days)
#     emails.send_daily_report(email_conn, errors, customers_to_close, problem_list, sold_today, sprint_less_used, sprint_most_used, shared_usage, success, verizon_usage["lines"], verizon_usage["usage"])
#     if datetime.datetime.now().weekday() == 0:
#         weekly_report_start_date = datetime.date.today() - datetime.timedelta(days=7)
#         sales_report = reports.get_sales_report(weekly_report_start_date, date_yesterday)
#         emails.send_sales_report(email_conn, weekly_report_start_date, date_yesterday, sales_report, "weekly")
#     monthly_start_date = datetime.datetime(datetime.datetime.now().year, date_yesterday.month, 1)
#     if datetime.datetime.now().day == 1:
#         monthly_start_date = datetime.datetime(datetime.datetime.now().year, date_yesterday.month, 1)
#         sales_report = reports.get_sales_report(monthly_start_date.date(), date_yesterday)
#         reports.update_sold_lines(date_yesterday, sales_report, "sold")
#         reports.update_sold_lines(date_yesterday, sales_report, "renewed")
#         emails.send_sales_report(email_conn, monthly_start_date, date_yesterday, sales_report, "monthly")
#     email_conn.quit()
#
# except smtplib.SMTPException:
#     print("Connection to the server {0} has been failed for some reason..".format(settings.server_username))
#     logs.write_to_errors("Connection to the server {0} has been failed for some reason..".format(settings.server_username))
