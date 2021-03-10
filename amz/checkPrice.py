from .models import users
import smtplib,ssl
import datetime
import time
import random
from bs4 import BeautifulSoup
from email.message import EmailMessage
import requests

headers_list = [
    # Firefox 77 Mac
     {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    },
    # Firefox 77 Windows
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    },
    # Chrome 83 Mac
    {
        
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://www.google.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
    },
    # Chrome 83 Windows 
    {
        
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://www.google.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9"
    }
]

def send_mail(email,link,price,creation_price):
    port = 465
    user_name = "vvilas122@gmail.com"
    password = "Mybrother@10"
    message = EmailMessage()
    message['From'] = user_name
    message['To'] = email
    message['Subject'] = "Your Product Price Changed"
    user_message = f"""
    Your item Current Price is {price} 
    previous price was {creation_price} 
    hurry up grab your stuff from the link
     {link}"""
    message.set_content(user_message)

    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL('smtp.gmail.com',port,context=context)
    server.login(user_name,password)
    server.send_message(message)
    print("Email sent")
    server.quit()



def checkDays():
    userss = users.objects.all()
    for i in userss:
        c_date = datetime.datetime.now().date()
        creation_date_full = i.creation_date
        creation_year = int(creation_date_full[0:4])
        creation_month = int(creation_date_full[5:7])
        creation_date = int(creation_date_full[8:])
        creation_date_date = datetime.date(creation_year,creation_month,creation_date)
        no_of_days = c_date - creation_date_date
        if(no_of_days.day >= 7):
            Users.objects.filter(id=i.id).delete()
        


def check():
    checkDays()
    usersss = users.objects.all()
    if(len(usersss) == 0):
        pass
    else:
        for i in usersss:
            id = i.id
            url = i.item
            creation_price = i.creation_price
            trigger_price = i.trigger_price
            creation_date = i.creation_date
            email = i.email
            HEADER = random.choice(headers_list)
            site = requests.get(url,headers=HEADER)
            soup = BeautifulSoup(site.content,'lxml')
            price_raw = soup.find(id="priceblock_ourprice")
            price = price_raw.string
            check_price = price[1:].strip().replace(",","")
            final_check_price = int(float(check_price))

            if(final_check_price == trigger_price or final_check_price<creation_price):
                send_mail(email,url,price,creation_price)
                users.objects.filter(id=id).delete()

            print(f"link:{url},creation_price:{creation_price},creation_date:{creation_date},trigger_price:{trigger_price},email:{email}")
            time.sleep(100)





