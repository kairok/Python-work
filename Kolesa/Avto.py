#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import requests
from lxml import html
#import urlparse
#from urllib.parse import urlparse
#import collections
import time
import urllib
from datetime import date

#from urllib.parse import urljoin
from logtrap import loggingBase
from pymongo import MongoClient
import logging.handlers
import logging, logging.config
import urlparse

#logging.config.fileConfig('avto.conf')

#log=logging.getLogger('main')


host="IP"
port="27017"
client =MongoClient(host)
collection = client.big_data.avto

#   KOLESA


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
loggingBase.save_error('auto', 'RUN AVTO')
contractid=''
def avto_start():
    ic = 0
    total = 20
    date_srez = date.today().strftime("%d/%m/%Y")
    try:
        for town in Cities:

                base_url = "https://kolesa.kz/cars/%s/?page=%s" % (town, page)

                try:
                    response = requests.get(base_url, headers = user_agent)
                    if response.status_code==404:
                        #log.exception("exception  No Town!!"+town)
                        continue
                    parsed_body = html.fromstring(response.content)
                    nom_pages=parsed_body.xpath('//*[@class="pager"]/ul/li//text()')
                    try:
                        nom_pages=nom_pages[len(nom_pages)-1].strip()
                        nom_pages=int(nom_pages)+1
                    except:
                        nom_pages =2
                except:
                    #log.exception("exception  URL!!")
                    time.sleep(5)
                    continue
                    exit(-1)

                #base_url = "https://krisha.kz/prodazha/kvartiry/almaty/?das[live.rooms]=1&page=%s"
                ic += 1
                title = ""
                pages = ""
                base_url = "https://kolesa.kz/cars/%s/?page=%s"
                loggingBase.save_error('auto', town)

                for url in [base_url % (town,i) for i in range(1,nom_pages)]:
                #while len(urls_queue):
                    #url = urls_queue.popleft()
                    try:
                        time.sleep(0.2)
                        response = requests.get(url, headers = user_agent)
                        parsed_body = html.fromstring(response.content)

                    # Печатает заголовок страницы

                        print (parsed_body.xpath('//title/text()')[0])
                        title = parsed_body.xpath('//title/text()')[0]
                        pages = title[title.find(u'страница'):]
                        loggingBase.save_error('auto', title)
                       # logging.info(parsed_body.xpath('//title/text()')[0])
                    except:
                        #log.exception("exception message")
                        time.sleep(5)
                        continue

                    #continue
                    # Ищем все обьявления

                    links = [urlparse.urljoin(response.url, url) for url in parsed_body.xpath('.//*[@class="list-title"]/a/@href')]
                    #links=parsed_body.xpath('//div[@class="a-content clearfix"]')

                    for link in links:
                        try:
                            response = requests.get(link, headers=user_agent)
                            time.sleep(0.2)
                            parsed_body = html.fromstring(response.content)

                            brand = ""
                            name = ""
                            year = ""
                            price = ""
                            kuzov = ""
                            city = ""
                            volume = ""
                            contractid = ""
                            distance=''
                            transmition=''
                            helm=''
                            customs=''
                            description =''
                            phone=''
                            date_applay=''
                            zalog = 0
                            #found_urls.add(link)
                            contractid=link         #link.xpath('.//a[@class="link"]/@href')[0]
                            link=parsed_body
                            try:
                                brand=link.xpath('.//span[@itemprop="brand"]/text()')[0].strip()
                                loggingBase.save_error('auto', brand)
                            except:
                                print "Not brand"
                                loggingBase.save_error('error', "Not brand")
                                time.sleep(5)
                                continue

                            try:
                                name=link.xpath('.//span[@itemprop="name"]/text()')[0].strip()
                            except:
                                pass
                            #try:
                            year = link.xpath('.//span[@class="year"]/text()')[0].strip()

                            try:
                                price=link.xpath('.//*[@class="a-price"]//span/text()')[0].strip()
                                price =price.replace('~', '').strip()
                                price="".join(filter(lambda x: ord(x) < 128, price))
                                price = int(float(price))
                            except:
                                loggingBase.save_error('error', "Not brand")
                                print "Not price!"
                                time.sleep(1)
                                continue

                            #   Adress  volume and etc
                            t=link.xpath('.//*[@class="description-body"]//dt/text()')
                            i=0
                            zakaz=0
                            for item in t:
                                if u'Наличие' in item:
                                    zakaz=1
                                    break

                                if u'Город' in item:
                                    city = link.xpath('.//*[@class="description-body"]//dd/text()')[i].strip()
                                    if u'Не на ходу' in city:
                                        zakaz = 1
                                        break
                                    if u'Казахстан' in city:
                                        city = geo[town]
                                if u'Кузов' in item:
                                    kuzov = link.xpath('.//*[@class="description-body"]//dd/text()')[i].strip()
                                if u'Объем двигателя, л' in item:
                                    volume = link.xpath('.//*[@class="description-body"]//dd/text()')[i].strip()
                                if u'Пробег' in item:
                                    distance = link.xpath('.//*[@class="description-body"]//dd/text()')[i].strip()
                                    distance = "".join(filter(lambda x: ord(x) < 128, distance)).replace(' ','')
                                if u'Коробка передач' in item:
                                    transmition = link.xpath('.//*[@class="description-body"]//dd/text()')[i].strip()
                                if u'Руль' in item:
                                    helm = link.xpath('.//*[@class="description-body"]//dd/text()')[i].strip()
                                if u'Растаможен' in item:
                                    customs = link.xpath('.//*[@class="description-body"]//dd/text()')[i].strip()

                                i+=1

                            if zakaz==1:
                                continue
                            # description
                            description = ''.join(link.xpath('.//*[@class="a-params"]//span/text()'))

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

                            room = {'entity':'auto','date_srez':date_srez,'phone':phone,'zalog':zalog,'description':description,
                                    'contractid': contractid,'date_applay': date_applay, 'city': city, 'helm': helm,
                                    'transmition': transmition, 'price': price, 'distance': distance, 'volume': volume,
                                    'year': year,'kuzov': kuzov,'name': name ,'brand': brand,'customs':customs}

                            collection.remove({"contractid": contractid,"date_srez":date_srez})
                            collection.save(room)
                            message = "" + city + " Page " + pages + "  " + parsed_body.xpath('//title/text()')[0]

                        except:
                            #log.exception("exception message")
                            print  sys.exc_info()[1].message + ' line err ' + str(
                                sys.exc_info()[2].tb_lineno)
                            message = 'auto '+sys.exc_info()[1].message + ' line err ' + str(
                                sys.exc_info()[2].tb_lineno)+'  '+contractid

                            loggingBase.save_error('error', message)
                            time.sleep(5)
                            continue

                #  page
            #  City
    except:
        print  sys.exc_info()[1].message + ' line err ' + str(
            sys.exc_info()[2].tb_lineno)
        message = 'Avto '+sys.exc_info()[1].message + ' line err ' + str(
            sys.exc_info()[2].tb_lineno)+'  '+contractid

        loggingBase.save_error('error', message)
        #log.exception("exception message")
        #logging.info("Finita ERROR!!!")
        #exit(-1)

print ("Finita")
loggingBase.save_error('auto', 'DONE')
#logging.info("Finita!!!")

