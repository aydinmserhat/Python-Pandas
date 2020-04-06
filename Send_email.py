def send_email(user, pwd, recipient, subject, body, cc=None, bcc=None):
    import smtplib

    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body
    
    if cc:
        BCC = ['']
        CC = cc if isinstance(cc, list) else [cc]
        message = """From: %s\nTo: %s\nCc: %s\nBcc: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), ", ".join(CC), ", ".join(BCC), SUBJECT, TEXT) 
    
    elif bcc and cc==None:
        CC = ['']
        BCC = bcc if isinstance(bcc, list) else [bcc]
        message = """From: %s\nTo: %s\nCc: %s\nBcc: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), ", ".join(CC), ", ".join(BCC), SUBJECT, TEXT) 

    elif cc and bcc:
        CC = cc if isinstance(cc, list) else [cc]
        BCC = bcc if isinstance(bcc, list) else [bcc]
        message = """From: %s\nTo: %s\nCc: %s\nBcc: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), ", ".join(CC), ", ".join(BCC), SUBJECT, TEXT)    
    else:
        # Prepare actual message
        CC = ['']
        BCC = ['']
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


#send_email('sender_email', 'sender_password', 'recepient(s)', 'subject', 'body', None, None)
