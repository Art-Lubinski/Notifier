from selenium import webdriver
import pandas as pd
import time
import pyodbc
import sqlalchemy
import datetime
import model
import settings
from Naked.toolshed.shell import execute_js
import os
import re
import json

conn = pyodbc.connect(settings.sqlconnection_string)
cursor = conn.cursor()
cursor.execute(r"SELECT TOP 1 * FROM UsageHistory ORDER BY [Index] DESC")
last_update = cursor.fetchall()[0][2]


def update_sprint_usage():
    print("SCRAPER: updating sprint data usage from account now...")
    success = False
    if last_update != datetime.datetime.now().date():
        print(f"SCRAPER: data usage updated last time {last_update}. Updating...")
        try:
            print(settings.webdriver_path)
            driver = webdriver.Chrome(executable_path=settings.webdriver_path)
            try:
                driver.get("https://mysprint.sprint.com/mysprint/pages/sl/global/login.jsp?INTNAV=Header:SignInRegister")
                username = driver.find_element_by_xpath("""//*[@id="txtLoginUsernameDL"]""")
                driver.find_element_by_xpath("""//*[@id="txtLoginPasswordDL"]""").send_keys(settings.passwordSprint)
                username.send_keys(settings.usernameSprint)
                username.submit()
                time.sleep(1)
                driver.get("https://mysprint.sprint.com/mysprint/pages/secure/InterstitialCookieHandler?ICTarget=my.usage.usage.details&amp;INTNAV=ATG:HE:SeeAcctUsage")
                sprint_usage_df = pd.DataFrame()
                for n in range(4):
                    table_html = driver.find_element_by_xpath("/html/body/table/tbody/tr/td[1]/table/tbody/tr[4]/td/table/tbody/tr[15]/td/form/table").get_attribute('outerHTML')
                    df_list = pd.read_html(table_html)
                    df = df_list[0].drop(df_list[0].index[0])
                    sprint_usage_df = pd.concat([sprint_usage_df, df], sort=False)
                    if n < 3: driver.find_element_by_link_text("Next >>").click()
                usage = sprint_usage_df.iloc[:, [3, 11]]
                usage.insert(0, 'Date', datetime.datetime.now().strftime("%m/%d/%y"))
                usage.columns = ['Date', 'Number', 'Usage']
                usage.set_index('Number', inplace=True)
                import random
                usage["Usage"] = usage["Usage"].astype(float)
                usage.index = usage.index.map(str)
                cursor.execute(r"SELECT Number, ID FROM MobileNumbers WHERE AccountID in (select ID from MobileAccounts where Provider = 'Sprint')")
                map_df = pd.DataFrame([[x[0], x[1]] for x in cursor.fetchall()], columns=["Number", 'ID']).set_index('Number')
                usage_id_df = pd.merge(map_df, usage, left_index=True, right_index=True)
                usage_id_df.reset_index(drop=True, inplace=True)
                engine = sqlalchemy.create_engine(settings.sql_alchemy)
                usage_id_df.to_sql("UsageHistory", engine, if_exists='append', index=False)
                success = True
                driver.quit()
                print("SCRAPER: Sprint data usage scrapped and database updated")
                return success
            except Exception as e:
                print(f"SCRAPER: some error raised inside Sprint account. Code: {e}")
                return success
        except Exception as e:
            print(f"SELENIUM: cannot create webdriver. Code: {e}")
    else:
        print(f"SCRAPER: sprint has already been updated today")
    return success


# def update_verizon_usage():
#     success = False
#     lines = 0
#     verizon_usage = 0
#     if last_update != datetime.datetime.now().date():
#         try:
#             main_table_4g = model.Model.online.Main.Sheet4G().sheet.get_all_values()
#             success = execute_js("verizon_usage_scraper.js")
#             lines = []
#             if success:
#                 path1 = settings.data_folder_path + "verizon_usage.txt"
#                 path2 = settings.data_folder_path + "verizon_lines_usage.json"
#                 if os.path.exists(path1):
#                     verizon_usage = open(path1, "r")
#                     verizon_usage = verizon_usage.read().split()
#                     if len(verizon_usage) <= 2:
#                         verizon_usage = 0
#                     #os.remove(path1)
#                 if os.path.exists(path2):
#                     temp = []
#                     with open(path2) as f:
#                         data = json.load(f)
#                         for n in data:
#                             num = n.get('name').replace('-', '')
#                             use = n.get('usage')
#                             use = re.sub("[^0-9.]", '', use)
#                             temp1 = {'num': num, 'use': use}
#                             temp.append(temp1)
#                     #os.remove(path2)
#                     for pc_name, provider, number, email, is_panel in zip(main_table_4g[1], main_table_4g[4], main_table_4g[17], main_table_4g[7], main_table_4g[9]):
#                         if provider == 'VERIZON':
#                             for n in temp:
#                                 if number == n['num']:
#                                     if email == "" and is_panel == "1":
#                                         email = "panel"
#                                     data = {'name': pc_name, 'email': email, 'usage': n['use']}
#                                     lines.append(data)
#                     success = True
#                 else:
#                     lines = 0
#         except Exception as e:
#             print(f"Error. Code{e}")
#     else:
#         print(f"SCRAPER: verizon has already been updated today")
#     print(lines)
#     print(verizon_usage)
#     return success


def update_verizon_usage():
    print("SCRAPER: updating verizon data usage from account now...")
    success = False
    if last_update != datetime.datetime.now().date():
        print(f"SCRAPER: data usage updated last time {last_update}. Updating...")
        try:
            driver = webdriver.Chrome(executable_path=settings.webdriver_path)
            try:
                driver.get(
                    "https://mysprint.sprint.com/mysprint/pages/sl/global/login.jsp?INTNAV=Header:SignInRegister")
                username = driver.find_element_by_xpath("""//*[@id="txtLoginUsernameDL"]""")
                driver.find_element_by_xpath("""//*[@id="txtLoginPasswordDL"]""").send_keys(settings.passwordSprint)
                username.send_keys(settings.usernameSprint)
                username.submit()
                time.sleep(1)
                driver.get(
                    "https://mysprint.sprint.com/mysprint/pages/secure/InterstitialCookieHandler?ICTarget=my.usage.usage.details&amp;INTNAV=ATG:HE:SeeAcctUsage")
                sprint_usage_df = pd.DataFrame()
                for n in range(4):
                    table_html = driver.find_element_by_xpath(
                        "/html/body/table/tbody/tr/td[1]/table/tbody/tr[4]/td/table/tbody/tr[15]/td/form/table").get_attribute(
                        'outerHTML')
                    df_list = pd.read_html(table_html)
                    df = df_list[0].drop(df_list[0].index[0])
                    sprint_usage_df = pd.concat([sprint_usage_df, df], sort=False)
                    if n < 3: driver.find_element_by_link_text("Next >>").click()
                usage = sprint_usage_df.iloc[:, [3, 11]]
                usage.insert(0, 'Date', datetime.datetime.now().strftime("%m/%d/%y"))
                usage.columns = ['Date', 'Number', 'Usage']
                usage.set_index('Number', inplace=True)
                import random
                usage["Usage"] = usage["Usage"].astype(float)
                usage.index = usage.index.map(str)
                cursor.execute(
                    r"SELECT Number, ID FROM MobileNumbers WHERE AccountID in (select ID from MobileAccounts where Provider = 'Sprint')")
                map_df = pd.DataFrame([[x[0], x[1]] for x in cursor.fetchall()], columns=["Number", 'ID']).set_index(
                    'Number')
                usage_id_df = pd.merge(map_df, usage, left_index=True, right_index=True)
                usage_id_df.reset_index(drop=True, inplace=True)
                engine = sqlalchemy.create_engine(settings.sql_alchemy)
                usage_id_df.to_sql("UsageHistory", engine, if_exists='append', index=False)
                success = True
                driver.quit()
                print("SCRAPER: Sprint data usage scrapped and database updated")
                return success
            except Exception as e:
                print(f"SCRAPER: some error raised inside Sprint account. Code: {e}")
                return success
        except Exception as e:
            print(f"SELENIUM: cannot create webdriver. Code: {e}")
    else:
        print(f"SCRAPER: sprint has already been updated today")
    return success

