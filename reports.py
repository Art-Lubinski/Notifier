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
    daily_sales = open(daily_sales_path, "r")
    table_purchase_CAN, table_renewed_CAN = _sales_report(daily_sales, from_date, to_date, "4G-CAN.*$")
    daily_sales = open(daily_sales_path, "r")
    table_purchase_AUS, table_renewed_AUS = _sales_report(daily_sales, from_date, to_date, "4G-AU1.*$")


    return table_purchase_4g, table_renewed_4g, table_purchase_dsl, table_renewed_dsl, table_purchase_CAN, table_renewed_CAN, table_purchase_AUS, table_renewed_AUS


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


def update_sold_lines(prev_month, wks_sold_lines_table, table_purchase_4g, table_purchase_dsl, table_purchase_CAN, table_purchase_AUS, type):
    first_column = wks_sold_lines_table.col_values(1)

    row1 = len(first_column) + 1
    cell_list = wks_sold_lines_table.range('A{0}:AH{0}'.format(row1))

    if len(table_purchase_4g) == 3:
        table_purchase_4g = [["trial",0,0]] + table_purchase_4g
        table_purchase_dsl = [["trial", 0, 0]] + table_purchase_dsl
        table_purchase_CAN = [["trial", 0, 0]] + table_purchase_CAN
        table_purchase_AUS = [["trial", 0, 0]] + table_purchase_AUS

    def prep_list(values, data):
        for n in range(0, 4):
            revenue_4g = data[n][1]
            lines_sold_4g = data[n][2]

            values.append(lines_sold_4g)
            values.append(revenue_4g)

            if lines_sold_4g == 0:
                mean = 0
            else:
                mean = revenue_4g / lines_sold_4g
            values.append(mean)
        return values

    def prep_list_other(values, data):
        for n in range(0, 4):
            values.append(data[n][1])
        return values

    values = []

    values.append(str(prev_month.strftime("%b %Y")))
    values.append(type)
    values = prep_list(values, table_purchase_dsl)
    values = prep_list(values, table_purchase_4g)
    values = prep_list_other(values, table_purchase_AUS)
    values = prep_list_other(values, table_purchase_CAN)

    for cell, value in zip(cell_list, values):
        cell.value = value
    wks_sold_lines_table.update_cells(cell_list)


