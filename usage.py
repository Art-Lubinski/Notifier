from selenium import webdriver
import settings
import gspread
import pandas as pd
import logs
import time
import datetime
from Naked.toolshed.shell import execute_js
import re
import json
import os

gc = gspread.authorize(settings.google_credentials)
sh = gc.open(settings.wireless_table)
wks1 = sh.worksheet(settings.sheet_sprint)
data_table = wks1.get_all_values()
sh = gc.open(settings.main_table)
wks = sh.worksheet(settings.sheet_name_4g)
main_table = wks.get_all_values()


def check_data_usage(main_table_4g):
    success = False
    dic_less_used = {}
    dic_most_used = {}
    shared_total_usage = 0

    try:
        driver = webdriver.Chrome(executable_path=r"C:\Program Files\Notifier\chromedriver.exe")
        # driver = webdriver.Firefox(executable_path=r"C:\Program Files\Usage Tracker\geckodriver.exe")

        try:
            driver.get("https://mysprint.sprint.com/mysprint/pages/sl/global/login.jsp?INTNAV=Header:SignInRegister")
            username = driver.find_element_by_xpath("""//*[@id="txtLoginUsernameDL"]""")
            password = driver.find_element_by_xpath("""//*[@id="txtLoginPasswordDL"]""")
            username.send_keys(settings.usernameSprint)
            password.send_keys(settings.passwordSprint)
            username.submit()
            time.sleep(1)
            driver.get((
                           "https://mysprint.sprint.com/mysprint/pages/secure/InterstitialCookieHandler?ICTarget=my.usage.usage.details&amp;INTNAV=ATG:HE:SeeAcctUsage"))
            sprint_usage_df = pd.DataFrame()
            for n in range(4):
                table_html = driver.find_element_by_xpath(
                    "/html/body/table/tbody/tr/td[1]/table/tbody/tr[4]/td/table/tbody/tr[15]/td/form/table").get_attribute('outerHTML')
                df_list = pd.read_html(table_html)
                df = df_list[0].drop(df_list[0].index[0])
                sprint_usage_df = pd.concat([sprint_usage_df, df], sort=False)
                if n < 3:
                    driver.find_element_by_link_text("Next >>").click()
            with open(r"C:\Program Files\Notifier\Data\usage_today.csv") as usage_today:
                with open(r"C:\Program Files\Notifier\Data\usage_yesterday.csv", "w") as usage_yesterday:
                    for line in usage_today:
                        usage_yesterday.write(line)
            sprint_usage_df = sprint_usage_df.iloc[:, [1, 3, 11]]
            sprint_usage_df.columns = ['name', 'phone', 'data']
            sprint_usage_df = sprint_usage_df.reset_index(drop=True)
            sprint_usage_df.to_csv(r"C:\Program Files\Notifier\Data\usage_today.csv""", sep='\t', index=False)

            today_df = pd.read_csv(r"C:\Program Files\Notifier\Data\usage_today.csv", sep='\t')

            today_df = today_df.drop("name", axis=1)
            today_df.set_index("phone",inplace=True)

            today_df = today_df.T

            today_df["lol"] = datetime.datetime.now().date()

            today_df.set_index("lol", inplace=True)
            del today_df.index.name

            today_df.to_csv(r"C:\Program Files\Notifier\Data\usage_today_single_row.csv", sep='\t')
            single_row = pd.read_csv(r"C:\Program Files\Notifier\Data\usage_today_single_row.csv", sep='\t', index_col=0)
            history_df = pd.read_csv(r"C:\Program Files\Notifier\Data\usage_history.csv", sep='\t', index_col=0)

            history_df_concat = pd.concat([history_df, single_row], sort=False)
            history_df_concat.to_csv(r"C:\Program Files\Notifier\Data\usage_history.csv", sep='\t')

            driver.quit()
            logs.write_to_log("Sprint Usage tracker: finished with exit code 0")
            success = True

        except Exception as e:
            logs.write_to_errors("Sprint Usage tracker: data usage hasn't been updated ({0})".format(e))

        try:
            sprint_usage_df = pd.read_csv(r"C:\Program Files\Notifier\Data\usage_today.csv", sep='\t')
            df2 = pd.read_csv(r"C:\Program Files\Notifier\Data\usage_yesterday.csv", sep='\t')
            sprint_usage_df.phone = sprint_usage_df.phone.astype(str)
            sprint_usage_df.set_index('phone', inplace=True)
            sprint_usage_df.columns = ['name', 'usage_today']
            df2.phone = df2.phone.astype(str)
            df2.set_index('phone', inplace=True)
            df2 = df2.drop('name', axis=1)
            df2.columns = ['usage_yesterday']
            r = pd.concat([sprint_usage_df, df2], axis=1, sort=False)
            r['used_today'] = r["usage_today"] - r["usage_yesterday"]
            sprint_usage_df = r

            dic_numbers_plans = {}
            for row in data_table:
                dic_numbers_plans[row[1]] = row[2]
            if "Number" in dic_numbers_plans:
                del dic_numbers_plans["Number"]

            t = pd.DataFrame.from_dict(dic_numbers_plans.items())
            t.columns = ["phone","plan"]
            t.set_index('phone', inplace=True)
            sprint_usage_df = pd.concat([sprint_usage_df, t], axis=1, sort=False)
            shared_total_usage = sprint_usage_df.groupby(by=['plan'])['usage_today'].sum()
            shared_total_usage = shared_total_usage.iloc[0]

            number_shared_lines = 0
            for k, v in dic_numbers_plans.items():
                if v == 'shared':
                    number_shared_lines = number_shared_lines + 1
            data_usage = []
            data_name = []
            data_plan = []
            data_email = []
            data_used_today = []
            data_overusage = []
            for pc_name, provider, number, email in zip(main_table_4g[1], main_table_4g[4], main_table_4g[17], main_table_4g[7]):
                overusage = False
                if provider == 'SPRINT':
                    if number in sprint_usage_df.index:
                        if number in dic_numbers_plans:
                            plan = dic_numbers_plans[number]
                        else:
                            plan = "not found"
                        if email == "":
                            email = "panel"
                        data_name.append(pc_name)
                        data_plan.append(plan)
                        data_email.append(email)
                        data_usage.append(round(sprint_usage_df.loc[number]["usage_today"], 1))
                        data_used_today.append(round(sprint_usage_df.loc[number]["used_today"], 1))
                        if round(sprint_usage_df.loc[number]["usage_today"], 1) > settings.sprint_plan_limit/number_shared_lines and plan == "shared":
                            overusage = True
                        data_overusage.append(overusage)
            data = {'name': data_name, 'email': data_email, 'usage': data_usage, 'plan': data_plan, 'used_today': data_used_today, 'overusage': data_overusage}
            df = pd.DataFrame.from_dict(data)
            df.set_index('name', inplace=True)
            df.sort_values('usage', ascending=False, inplace=True)
            df_most_used = df.head(10)
            df_less_used = df.tail(10)
            dic_most_used = df_most_used.to_dict('index')
            dic_less_used = df_less_used.to_dict('index')
        except Exception as e:
            logs.write_to_log("Sprint Usage tracker: unknown error ({0})".format(e))

    except Exception as e:
        logs.write_to_log("Sprint usage tracker: either web driver not found or it has an issue ({0})".format(e))
    return dic_less_used, dic_most_used, success, shared_total_usage


def update_table_wireless_accounts(provider_name, main_table_4g, provider_table, wks):
    sprint_numbers_from_table = []
    for pc_name, provider, number, email, customer, if_panel, modem, if_broken in zip(main_table_4g[1], main_table_4g[4], main_table_4g[17], main_table_4g[7], main_table_4g[6], main_table_4g[9],  main_table_4g[5], main_table_4g[10]):
        if provider == provider_name:
            if number == "":
                number = "not found"
            if email == "" and if_panel == "1":
                customer = "panel"
            modem = modem.split()
            if len(modem) == 0:
                modem = ""
            else: modem = modem[0]
            pc = {"phone": number, "pc_name": pc_name, "email": email, "customer": customer, "modem": modem}
            sprint_numbers_from_table.append(pc)

    length = len(provider_table)

    numbers = wks.range('B2:B{0}'.format(length))
    lines = wks.range('A2:A{0}'.format(length))
    clients = wks.range('E2:E{0}'.format(length))
    modems = wks.range('D2:D{0}'.format(length))

    for phone, line, client, modem in zip(numbers, lines, clients, modems):
        line.value = "not found"
        client.value = ""
        modem.value = ""
        if phone.value in settings.special_lines:
            line.value = settings.special_lines[phone.value]
        for pc in sprint_numbers_from_table:
            if pc["phone"] == phone.value:
                line.value = pc["pc_name"]
                client.value = pc["customer"]
                modem.value = pc["modem"]

    wks.update_cells(lines)
    wks.update_cells(clients)
    wks.update_cells(modems)


def check_verizon_data_usage(main_table_4g):
    os.chdir(r"C:\Program Files\Notifier")
    success = execute_js(r"verizon_scraper.js")
    lines = []
    if success:
        path1 = r"C:\Program Files\Notifier\Data\verizon_usage.txt"
        path2 = r"C:\Program Files\Notifier\Data\verizon_lines_usage.json"
        if os.path.exists(path1):
            verizon_usage = open(path1, "r")
            verizon_usage = verizon_usage.read().split()
            if len(verizon_usage) <= 2:
                verizon_usage = 0
            os.remove(path1)
        else:
            verizon_usage = 0
        if os.path.exists(path2):
            temp = []
            with open(r"C:\Program Files\Notifier\Data\verizon_lines_usage.json") as f:
                data = json.load(f)
                for n in data:
                    num = n.get('name').replace('-', '')
                    use = n.get('usage')
                    use = re.sub("[^0-9.]", '', use)
                    temp1 = {'num': num, 'use': use}
                    temp.append(temp1)
            os.remove(path2)

            for pc_name, provider, number, email, is_panel in zip(main_table_4g[1], main_table_4g[4], main_table_4g[17], main_table_4g[7], main_table_4g[9]):
                if provider == 'VERIZON':
                    for n in temp:
                        if number == n['num']:
                            if email == "" and is_panel == "1":
                                email = "panel"
                            data = {'name': pc_name, 'email': email, 'usage': n['use']}
                            lines.append(data)
        else:
            lines = 0

    return lines, verizon_usage





