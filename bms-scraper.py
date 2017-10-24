from bs4 import BeautifulSoup
import requests
import re
import smtplib
from multiprocessing import Pool
from time import sleep

def bms_bh(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'
    }
    alertedShows = []
    hitCount = 1
    while(True):
        print('request Count::::', hitCount)
        try:
            page = requests.get(url, headers=headers)
            req_status = -1
            while (req_status != 200):
                page = requests.get(url, headers=headers)
                req_status = page.status_code

            mainSoup = BeautifulSoup(page.content)
            all_shows = mainSoup.findAll("div", {"data-online": "Y"})

            for show in all_shows:
                showTimeE = show.findAll("a")
                showDetail = {
                    'theatre': show.parent.parent.get('data-name'),
                    'showTime': showTimeE[0].text,
                    'link': 'https://in.bookmyshow.com' + showTimeE[0].get('href')
                }
                showDetail['showTime'] = str(re.sub('[\\n\\t]', '', showDetail['showTime']))

                if not hasAlerted(alertedShows, showDetail):
                    alertedShows.append(showDetail)
                    sendMailAsync(showDetail)
                    print(showDetail)

            hitCount = hitCount + 1
            sleep(2)
        except Exception as err:
            print('EXCEPTION OCCURED', err)
            hitCount = hitCount + 1
            continue

def hasAlerted(alertedShows, show):
    for alertedShow in alertedShows:
        if alertedShow['showTime'] == show['showTime'] and alertedShow['theatre'] == show['theatre']:
            return True
    return False

def send_email(user, pwd, recipient, subject, body):
    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print('successfully sent the mail to ', recipient)
    except:
        print('sending mail failed')
    return

SENDER_EMAIL = 'youremail@gmail.com'
SENDER_PASS = 'password'
RECIEVERS = ['email1@gmail.com', 'email2@gmail.com']

def sendMailAsync(showDetail):
    msg = "Just Opened for " + showDetail['showTime'] + ' Show in ' + showDetail['theatre'] \
          + ' \n Click below link to book tickets :: \n' + showDetail['link']
    sub = 'BMS Bahubali Alert :: ' + showDetail['theatre'] + ' :: ' + showDetail['showTime']
    pool = Pool(processes=1)
    pool.apply_async(send_email, [SENDER_EMAIL, SENDER_PASS, RECIEVERS, sub, msg])


if __name__ == "__main__":
    url = "https://in.bookmyshow.com/buytickets/baahubali-2-the-conclusion-hyderabad/movie-hyd-ET00038693-MT/20170428"
    bms_bh(url)
