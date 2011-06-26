import smtplib 
import urllib
import xml.dom.minidom

from email.MIMEText import MIMEText

API_KEY = # Your weather.com API key

SEND_EMAIL = # Sender Email
SEND_EMAIl_PW = # Sender Email password
RECV_EMAIL = # Reciever Email
EMAIL_SUBJ = # Subject for the alert emails
LOW_BOUND = # Low bound in degrees C
HIGH_BOUND = # Upper bound in degrees C

SMTP_SERV = # SMTP Server to send the email
SMTP_SERV_PORT = # Port the SMTP server is running on

def sendemail(to, message):
    '''
        Send a message via email
    '''
    msg = MIMEText(message)
    msg['Subject'] = EMAIL_SUBJ
    msg['From'] = SEND_EMAIL
    msg['To'] = to

    # Set up to send from gmail addresses
    s = smtplib.SMTP(SMTP_SERV, SMTP_SERV_PORT)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(SEND_EMAIL, SEND_EMAIL_PW)
    s.sendmail(SEND_EMAIL, to, msg.as_string())

    return

def main():
    '''
        Driver of the program.  Makes a call to the weather.com API,
        and if the high temperature for the day is outside the bounds
        set at the top, it sends an email alert
    '''
    params = urllib.urlencode({
        'dayf': 1, 
        'link': 'xoap', 
        'par': '1193606313', 
        'prod': 'xoap', 
        'key': API_KEY, 
        'unit': 'm'})

    f = urllib.urlopen(
        'http://xoap.weather.com/weather/local/10006?%s' % params)
    result = f.read()

    dom = xml.dom.minidom.parseString(result)
    daysnode = dom.getElementsByTagName('dayf')[0]
    todaynode = daysnode.getElementsByTagName('day')[0]
    high = todaynode.getElementsByTagName('hi')[0].childNodes[0].data

    try:
        deg = int(high)
        if (deg >= HIGH_BOUND):
            sendemail(RECV_EMAIL, 'High of %d today\n' % deg)
        elif (deg <= LOW_BOUND):
            sendemail(RECV_EMAIL, 'Low of %d today\n' % deg)
    except ValueError:
        msg = ''

if __name__ == "__main__":
    main()
