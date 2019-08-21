import os
import datetime
import sys
import credentials

current_dir = os.path.realpath(__file__)

folder_path = current_dir[:-8] + "/Logs"
logs_path = folder_path + "/logs.txt"
errors_path = folder_path + "/errors.txt"
statistics_path = folder_path + "/statistics.txt"
daily_sales_path = folder_path + "/daily_sales.txt"
sprint_usage_path = folder_path + "/usage_sprint.txt"

if sys.platform == "win32":
    folder_path = folder_path.replace("/","\\")
    logs_path = logs_path.replace("/","\\")
    errors_path = errors_path.replace("/","\\")
    statistics_path = statistics_path.replace("/","\\")
    daily_sales_path = daily_sales_path.replace("/", "\\")
    sprint_usage_path = sprint_usage_path.replace("/", "\\")

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

logs = open(logs_path, "a")
errors = open(errors_path, "a")
statistics = open(statistics_path, "a")
daily_sales = open(daily_sales_path, "a")
sprint_usage = open(sprint_usage_path, "a")

def write_to_log(message):
    timestamp = datetime.datetime.now() - datetime.timedelta(days=1)
    message = str(timestamp.date()) + " " + message + "\n"
    logs.write(message)

def write_to_errors(message):
    timestamp = datetime.datetime.now() - datetime.timedelta(days=1)
    message = str(timestamp.date()) + " " + message + "\n"
    errors.write(message)

def write_to_daily_sales(message):
    if credentials.mode == "prod":
        timestamp = datetime.datetime.now() - datetime.timedelta(days=1)
        message = str(timestamp.date()) + " " + message + "\n"
        daily_sales.write(message)

def write_to_statistics(message):
    timestamp = datetime.datetime.now() - datetime.timedelta(days=1)
    message = str(timestamp.date()) + " " + message + "\n"
    statistics.write(message)

def write_to_usage(message):
    if credentials.mode == "prod":
        timestamp = datetime.datetime.now()
        message = str(timestamp.date()) + " " + message + "\n"
        sprint_usage.write(message)