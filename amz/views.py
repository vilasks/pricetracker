from django.shortcuts import render
from django.http import HttpResponse
import requests
import datetime
import random
from bs4 import BeautifulSoup
from .models import users
import threading
import amz.checkPrice as pricecheck
# Create your views here.
headers_list = [{
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
    }]

def home(request):
    
    return  render(request,'home.html',{})

def productPage(request):


    if (request.method == "POST"):
        url = request.POST['item']
        HEADER = random.choice(headers_list)
        page = requests.get(url, headers=HEADER)
        soup = BeautifulSoup(page.content, 'html.parser')
        title = soup.title.string
        image = soup.find(id="landingImage")
        image_url = image['src']
        price1 = soup.find(id="priceblock_ourprice")
        price = price1.string
        '''url = "www.google.com"
            title = "Fake title"
            price = 555
            image_url = "https://image.shutterstock.com/image-photo/large-beautiful-drops-transparent-rain-600w-668593321.jpg"'''
        return render(request, 'productpage.html',{'item': url, 'itemtitle': title, 'price': price[1:], 'imageurl': image_url})
    else:
        return HttpResponse("Something Went Wrong")

def submit_email(request):

    if(request.method == "POST"):
        url = request.POST['url']
        total_user = users.objects.all()

        if(len(total_user) >= 100):
            return HttpResponse("Users Limit Reached")

        Email = request.POST['email']
        if(len(total_user) == 0):
            pass
        else:
            email_exists = users.objects.filter(email=Email)
            if(email_exists.exists()):
                return HttpResponse("Email Exists In our Please use another Email")

        

        creation_price_raw = request.POST['creation_price']
        strip_creation_price = creation_price_raw[1:]
        creation_price_int = strip_creation_price.strip().replace(",","")
        creation_price = int(float(creation_price_int))
        creation_date = datetime.datetime.now().date()

        if (not request.POST['target_price']):
            trigger_price = int(creation_price)
        else:
            trigger_price = int(request.POST['target_price'])

        user = users(email=Email,
                    item=url,
                    creation_date=creation_date,
                    creation_price=creation_price,
                    trigger_price=trigger_price)
        
        user.save()
        return render(request,'email_success.html',{})
    else:
        return HttpResponse("Your not supposed to Visit Directly")



#threading._start_new_thread(pricecheck.check())
