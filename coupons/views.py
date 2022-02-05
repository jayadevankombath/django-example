import re
import requests

from bs4 import BeautifulSoup
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render

from .models import Coupon

def approved_coupons(request):
    """ 
    Return Approved coupons
    """

    if request.method == 'GET':
        coupnObjs = Coupon.objects.filter(status = "APPROVED")
        return render(request,"coupons/index.html",{'coupons':coupnObjs}, status=200)
    else:
        return HttpResponse('HTTP_405_METHOD_NOT_ALLOWED', content_type="text/plain", status=405)
    

def scrap_coupons(request):
    """ Scrap Coupons from https://www.rezeem.com/azadea-coupons
    """
    
    url = "https://www.rezeem.com/azadea-coupons"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    elements = soup.findAll('div', attrs={'class':'ocode'})

    couponsObjs = []

    for element in elements:

        cptype = element.find('span', attrs={'class':'cp-type cp-type-code'})

        if cptype and cptype.text == 'Code':
            button_element = element.find('button', attrs={'class':'cp-code-btn'})

            if button_element:
                coupon_code  = button_element.find('span')

                if coupon_code:

                    coupon_code = coupon_code.text
                    expire_date = element.find(lambda tag:tag.name=="span" and "Expires" in tag.text)
                    offertext = element.find('span', attrs={'class':'title'})
                    desciption = element.find('h3', attrs={'class':'subtitle','data-cptype':'cp'})

                    if expire_date:
                        expire_date_element = expire_date.text.split("Expires")
                        exp_date = expire_date_element[1]
                        date = datetime.strptime(str(exp_date), '%d %b %Y')
                        
                    else:
                        date = None

                    if offertext:
                        text = offertext.text
                        offervalue = re.findall(r"[-+]?(?:\d*\.\d+|\d+)",text)
                        
                        if offervalue:
                            offer = offervalue[0]
                            offer = float(offer)
                            type = 'Percentage'
                        else:
                            offer = None
                            type = 'Flat'

                    if desciption:
                        desc = desciption.text
                    else:
                        desc = None

                    couponsObjs.append({
                        'coupon_code':coupon_code,
                        'expiry_date':date,
                        'type':type,
                        'offer_value':offer,
                        'coupon_description':desc,
                        'status':'Pending'})
                
                continue
            continue
        continue
    return insert_scrp_coupons(request, couponsObjs)

def insert_scrp_coupons(request, coupons_data):
    """ 
    Inserting scraped coupons
    """

    for coupon in coupons_data:
        try:
            cpnObj = Coupon.objects.create(
                coupon_code = coupon['coupon_code'],
                expiry_date = coupon['expiry_date'] if coupon['expiry_date'] != None else None,
                offer_value = coupon['offer_value'] if coupon['offer_value'] else 0,
                coupon_description = coupon['coupon_description'],
                status = Coupon.Status.PENDING)

            if coupon['type'] == 'Flat':
                cpnObj.type = Coupon.Types.FLAT
            else:
                cpnObj.type = Coupon.Types.PERCENTAGE

            cpnObj.save()
        except Exception as e:
            return HttpResponse(e, content_type="text/plain")

    return HttpResponse(
        'New coupons are scraped and inserted into database.', content_type="text/plain", status=201)






