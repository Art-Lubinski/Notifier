import credentials
import gspread
import requests
import pandas as pd

gc = gspread.authorize(credentials.google_credentials)
sh = gc.open(credentials.quote_form_tab)
wks= sh.worksheet(credentials.panel_sheet)
panel_tab = wks.get_all_values()
url = "https://panel.dslrentals.com/export_data?pwd=pleaseshowittome&format=html&type=support"
html = requests.get(url).content
df_list = pd.read_html(html)
df = df_list[-1]

if len(df.index) != len(panel_tab):
    new_msg = df.iloc[len(panel_tab):].values
    date_upd = df.iloc[len(panel_tab):][1].values
    ip_upd = df.iloc[len(panel_tab):][2].values
    email_upd = df.iloc[len(panel_tab):][3].values
    name_upd = df.iloc[len(panel_tab):][4].values
    theme_upd = df.iloc[len(panel_tab):][5].values
    body_upd = df.iloc[len(panel_tab):][6].values

    length1 = len(panel_tab) + 1
    length2 = length1 + len(new_msg)
    time = wks.range('A{0}:A{1}'.format(length1,length2))
    name = wks.range('B{0}:B{1}'.format(length1,length2))
    email = wks.range('C{0}:C{1}'.format(length1,length2))
    ip = wks.range('D{0}:D{1}'.format(length1,length2))
    body = wks.range('F{0}:F{1}'.format(length1,length2))
    theme = wks.range('E{0}:E{1}'.format(length1,length2))

    for t, n, e, i, b, th, t_upd, n_upd, e_upd, i_upd, b_upd, th_upd in zip(time, name, email, ip, body, theme, date_upd, name_upd, email_upd, ip_upd,body_upd,theme_upd):
        t.value = t_upd
        n.value = n_upd
        e.value = e_upd
        i.value = i_upd
        b.value = b_upd
        th.value = th_upd

    wks.update_cells(time)
    wks.update_cells(name)
    wks.update_cells(email)
    wks.update_cells(ip)
    wks.update_cells(body)
    wks.update_cells(theme)