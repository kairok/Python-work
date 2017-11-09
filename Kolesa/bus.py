#!/usr/bin/python
# -*- coding: utf-8 -*-



import requests
from lxml import html
#import urlparse
#from urllib.parse import urlparse
#import collections
import time
import urllib
from datetime import date
import sys

#from urllib.parse import urljoin
from logtrap import loggingBase
from pymongo import MongoClient
import logging.handlers
import logging, logging.config
import urlparse

#logging.config.fileConfig('bus.conf')

#log=logging.getLogger('main')


host="IP"
port="27017"
client =MongoClient(host)
collection = client.big_data.avto

#   KOLESA

'''
STARTING_URL = 'https://krisha.kz/prodazha/kvartiry/almaty/?das[live.rooms]=1'
urls_queue = collections.deque()
urls_queue.append(STARTING_URL)
found_urls = set()
found_urls.add(STARTING_URL)
'''

Apartments=[]
room_count=1
page=1
date_srez=date.today().strftime("%d/%m/%Y")
user_agent = {'User-agent': 'Mozilla/5.0'}
#'almaty','astana',
Cities=['almaty','astana','kokshetau','shhuchinsk','aktobe','taldykorgan','kaskelen','kapchagaj','talgar','atyrau','ust-kamenogorsk',
        'ridder','semej','taraz','uralsk','aksaj','karaganda','balhash','temirtau','shahtinsk','kostanaj','kyzylorda','aktau',
        'pavlodar','ekibastuz','petropavlovsk','shymkent','zhezkazgan','kulsary']
geo={'almaty':u'Алматы','astana':u'Астана','kokshetau':u'Кокшетау','shhuchinsk':u'Щучинск','aktobe':u'Актобе','taldykorgan':u'Талдыкорган','kaskelen':u'Каскелен',
     'kapchagaj': u'Капчагай','atyrau':u'Астана','talgar':u'Талгар','ust-kamenogorsk':u'Усть-каменогорск','ridder':u'Риддер','semej':u'Семей',
     'taraz': u'Тараз','uralsk':u'Уральск','aksaj':u'Аксай','karaganda':u'Караганда','balhash':u'Балхаш','temirtau':u'Темиртау','shahtinsk':u'Шахтинск',
     'kostanaj': u'Костанай', 'kyzylorda': u'Кызылорда', 'aktau': u'Актау', 'pavlodar': u'Павлодар', 'ekibastuz': u'Экибастуз',
     'petropavlovsk': u'Петропавловск', 'shymkent': u'Шымкент', 'zhezkazgan': u'Жезказган', 'kulsary': u'Кульсары'}
ic=0
total=20
loggingBase.save_error('bus', 'RUN')
contractid=''
def bus_start():
    ic = 0
    total = 20
    date_srez = date.today().strftime("%d/%m/%Y")
    try:
        for town in Cities:

                base_url = "https://kolesa.kz/spectehnika/avtobusy/%s/?page=%s" % (town, page)

                try:
                    response = requests.get(base_url, headers = user_agent)
                    if response.status_code==404:
                        continue
                    parsed_body = html.fromstring(response.content)
                    nom_pages=parsed_body.xpath('//*[@class="pager"]/ul/li//text()')
                    try:
                        nom_pages=nom_pages[len(nom_pages)-1].strip()
                        nom_pages=int(nom_pages)+1
                    except:
                        nom_pages =2
                except:
                    #log.exception("exception URL")
                    time.sleep(5)
                    continue
                    exit(-1)

                #base_url = "https://krisha.kz/prodazha/kvartiry/almaty/?das[live.rooms]=1&page=%s"
                ic += 1
                title = ""
                pages = ""
                base_url = "https://kolesa.kz/spectehnika/avtobusy/%s/?page=%s"
                loggingBase.save_error('bus', town)
                for url in [base_url % (town,i) for i in range(1,nom_pages)]:
                #while len(urls_queue):
                    #url = urls_queue.popleft()
                    #time.sleep(3)
                    try:
                        response = requests.get(url, headers = user_agent)
                        #time.sleep(1)
                        parsed_body = html.fromstring(response.content)

                    # Печатает заголовок страницы

                        print (parsed_body.xpath('//title/text()')[0])
                        title = parsed_body.xpath('//title/text()')[0]
                        pages = title[title.find(u'страница'):]
                        #logging.info(parsed_body.xpath('//title/text()')[0])
                        loggingBase.save_error('bus', title)
                    except:
                        #log.exception("exception message")
                        continue

                    #continue
                    # Ищем все обьявления

                    links = [urlparse.urljoin(response.url, url) for url in parsed_body.xpath('.//*[@class="list-title"]/a/@href')]
                    #links=parsed_body.xpath('//div[@class="a-content clearfix"]')

                    for link in links:
                        try:
                            response = requests.get(link, headers=user_agent)
                            time.sleep(0.3)
                            parsed_body = html.fromstring(response.content)

                            brand = ""
                            name = ""
                            year = ""
                            price = ""
                            kuzov = ""
                            city = ""
                            fuel = ""
                            contractid = ""
                            distance=''
                            transmition=''
                            count_place=''
                            helm=''
                            volume = ""
                            customs=''
                            description =''
                            phone=''
                            date_applay=''
                            zalog = 0
                            #found_urls.add(link)
                            contractid=link         #link.xpath('.//a[@class="link"]/@href')[0]
                            link=parsed_body
                            try:
                                t=link.xpath('.//*[@class="a-title__text"]/text()')[0].strip()
                                print t
                                loggingBase.save_error('bus', t)
                            except:
                                print "Not Text!"
                                continue
                            s=t.split('  ')
                            #try:
                            brand=s[0].strip()
                            #except:
                            #    pass
                            if len(s)>2:
                                name=s[1].strip()
                                year=s[2].strip()
                            else:
                                year = s[1].strip()

                            try:
                                price=link.xpath('.//*[@class="a-price"]//span/text()')[0].strip()
                                price =price.replace('~', '').strip()
                                price="".join(filter(lambda x: ord(x) < 128, price))
                                price = int(float(price))
                            except:
                                print "Not price!"
                                continue

                            #   Adress  volume and etc
                            t=link.xpath('.//*[@class="description-body"]//dt/text()')
                            k=link.xpath('.//*[@class="description-body"]//dd/text()')
                            if len(t)<len(k):
                                i=1
                            else:
                                i=0
                            zakaz=0
                            for item in t:
                                if u'Наличие' in item:
                                    zakaz=1
                                    break

                                if u'Город' in item:
                                    city = link.xpath('.//*[@class="description-body"]//dd/text()')[i].strip()
                                    if u'Казахстан' in city:
                                        city = geo[town]
                                if u'Тип автобуса' in item:
                                    kuzov = link.xpath('.//*[@class="description-body"]//dd/text()')[i].strip()
                                if u'Тип топлива' in item:
                                    try:
                                        fuel = link.xpath('.//*[@class="description-body"]//dd/text()')[i].strip()
                                    except:
                                        pass
                                if u'Объем двигателя, л' in item:
                                    try:
                                        volume = link.xpath('.//*[@class="description-body"]//dd/text()')[i].strip()
                                    except:
                                        pass
                                if u'КПП' in item:
                                    try:
                                        transmition = link.xpath('.//*[@class="description-body"]//dd/text()')[i].strip()
                                    except:
                                        pass
                                if u'Количество мест' in item:
                                    try:
                                        count_place = link.xpath('.//*[@class="description-body"]//dd/text()')[i].strip()
                                    except:
                                        pass
                                i+=1

                            if zakaz==1:
                                continue
                            # description
                            description = ''.join(link.xpath('.//*[@class="description-text"]/text()'))

                            #    Zalog  ?


                            #  Phone
                            try:
                                t=link.xpath('.//*[@class="action-link showPhonesLink"]/@data-href')[0]
                                url_phone=urlparse.urljoin(response.url, t)
                                response = requests.get(url_phone,
                                                    headers={'X-Requested-With': 'XMLHttpRequest'})
                                phone = response.json()['data']['model']['phone'].strip()
                            except:
                                pass


                            #  Date
                            t = link.xpath('.//*[@class="row"]/div/text()')
                            for it in t:
                                if u'Опубликовано' in it:
                                    date_applay=it.replace(u'Опубликовано','').strip()

                            room = {'entity':'bus','date_srez':date_srez,'phone':phone,'zalog':zalog,'description':description,
                                    'contractid': contractid,'date_applay': date_applay, 'city': city, 'helm': helm,
                                    'transmition': transmition, 'price': price, 'volume': volume, 'fuel': fuel,'count_place': count_place,
                                    'year': year,'kuzov': kuzov,'name': name ,'brand': brand,'customs':customs}

                            collection.remove({"contractid": contractid,"date_srez":date_srez})
                            collection.save(room)
                            message = "" + city + " Page " + pages + "  " + parsed_body.xpath('//title/text()')[0]

                        except:
                            #log.exception("exception message")
                            print  sys.exc_info()[1].message + ' line err ' + str(
                                sys.exc_info()[2].tb_lineno)
                            message = 'bus '+sys.exc_info()[1].message + ' line err ' + str(
                                sys.exc_info()[2].tb_lineno)+'  '+contractid

                            loggingBase.save_error('error', message)
                            time.sleep(5)
                            continue

                #  page
            #  City
    except:
        print  sys.exc_info()[1].message + ' line err ' + str(
            sys.exc_info()[2].tb_lineno)
        message ='BUS '+ sys.exc_info()[1].message + ' line err ' + str(
            sys.exc_info()[2].tb_lineno)

        loggingBase.save_error('error', message)
        #log.exception("exception message")
        #logging.info(contractid)
        #exit(-1)

loggingBase.save_error('bus', 'Done')
#print ("Finita")
#logging.info("Finita!!!")

'''
for room in Apartments:
    for k, v in room.items():
         print(k, v)

    print('------------------------')
'''

'''
import csv

#my_dict = {"test": 1, "testing": 2}

with open('mycsvfile.csv', 'w') as f:  # Just use 'w' mode in 3.x
    for room in Apartments:
        #for k, v in room.items():
            w = csv.DictWriter(f, room.keys())
            #w.writeheader()
            w.writerow(room)
'''

