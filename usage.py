import credentials
import gspread
import pandas as pd


def check_data_usage():
    gc = gspread.authorize(credentials.google_credentials)

    sh = gc.open(credentials.wireless_table)
    wks = sh.worksheet(credentials.sheet_sprint)
    data_table = wks.get_all_values()
    sh = gc.open(credentials.main_table)
    wks = sh.worksheet(credentials.sheet_name_4g)
    main_table = wks.get_all_values()

    df1 = pd.read_csv(r"C:\Program Files\Usage Tracker\usage_today.csv", sep='\t')
    # df2 = pd.read_csv(r"C:\Program Files\Usage Tracker\usage_yesterday.csv", sep='\t')
    df1.phone = df1.phone.astype(str)
    df1.set_index('phone', inplace=True)

    dic_numbers_plans = {}
    for row in data_table:
        dic_numbers_plans[row[1]] = row[2]
    if "Number" in dic_numbers_plans:
        del dic_numbers_plans["Number"]

    data_usage = []
    data_name = []
    data_plan = []
    data_email = []

    for pc_name, provider, number, email in zip(main_table[1], main_table[4], main_table[17], main_table[7]):
        if provider == 'SPRINT':
            if number in df1.index:
                if number in dic_numbers_plans:
                    plan = dic_numbers_plans[number]
                else:
                    plan = "not found"
                if email == "":
                    email = "panel"
                data_name.append(pc_name)
                data_plan.append(plan)
                data_email.append(email)
                data_usage.append(round(df1.loc[number]["data"], 1))

    data = {'name':data_name, 'email': data_email, 'usage': data_usage, 'plan': data_plan}
    df = pd.DataFrame.from_dict(data)
    df.set_index('name', inplace=True)
    df.sort_values('usage', ascending=False, inplace=True)
    df_most_used = df.head(8)
    df_less_used = df.tail(8)
    dic_most_used = df_most_used.to_dict('index')
    dic_less_used = df_less_used.to_dict('index')
    return dic_less_used, dic_most_used



