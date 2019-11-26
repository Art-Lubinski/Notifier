from selenium import webdriver
import pandas as pd
import time
import sqlalchemy
import datetime
import connections
import settings
import logs

log = logs.write_to_balance_tracker

conn = connections.conn
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


def update_verizon_usage():
    success = False
    print("SCRAPER: updating verizon data usage from account now...")
    if last_update != datetime.datetime.now().date():
        print(f"SCRAPER: data usage updated last time {last_update}. Updating...")
        try:
            driver = webdriver.Chrome(executable_path=settings.webdriver_path)
            try:
                driver.get("https://sso.verizonenterprise.com/amserver/sso/login.go")
                username = driver.find_element_by_xpath('/html/body/div[1]/div[1]/form/label[1]/input')
                driver.find_element_by_xpath('/html/body/div[1]/div[1]/form/label[2]/input').send_keys(settings.passwordVerizon)
                username.send_keys(settings.usernameVerizon)
                username.submit()
                time.sleep(15)
                driver.get("https://b2b.verizonwireless.com/sms/amsecure/unbilledusage/allLinesUsage.go?mtn=929-236-5003")
                time.sleep(10)
                usages = driver.find_elements_by_class_name("usage")
                numbers = driver.find_elements_by_class_name("mtn")
                lines_list = []
                for number, usage in zip(numbers, usages):
                    number = number.text
                    usage = usage.text
                    lines_list.append([number.replace("-",""),float(usage.replace(" GB", ""))])
                print(lines_list)
                df = pd.DataFrame(lines_list, columns=['Number', 'Usage'])
                df.set_index('Number', inplace=True)
                df.insert(0, 'Date', datetime.datetime.now().strftime("%m/%d/%y"))
                df.index = df.index.map(str)
                try:
                    cursor.execute("SELECT Number, ID FROM MobileNumbers WHERE AccountID in (select ID from MobileAccounts where Provider = 'Verizon')")
                except Exception as e:
                    print(f"SQL REQUEST: pyodbc can't complete request. Code{e}")
                map_df = pd.DataFrame([[x[0], x[1]] for x in cursor.fetchall()], columns=["Number", 'ID']).set_index('Number')
                usage_id_df = pd.merge(map_df, df, left_index=True, right_index=True)
                usage_id_df.reset_index(drop=True, inplace=True)
                engine = sqlalchemy.create_engine(settings.sql_alchemy)
                usage_id_df.to_sql("UsageHistory", engine, if_exists='append', index=False)
                success = True
                print("SCRAPER: Verizon data usage scrapped and database updated")
                return success
            except Exception as e:
                print(f"SCRAPER: some error raised inside Verizon account. Code: {e}")
                return success
        except Exception as e:
            print(f"SELENIUM: cannot create webdriver. Code: {e}")
    else:
        print(f"SCRAPER: verizon has already been updated today")
    return success
