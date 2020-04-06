## this code was written by Serhat Aydin,
## data were taken from Github (time series-aggregated csv data file for all countries)

import pandas as pd
import smtplib

url = 'https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv' ## pull the data from github raw url
df = pd.read_csv(url, index_col=0) ## read data as dataframe with pandas library

tr = df.loc[df['Country']=='Turkey'] ## get data with respect to spesific country (if name of country == "Turkey") using .loc (boolean) method

tr_diff = tr[:] # copy data set to change over it
tr_diff[['dC', 'dR', 'dD']] = tr_diff[['Confirmed', 'Recovered', 'Deaths']].diff(1) ## add increment of confirmed case according to last 2 days. (subtraction of the last 2 rows)

def send_email(user, pwd, recipient, subject, body, cc=None, bcc=None): ## sen email function. Use smtplib for server connection.
    import smtplib

    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient] ## check recipient and return as list.
    SUBJECT = subject
    TEXT = body
    
    if cc and bcc==None:
        BCC = ['']
        CC = cc if isinstance(cc, list) else [cc]
        print('CC active')
    elif bcc and cc==None:
        CC = ['']
        BCC = bcc if isinstance(bcc, list) else [bcc]
        print('BCC active')
    elif cc and bcc:
        CC = cc if isinstance(cc, list) else [cc]
        BCC = bcc if isinstance(bcc, list) else [bcc]
        print('CC - BCC active')
    else:
        CC = ['']
        BCC = ['']
        print('Neither CC nor BCC')

    message = """From: %s\nTo: %s\nCc: %s\nBcc: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), ", ".join(CC), ", ".join(BCC), SUBJECT, TEXT)      
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, (TO + CC + BCC), message)
        server.close()
        print ('successfully sent the mail')
    except:
        print ("failed to send mail")

covid_text_last3days = "COVID-19 data for last 3 days of your country\n\n\n {}".format(tr_diff.tail(3))
covid_text_lastday = 'last day data ofs COVID-19 in your county\n\n\n' + 'dC, dR, dD: increment of each cases\n\n\n' + tr_diff.iloc[-1].to_string()
print (covid_text_last3days)

#send_email('sender_email_adress', 'sender_password', 'recipient(s)', 'subject', text, None, None)