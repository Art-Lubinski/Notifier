# Notifier
Programm helps send customer due date reminders, create various reports, notify about google sheets possible errors, control mobile data usage.

### Prerequisites
This program written for Proxy\VPN provider which used to heavily rely on manual labour. Five employees managed more than four hundred computers in two Google Sheets tables "4G Servers" and "DSL Servers". Each column represents single computer and each row is technical (PC name, Team-Viewer ID, password, phone number and etc.) or clients info (email, name, due dates, price\plan and etc.) Large database and manual entrees led to inconsistency, additional mistakes and time to fix them.

### What programm does?
- Keeps track of sold lines every day. Employees used to write daily sales report.
- Keeps track of list of broken lines and sets priority. Once a week employee made broken lines report and set priorities to fix them.
- Keeps track of lines that should be closed today. It was done by manally searching duedates in Google Spreadsheets.
- Sends weekly and monthly Sold Lines Report.
- Reminds customers about payment due date 3 and 1 day in advance.
- Gets mobile data usage from Sprint account, caculates daily usage, separate lines into groups (unlimited, shared), notify if client reached the limit.
- Keeps Google spread sheets consistent by checking many possible mistakes (Incorrect TV ID, missing password/email/name/phone number, wrong dates, mathcing phone numbers and etc.)


### Result
Programm starts at 12:01 am. When finished it sends report to manager, support department along with payment reminders for clients.

### Libraries used
- pandas
- selenium
- gspread
- smtplib
- os
- re
