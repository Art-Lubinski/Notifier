import db
import emails
import credentials
import datetime
import reports
import calendar
import smtplib
import logs
# lol
table_4g = []
table_dsl = []
send_weekly_report = False
send_monthly_report = False

due_date_in_two_days = datetime.date.today() + datetime.timedelta(days=2)
due_date_today = datetime.date.today()
due_date_yesturday = datetime.date.today() - datetime.timedelta(days=1)

errors = db.check_errors()
problem_list = db.get_lines_by_status("broken")
sold_today = db.get_sold_lines_today()
customers_to_close = db.get_customers(due_date_yesturday)
customers_due_date_today = db.get_customers(due_date_today)
customers_due_date_in_two_days = db.get_customers(due_date_in_two_days)

try:
    email_conn = smtplib.SMTP(credentials.server_host, credentials.server_port)
    email_conn.ehlo()
    email_conn.starttls()
    email_conn.login(credentials.server_username, credentials.server_password)
    emails.send_reminders(email_conn, customers_due_date_today, due_date_today)
    emails.send_reminders(email_conn, customers_due_date_in_two_days, due_date_in_two_days)
    emails.send_daily_report(email_conn, errors, customers_to_close, problem_list, sold_today)
    if datetime.datetime.now().weekday() == 0:
        weekly_report_start_date = datetime.date.today() - datetime.timedelta(days=7)
        table_purchase_4g, table_renewed_4g, table_purchase_dsl, table_renewed_dsl = reports.get_sales_report(weekly_report_start_date, due_date_yesturday)
        emails.send_sales_report(email_conn, weekly_report_start_date, due_date_yesturday, table_purchase_4g, table_renewed_4g, table_purchase_dsl, table_renewed_dsl,  "weekly")
    monthly_start_date = datetime.datetime(datetime.datetime.now().year, due_date_yesturday.month, 1)
    if datetime.datetime.now().day == 1:
        monthly_start_date = datetime.datetime(datetime.datetime.now().year, due_date_yesturday.month, 1)
        table_purchase_4g, table_renewed_4g, table_purchase_dsl, table_renewed_dsl = reports.get_sales_report(monthly_start_date.date(), due_date_yesturday)
        emails.send_sales_report(email_conn, monthly_start_date, due_date_yesturday, table_purchase_4g, table_renewed_4g, table_purchase_dsl, table_renewed_dsl, "monthly")
    email_conn.quit()

except smtplib.SMTPException:
    print("Connection to the server {0} has been failed for some reason..".format(credentials.server_username))
    logs.write_to_errors("Connection to the server {0} has been failed for some reason..".format(credentials.server_username))











