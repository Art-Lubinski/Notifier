import imaplib
from selenium import webdriver
import pandas as pd
import time
import pyodbc
import sqlalchemy
import datetime
import settings
import re
import base64
import email
import logs
import random

conn = pyodbc.connect(settings.sqlconnection_string)
cursor = conn.cursor()
# cursor.execute(r"SELECT TOP 1 * FROM UsageHistory ORDER BY 'Index' DESC")
# try:
#     last_update = cursor.fetchall()[0][2]
# except:
#     last_update = ""

def GetSprintPasscode():
    from_email = "info@worldintercom.net"
    from_pwd = "comN#cVDG%&vG$"
    smtp_server = "gator3066.hostgator.com"
    while True:
        try:
            mail = imaplib.IMAP4_SSL(smtp_server)
            mail.login(from_email , from_pwd)
            mail.select('inbox')
            type, data = mail.search(None, 'ALL')
            mail_ids = data[0]
            id_list = mail_ids.split()
            first_email_id = int(id_list[-2])
            latest_email_id = int(id_list[-1])
            for i in range(latest_email_id,first_email_id, -1):
                typ, data = mail.fetch(str(i),"(RFC822)")
                for response_part in data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_string(str(response_part[1]))
                        base64str = msg.as_string()
            base64str = base64str.split(" ")

            body = ""
            for word in base64str:
                if len(word) > 150:
                    word = word.replace(" ","").replace("base64","").replace("","")
                    msg = word.split("\\r\\n")
                    del msg[0]
                    del msg[0]
                    del msg[-1]
                    del msg[-1]
                    del msg[-1]
                    for n in msg:
                        body = body + str(base64.b64decode(n))
            object = re.findall("one-time passcode [0-9]{5}", body)
            passcode = object[0].split()[-1]
            match = re.search("[0-9]{5}",passcode)
            if match != None:
                return passcode
            else:
                time.sleep(2)
        except Exception as ex:
            logs.write_to_errors(ex)


def update_sprint_usage():
    success = False
    try:
        driver = webdriver.Chrome(executable_path=settings.webdriver_path)
        try:
            driver.get("https://www.sprint.com/content/sprint/sprint_com/us/en/login.html?")
            username = driver.find_element_by_xpath("/html/body/div[1]/main/div[3]/div[2]/div[1]/form/div/div[1]/div[1]/input")
            driver.find_element_by_xpath("/html/body/div[1]/main/div[3]/div[2]/div[1]/form/div/div[1]/div[2]/input").send_keys(settings.passwordSprint)
            username.send_keys(settings.usernameSprint)
            username.submit()
            time.sleep(15)
            try:
                print("chp2")
                x = ""
                try:
                    x = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[1]/h2").text
                except:
                    logs.write_to_errors("Passcode check not found")
                if "security" in x:
                    driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/form/div/fieldset/div[1]/label").click()
                    time.sleep(1)
                    driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/form/div/fieldset/div[2]/a").click()
                    time.sleep(30)
                    passcode = GetSprintPasscode()
                    driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/form/div/div[1]/p/encrp3/input").send_keys(passcode)
                    time.sleep(2)
                    driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/form/div/div[2]/a/span/span/span/span").click()
                    time.sleep(10)
            except:
                logs.write_to_errors("Exception inside passcode check")
            driver.get("https://mysprint.sprint.com/mysprint/pages/secure/InterstitialCookieHandler?ICTarget=my.usage.usage.details&amp;INTNAV=ATG:HE:SeeAcctUsage")
            time.sleep(10)
            sprint_usage_df = pd.DataFrame()
            for n in range(4):
                table_html = driver.find_element_by_xpath("/html/body/table/tbody/tr/td[1]/table/tbody/tr[4]/td/table/tbody/tr[15]/td/form/table").get_attribute('outerHTML')
                df_list = pd.read_html(table_html)
                df = df_list[0].drop(df_list[0].index[0])
                sprint_usage_df = pd.concat([sprint_usage_df, df], sort=False)
                if n < 3: driver.find_element_by_link_text("Next >>").click()
            print("chp3")
            usage = sprint_usage_df.iloc[:, [3, 11]]
            usage.insert(0, 'Date', datetime.datetime.now().strftime("%m/%d/%y"))
            usage.columns = ['Date', 'Number', 'Usage']
            usage.set_index('Number', inplace=True)
            usage["Usage"] = usage["Usage"].astype(float)
            usage.index = usage.index.map(str)
            cursor.execute(r"SELECT Number, ID FROM MobileNumbers WHERE AccountID in (select ID from Accounts where Provider = 'Sprint')")
            map_df = pd.DataFrame([[x[0], x[1]] for x in cursor.fetchall()], columns=["Number", 'ID']).set_index('Number')
            usage_id_df = pd.merge(map_df, usage, left_index=True, right_index=True)
            usage_id_df.reset_index(drop=True, inplace=True)
            engine = sqlalchemy.create_engine(settings.sql_alchemy)
            usage_id_df.to_sql("UsageHistory", engine, if_exists='append', index=False)
            success = True
            logs.write_to_errors("SCRAPER: Sprint data usage scrapped and database updated")
            driver.quit()
            return success
        except Exception as e:
            logs.write_to_errors(f"SCRAPER: some error raised inside Sprint account. Code: {e}")
            return success
    except Exception as e:
        logs.write_to_errors(f"SELENIUM: cannot create webdriver. Code: {e}")
    return success


def update_verizon_usage():
    success = False
    try:
        driver = webdriver.Chrome(executable_path=settings.webdriver_path)
        try:
            driver.get("https://sso.verizonenterprise.com/amserver/sso/login.go")
            username = driver.find_element_by_xpath('/html/body/div[1]/div[1]/form/label[1]/input')
            driver.find_element_by_xpath('/html/body/div[1]/div[1]/form/label[2]/input').send_keys(settings.passwordVerizon)
            username.send_keys(settings.usernameVerizon)
            username.submit()
            time.sleep(15)
            try:
                device_check = driver.find_element_by_xpath('/html/body/div[1]/div[4]/h1').text
                print(device_check)
                time.sleep(5)
                if device_check == "Device not recognized":
                    driver.execute_script('document.querySelector("body > div.container.setHeight > div.padleft15.padright15.col-xs-0.col-sm-8 > div.ng-scope > div > div:nth-child(3) > div > div > strong > span > a").click()')
                    time.sleep(5)
                    driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[4]/div/div[2]/form/div[1]/div/input').send_keys("kostya")
                    time.sleep(2)
                    driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[4]/div/div[2]/form/div[3]/button').click()
                    time.sleep(25)
            except Exception as ex:
                print(ex)
            driver.get("https://b2b.verizonwireless.com/sms/amsecure/unbilledusage/allLinesUsage.go?mtn=929-236-5003")
            time.sleep(10)
            usages = driver.find_elements_by_class_name("usage")
            numbers = driver.find_elements_by_class_name("mtn")
            lines_list = []
            for number, usage in zip(numbers, usages):
                number = number.text
                usage = usage.text
                lines_list.append([number.replace("-",""),float(usage.replace(" GB", ""))])
            df = pd.DataFrame(lines_list, columns=['Number', 'Usage'])
            df.set_index('Number', inplace=True)
            df.insert(0, 'Date', datetime.datetime.now().strftime("%m/%d/%y"))
            df.index = df.index.map(str)
            try:
                cursor.execute("SELECT Number, ID FROM MobileNumbers WHERE AccountID in (select ID from Accounts where Provider = 'Verizon')")
            except Exception as e:
                logs.write_to_errors(f"SQL REQUEST: pyodbc can't complete request. Code{e}")
            map_df = pd.DataFrame([[x[0], x[1]] for x in cursor.fetchall()], columns=["Number", 'ID']).set_index('Number')
            usage_id_df = pd.merge(map_df, df, left_index=True, right_index=True)
            usage_id_df.reset_index(drop=True, inplace=True)
            engine = sqlalchemy.create_engine(settings.sql_alchemy)
            usage_id_df.to_sql("UsageHistory", engine, if_exists='append', index=False)
            success = True
            logs.write_to_errors("SCRAPER: Verizon data usage scrapped and database updated")
            driver.quit()
            return success
        except Exception as e:
            logs.write_to_errors(f"SCRAPER: some error raised inside Verizon account. Code: {e}")
            return success
    except Exception as e:
        logs.write_to_errors(f"SELENIUM: cannot create webdriver. Code: {e}")
    return success

