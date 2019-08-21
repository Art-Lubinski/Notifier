import os
import datetime
import re

current_dir = os.path.realpath(__file__)
folder_path = current_dir[:-11] + "/Logs"
daily_sales_path = folder_path + "/daily_sales.txt"
print(daily_sales_path)


def get_sales_report(from_date, to_date):
    daily_sales = open(daily_sales_path, "r")
    table_purchase_4g, table_renewed_4g = _sales_report(daily_sales, from_date, to_date, "^4G-.*$")
    daily_sales = open(daily_sales_path, "r")
    table_purchase_dsl, table_renewed_dsl = _sales_report(daily_sales, from_date, to_date, "DSL-.*$")
    return table_purchase_4g, table_renewed_4g, table_purchase_dsl, table_renewed_dsl


def _sales_report(daily_sales, from_date, to_date, regex):
    table_purchase = [
        ['trial',0,0],
        ['weekly',0,0],
        ['bi-weekly',0,0],
        ['monthly',0,0,],
    ]
    table_renewed = [
        ['weekly',0, 0,],
        ['biweekly',0, 0,],
        ['monthly', 0, 0,],
    ]
    for x in daily_sales:
        a = x.split()
        if len(a) != 0:
            b = datetime.datetime.strptime(a[0], '%Y-%m-%d').date()
            if from_date <= b <= to_date:
                if re.findall(regex, a[1]):
                    if a[5] == "purchase":
                        if a[3] == "trial":
                            table_purchase[0][1] = table_purchase[0][1] + int(a[4])
                            table_purchase[0][2] = table_purchase[0][2] + 1
                        elif a[3] == "weekly":
                            table_purchase[1][1] = table_purchase[1][1] + int(a[4])
                            table_purchase[1][2] = table_purchase[1][2] + 1

                        elif a[3] == "biweekly":
                                table_purchase[2][1] = table_purchase[2][1] + int(a[4])
                                table_purchase[2][2] = table_purchase[2][2] + 1
                        elif a[3] == "monthly":
                                table_purchase[3][1] = table_purchase[3][1] + int(a[4])
                                table_purchase[3][2] = table_purchase[3][2] + 1
                    else:
                        if a[3] == "weekly":
                            table_renewed[0][1] = table_renewed[0][1] + int(a[4])
                            table_renewed[0][2] = table_renewed[0][2] + 1
                        elif a[3] == "biweekly":
                            table_renewed[1][1] = table_renewed[1][1] + int(a[4])
                            table_renewed[1][2] = table_renewed[1][2] + 1
                        elif a[3] == "monthly":
                            table_renewed[2][1] = table_renewed[2][1] + int(a[4])
                            table_renewed[2][2] = table_renewed[2][2] + 1

    return table_purchase, table_renewed

