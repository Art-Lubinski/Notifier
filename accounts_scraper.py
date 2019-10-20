from selenium import webdriver
import logs
import time
from datetime import datetime
import os
import zipfile
from selenium import webdriver
import re

log = logs.write_to_balance_tracker

def scrape_verizon_wireless(username, password):
    log("SCRAPER: scraping Verizon wireless")
    scraped_accounts = []
    success = False
    try:
        driver = webdriver.Chrome(executable_path=r"C:\Program Files\Notifier\chromedriver.exe")
        driver.get(r"https://sso.verizonenterprise.com/amserver/sso/login.go")
        time.sleep(5)
        user_field = driver.find_element_by_xpath("/html/body/div[1]/div[1]/form/label[1]/input")
        user_field.send_keys(username)
        pass_field = driver.find_element_by_xpath("/html/body/div[1]/div[1]/form/label[2]/input")
        pass_field.send_keys(password)
        time.sleep(2)
        driver.find_element_by_xpath("/html/body/div[1]/div[1]/form/button").click()
        time.sleep(40)
        driver.get(r"https://b2b.verizonwireless.com/epam/app/ng/secure/entry.go#/lineSelection")
        log("SCRAPER: login successful")
        time.sleep(15)
        try:
            status1 = driver.find_element_by_xpath(
                "/html/body/div[4]/div[2]/div/div/div/div/div[3]/div[2]/div/div/div/div/div[3]/div[1]/div/div[2]/div[2]/div/div[14]/div/div/div[3]/div/span").text
            status2 = driver.find_element_by_xpath(
                "/html/body/div[4]/div[2]/div/div/div/div/div[3]/div[2]/div/div/div/div/div[3]/div[1]/div/div[2]/div[2]/div/div[21]/div/div/div[3]/div/span").text
        except:
            status1 = ""
            status2 = ""
            log("unknown if both accounts are active or suspended")
        driver.get(r"https://epb.verizonwireless.com/epass/reporting/main.go#/viewInvoices")
        log("SCRAPER: checking Invoices")
        time.sleep(15)
        for acc_number in [1, 2]:
            try:
                balance = float(driver.find_element_by_xpath("/html/body/div[7]/div/div/div[5]/div[4]/div[1]/div[3]/div[1]/div[2]/h1").text.replace("$","").replace(",",""))
            except Exception as e:
                balance = ""
                log(f"SCRAPER: balance not found. Code {e}")
            try:
                balance_forward = float(driver.find_element_by_xpath("/html/body/div[7]/div/div/div[5]/div[4]/div[3]/div[3]/div[2]/table/tbody/tr[3]/td[2]").text.replace("$","").replace(",",""))
            except Exception as e:
                balance_forward = ""
                log(f"SCRAPER: balance forward not found. Code {e}")
            try:
                curr_charges = float(driver.find_element_by_xpath("/html/body/div[7]/div/div/div[5]/div[4]/div[3]/div[3]/div[2]/table/tbody/tr[9]/td[2]").text.replace("$","").replace(",",""))
            except Exception as e:
                curr_charges = ""
                log(f"SCRAPER: current charge not found. Code {e}")
            try:
                rec_payment = float(driver.find_element_by_xpath("/html/body/div[7]/div/div/div[5]/div[4]/div[3]/div[3]/div[2]/table/tbody/tr[2]/td[2]").text.replace("$","").replace("-","").replace(",",""))
            except Exception as e:
                rec_payment = ""
                log(f"SCRAPER: recent payment not found. Code {e}")
            try:
                due_date = driver.find_element_by_xpath("/html/body/div[7]/div/div/div[5]/div[4]/div[3]/div[3]/div[2]/table/tbody/tr[10]/td[1]/div[2]").text
            except:
                due_date = ""
                log(f"SCRAPER: due date not found. Code {e}")
            if due_date != "" and "Due by" in due_date :
                due_date = due_date.replace("Due by ", "").replace(",", "")
                due_date = datetime.strptime(due_date, '%b %d %Y')
                due_date = due_date.strftime("%d/%m/%Y")
            if acc_number == 1: status = status1
            else: status = status2
            account = [f"VZ-{acc_number}", balance, balance_forward, curr_charges, rec_payment, status, due_date, ""]
            scraped_accounts.append(account)
            if acc_number == 1:
                try:
                    driver.find_element_by_xpath("/html/body/div[7]/div/div/div[5]/div[4]/div[1]/div[1]/div/div/a/span[1]").click()
                    time.sleep(1)
                    driver.find_element_by_xpath("/html/body/div[7]/div/div/div[5]/div[4]/div[1]/div[1]/div/div/ul/li[2]").click()
                    time.sleep(5)
                except:
                    log("SCRAPER: second account not found!")
        driver.quit()
        success = True
        log("SCRAPER: scraping VZ WIRELESS completed successfully")
    except Exception as e:
        driver.quit()
        log(f"STATUS: scraping VZ WIRELESS failed Code: {e}")
    return success, scraped_accounts

def scrape_comcast(username,password):
    log("scraping COMCAST now..")
    success = False
    scraped_accounts = []
    try:
        driver = webdriver.Chrome(executable_path=r"C:\Program Files\Notifier\chromedriver.exe")
        driver.delete_all_cookies()
        driver.get(r"https://login.xfinity.com/login?r=commercial&s=oauth&continue=https%3A%2F%2Foauth.xfinity.com%2Foauth%2Fauthorize%3Fclient_id%3Dcomcast-business-myaccount-prod%26redirect_uri%3Dhttps%253A%252F%252Fbusiness.comcast.com%252Faccount%252Fsignin-cima%26response_type%3Dcode%26scope%3Dopenid%2520profile%2520email%2520address%2520offline_access%2520phone%2520urn%253Abusiness-profileapi%2520urn%253Abusiness-notificationapi%26response_mode%3Dform_post%26max_age%3D1170%26state%3DCfDJ8MOMRjajdWhGi9VLQxAUOK-g6_yHVd6_u4t1LaVOl_abwuhoHcbTEsjYIOzGI7K_FEeGyYOdCkd0twzVf9EIccOkB-flehNSmtOQRf8sX79q2XC1ieT40VjqwBAoIN97mEGPRJj9GU3GVodiUKBDT2ZdtGQ0JsEEfi75leETlv0SOu3-P9Pv27YsLYpau56Zg5JP4GCi58eZ8Myg1qzgPgTyFSQ6msAoD15JAHD79GQEEHeOWvtNw1J32xFer8J_aLe9lnL2meWZn_h11KL8zVrTSrt5ZEz4IJy1qYcTkLXbbMkqwnDHS0vijIF5V58fzDfH11zZ5YS4dwzmy9v20DPckb2C1HDh1_mIcdW7b-su%26x-client-SKU%3DID_NET%26x-client-ver%3D2.1.4.0%26response%3D1&maxAuthnAge=1170&client_id=comcast-business-myaccount-prod&reqId=668bb638-79b4-4ad9-ae7c-3994510fb9e7")
        time.sleep(5)
        user_field = driver.find_element_by_xpath("/html/body/section[1]/div/div/div[2]/form/div/fieldset/div[1]/input")
        user_field.send_keys(username)
        pass_filed = driver.find_element_by_xpath("/html/body/section[1]/div/div/div[2]/form/div/fieldset/div[2]/input")
        pass_filed.send_keys(password)
        pass_filed.send_keys(u'\ue007')
        time.sleep(2)
        driver.find_element_by_xpath("/html/body/div/div/div/div/div[2]/p/a").click()
        log("SCRAPER: login successful COMCAST")
        time.sleep(10)
        accounts = [["GA-Comcast",1],["IL-Comcast",2],["TX-Comcast",3],["WA-Comcast",4]]
        for account in accounts:
            log(f"SCRAPER: scraping account {account[0]}")
            driver.get(r"https://business.comcast.com/myaccount/Secure/MyAccount/Bills/BillLanding/")
            try:
                time.sleep(7)
                driver.find_element_by_xpath(r"/html/body/div[1]/header/div[4]/div/nav/ul/li[3]/div/div/div[1]/div[2]/div/button").click()
                time.sleep(1)
                driver.find_element_by_xpath(f"/html/body/div[1]/header/div[4]/div/nav/ul/li[3]/div/div/div[1]/div[2]/div/div/ul/li[{account[1]}]").click()
                time.sleep(10)
                try:
                    text = driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/div/div[2]/div[6]/div[1]/div[2]/span/span[2]/span").text
                    if text != "" and "past due" in text: is_past_due = True
                    else: is_past_due = False
                except Exception as s:
                    log(f"SCRAPER: past due not found? {s}")
                driver.get(r"https://business.comcast.com/myaccount/Secure/MyAccount/Bills/BillPaySelectAmount/")
                time.sleep(10)
                try:
                    balance = driver.find_element_by_xpath("/html/body/form/div[2]/div/div/div[2]/div[2]/div[1]/div/div[1]/div/label/strong").text
                    balance = float(balance.replace("$", "").replace("Balance: ", ""))
                except Exception as s:
                    balance = ""
                    log(s)
                past_due = ""
                if is_past_due:
                    try:
                        past_due = driver.find_element_by_xpath(
                            "/html/body/form/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/label/strong").text
                        past_due = float(past_due.replace("$", "").replace("Past due: ", ""))
                    except Exception as s:
                        log(s)
                        past_due = ""
                scraped_account = [account[0], balance, past_due]
                scraped_accounts.append(scraped_account)
            except Exception as e:
                log(f"SCRAPER: can't switch between accounts. Code: {e}")
                return success
        driver.quit()
        success = True
        log("SCRAPER: successfully updated COMCAST")
    except Exception as e:
        log(f"SCRAPER: failure update COMCAST. Code {e}")
        driver.quit()
    return success, scraped_accounts

def scrape_verizon_dsl(username, password, secret, line):
    success = False
    scraped_account = []
    log(f"SCRAPER: scraping {line}")
    try:
        driver = webdriver.Chrome(executable_path=r"C:\Program Files\Notifier\chromedriver.exe")
        driver.delete_all_cookies()
        driver.get(r"https://www.verizon.com/home/myverizon/")
        time.sleep(5)
        driver.switch_to.frame(driver.find_element_by_id("DOMWindowIframe"))
        username_e = driver.find_element_by_xpath("//*[@id='IDToken1']")
        password_e = driver.find_element_by_xpath("//*[@id='IDToken2']")
        submit = driver.find_element_by_xpath("//*[@id='login-submit']")
        username_e.send_keys(username)
        password_e.send_keys(password)
        submit.click()
        time.sleep(5)
        try:
            secret_e = driver.find_element_by_id("IDToken1")
            secret_e.send_keys(secret)
            driver.find_element_by_id("otherButton").click()
            time.sleep(15)
        except:
            log("SCRAPER: secret key page doesn't exist in %s account" %line)
        try:
            driver.execute_script('document.querySelector("#remind_close").click()')
            time.sleep(20)
        except:
            log("SCRAPER: no email check in %s account" %line)
        try:
            acc_notice = driver.execute_script('return document.querySelector("#_idJsp0 > p").textContent;')
            dis_date = ""
            status = "Active"
            if "have been suspended" in acc_notice:
                status = "Suspended"
                dis_date = re.findall("received before .*", acc_notice)
                dis_date = dis_date[0].split()[-1].replace(".", "")
        except:
            status = ""
            dis_date = ""
        driver.get(r"https://www.verizon.com/foryourbusiness/billview/billing/mybill")
        time.sleep(15)
        try:
            balance = driver.execute_script('return document.querySelector("#ghfbodycontent > table > tbody > tr > td:nth-child(2) > div:nth-child(1) > main > div.row.padding-vert-zero > div > div > div > div.active > div.w_bill-outer > div > div.bill-value > span").textContent;')
            balance = float(balance)
        except:
            balance = ""
        try:
            due_date = driver.execute_script(
                'return document.querySelector("#ghfbodycontent > table > tbody > tr > td:nth-child(2) > div:nth-child(1) > main > div.row.padding-vert-zero > div > div > div > div.active > div.w_bill-outer > div > div.bill-due-date").textContent;')
            due_date = due_date.replace("By ", "").replace(",", "")
            due_date = datetime.strptime(due_date, '%B %d %Y')
            due_date = due_date.strftime("%d/%m/%Y")
        except:
            due_date = ""
        try:
            curr_charge = driver.execute_script('return document.querySelector("#ghfbodycontent > table > tbody > tr > td:nth-child(2) > div:nth-child(1) > main > div.row.padding-vert-zero > div > div > div > div.active > ul > li:nth-child(3) > div > div.column.tiny-4.bill-value").textContent;')
            curr_charge = float(curr_charge.strip().replace("$", ""))
        except:
            curr_charge = ""
        try:
            rec_payment = driver.execute_script('return document.querySelector("#ghfbodycontent > table > tbody > tr > td:nth-child(2) > div:nth-child(1) > main > div.row.padding-vert-zero > div > div > div > div.active > ul > li:nth-child(5) > div > div.column.tiny-4.bill-value").textContent;')
            rec_payment = float(rec_payment.strip().replace("$", ""))
        except:
            rec_payment = ""
        try:
            prev_charge = driver.execute_script('return document.querySelector("#ghfbodycontent > table > tbody > tr > td:nth-child(2) > div:nth-child(1) > main > div.row.padding-vert-zero > div > div > div > div.active > ul > li:nth-child(1) > div > div.column.tiny-4.bill-value").textContent;')
            prev_charge = float(prev_charge.strip().replace("$", ""))
        except:
            prev_charge = ""
        scraped_account = [line, balance, prev_charge, curr_charge,rec_payment, status, due_date, dis_date]
        driver.quit()
        success = True
        log(f"SCRAPER: scraping {line} completed successfully")
    except Exception as e:
        log(f"SCRAPER: scraping {line} failed...%s" %e)
        driver.quit()
    log(f"INFO: {line} balance: {balance} past due: {prev_charge} charged: {curr_charge} payment: {rec_payment} status: {status} due date: {due_date} termination: {dis_date}")
    return success, scraped_account

def scrape_att(username, password, line):
    success = False
    due_date = ""
    past_due = ""
    balance = ""
    curr_charge = ""
    account = []
    log("SCRAPER: scraping ATT")
    try:
        #driver = get_chromedriver(use_proxy=True)
        driver = webdriver.Chrome(executable_path=r"C:\Program Files\Notifier\chromedriver.exe")
        time.sleep(2)
        driver.get(r"https://www.att.com/my/#/login")
        time.sleep(10)
        driver.find_element_by_xpath("//*[@id='userName']").send_keys(username)
        driver.find_element_by_xpath("//*[@id='password']").send_keys(password)
        time.sleep(5)
        submit = driver.find_element_by_xpath("//*[@id='loginButton-lgwgLoginButton']")
        submit.click()
        time.sleep(30)
        try:
            driver.find_element_by_xpath("/html/body/div[13]/div/div/section[3]/button[2]").click()
            print("SCRAPER: survey found")
        except:
            print("SCRAPER: survey not found")
        try:
            balance = float(driver.find_element_by_xpath(
                "/html/body/div[2]/div/div[2]/div[2]/div/div/div/section/div/div[1]/div[1]/div[1]/div[2]/span/span[2]/span[2]").text.replace(",",""))
        except Exception as s:
            log(f"SCRAPER: balance not found. Code: {s}")
        try:
            past_due_field = driver.find_element_by_xpath(
                "/html/body/div[2]/div/div[2]/div[2]/div/div/div/section/div/div[1]/div[1]/div[2]/div[1]").text
            if past_due_field != "" and "past due" in past_due_field:
                past_due = float(past_due_field.replace(" past due", "").replace("$","").replace(",",""))
            elif past_due_field != "" and "Pay by" in past_due_field:
                due_date = datetime.strptime(past_due_field.replace("Pay by ","").replace(",",""), '%b %d %Y')
                due_date = due_date.strftime("%m/%d/%Y")
        except Exception as e:
            log(f"SCRAPER: can't identify either past due or not. Code: {e}")
        if balance == 0.0:
            driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[2]/div/div/div/section/div/div[1]/div[2]/button").click()
        else: driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[2]/div/div/div/section/div/div[1]/div[2]/a").click()
        time.sleep(25)
        try:
            if line == "FL-Cable":
                curr_charge_filed = driver.find_element_by_xpath(
                    '/html/body/div[2]/div/div[2]/div[2]/div/div/div/div/div/div[3]/div/section[2]/div[1]/div/div/div/div[1]/div[1]/div/div[1]/div[4]/div/div[1]/div[1]/span/div[2]/span[2]').text
            else: curr_charge_filed = driver.find_element_by_xpath('/html/body/div[10]/div/div[2]/div[1]/div[5]/div[1]/div/div/div[2]/div/div[2]/div[4]/div[3]/h3/span[2]').text
            '//*[@id="toggleBillChrgs"]/div[3]/h3/span[2]'
            '/html/body/div[10]/div/div[2]/div[1]/div[5]/div[1]/div/div/div[2]/div/div[2]/div[4]/div[3]/h3/span[2]'
            '//*[@id="toggleBillChrgs"]/div[1]/h3/span[2]'
            '/html/body/div[10]/div/div[2]/div[1]/div[5]/div[1]/div/div/div[2]/div/div[2]/div[4]/div[1]/h3/span[2]'
            curr_charge = float(curr_charge_filed.replace("$", '').replace(",", ""))
        except Exception as e:
            log(f"SCRAPER: current charge not found. Code: {e}")
        log(f"SCRAPER: scraping ATT finished successfully")
        driver.quit()
        account = [line, balance, past_due,curr_charge, due_date]
    except Exception as s:
        print(s)
        log(f"SCRAPER: scraping ATT failed. Code: {s}")
    return success, account

def scrape_spectrum(username, password, line):
    success = False
    due_date = ""
    past_due = ""
    balance = ""
    account = []
    try:
        driver = webdriver.Chrome(executable_path=r"C:\Program Files\Notifier\chromedriver.exe")
        driver.get(r"https://www.spectrumbusiness.net/login")
        time.sleep(5)
        driver.find_element_by_xpath("/html/body/div[1]/div[2]/ui-view/div/div/div/div[2]/div[1]/div[2]/div/div/div/div/div[3]/form/div[1]/sb-input/div/div[2]/div/input").send_keys(username)
        driver.find_element_by_xpath("/html/body/div[1]/div[2]/ui-view/div/div/div/div[2]/div[1]/div[2]/div/div/div/div/div[3]/form/div[2]/sb-input/div/div[2]/div[1]/input").send_keys(password)
        time.sleep(2)
        driver.find_element_by_name('login').submit()
        try:
            time.sleep(10)
            driver.find_element_by_xpath('/html/body/app-root/div/div/div/div[2]/ng-component/spectrum-auto-optin-content/div/ngk-card/div/ngk-typography/section/div[4]/button').click()
        except:
            print("no fucking survey")
        time.sleep(20)
        info = ""
        try:
            info = driver.execute_script('return document.querySelector("#sb-main-body > div.sb-main > div.sb-content.no-padding.ng-scope > ui-view > div > div.overview-content > div.overview-content--top > div > div.billing-support-cards > div.content-card.billing-card > div:nth-child(1) > div > span").textContent;')
            print(info)
        except Exception as e:
            print(e)
        print (info)
        if info != "":
            if "is due by" in info:
                text = info.split()
                due_date = text[-1]
            elif "Past Due:" in info:
                print(info)
                text = info.split()
                print(text)
                past_due = float(text[4].replace("$",""))
        try:
            acc_notice = driver.execute_script('return document.querySelector("#sb-main-body > div.sb-main > div.sb-content.no-padding.ng-scope > ui-view > div > div.overview-content > div.overview-content--top > div > div.billing-support-cards > div.content-card.billing-card > div.billing-card__bottom.ng-scope > div.billing-card__content-container > div.billing-card__block.billing_card__details-wrapper > div > span.balance.ng-binding").textContent;')
            balance = float(acc_notice.replace("$",""))
            print(balance)
        except Exception as e:
            print(e)
        print(balance, due_date, past_due)
        success = True
        account = [balance, due_date, past_due]
    except Exception as e:
        print(e)
    return success, account

