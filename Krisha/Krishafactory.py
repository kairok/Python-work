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
import urlparse
#from urllib.parse import urljoin

from pymongo import MongoClient
import logging.handlers
import logging, logging.config
import sys
from logtrap import loggingBase

#logging.config.fileConfig('factory.conf')

log=logging.getLogger('main')


host="IP"
port="27017"
client =MongoClient(host)
collection = client.big_data.real_estate



Apartments=[]
room_count=''
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


loggingBase.save_krisha('factory', 'RUN factory')
contractid=''
def factory():
    date_srez = date.today().strftime("%d/%m/%Y")
    try:
        for town in Cities:

                #base_url = "https://krisha.kz/prodazha/kvartiry/%s/?das[live.rooms]=%s&page=%s" % (town,room_count,page)
                base_url = "https://krisha.kz/prodazha/prombazy/%s/?page=%s" % (town, page)

                try:
                    response = requests.get(base_url, headers = user_agent)
                    parsed_body = html.fromstring(response.content)
                    nom_pages=parsed_body.xpath('//a[@class="btn paginator-page-btn"]/text()')
                    try:
                        nom_pages=nom_pages[len(nom_pages)-1].strip()
                        nom_pages=int(nom_pages)+1
                    except:
                        nom_pages =2
                except:
                    log.exception("exception message")
                    exit(-1)

                #base_url = "https://krisha.kz/prodazha/kvartiry/almaty/?das[live.rooms]=1&page=%s"
                base_url = "https://krisha.kz/prodazha/prombazy/%s/?page=%s"
                for url in [base_url % (town,i) for i in range(1,nom_pages)]:
                #while len(urls_queue):
                    #url = urls_queue.popleft()
                    time.sleep(2)
                    response = requests.get(url, headers = user_agent)
                    parsed_body = html.fromstring(response.content)

                    # Печатает заголовок страницы
                    try:
                        print (parsed_body.xpath('//title/text()')[0])
                        logging.info(parsed_body.xpath('//title/text()')[0])
                        loggingBase.save_krisha('factory', parsed_body.xpath('//title/text()')[0])
                    except:
                         log.exception("exception message")
                         time.sleep(7)
                         continue

                    #continue
                    # Ищем все обьявления
                    links = [urlparse.urljoin(response.url, url) for url in
                         parsed_body.xpath('.//*[@class="a-title"]/a/@href')]
                    #links=parsed_body.xpath('//div[@class="a-content clearfix"]')

                    for link in links:
                        time.sleep(1)
                        response = requests.get(link, headers=user_agent)
                        parsed_body = html.fromstring(response.content)

                        region = ""
                        type = ""
                        year = ""
                        price = ""
                        square = ""
                        city = ""
                        number = ""
                        contractid = ""
                        description = ""
                        buildings = 0
                        whois = ''
                        date_applay = ''
                        phone = ''
                        zalog = 0
                        square2 =''

                        contractid = link
                        link = parsed_body
                        price = link.xpath('.//*[@class="price"]/text()')[0].strip()
                        price = price.replace('~', '').strip()
                        price = "".join(filter(lambda x: ord(x) < 128, price))
                        price = int(float(price))

                        #   Adress  Square
                        t = link.xpath('.//*[@class="a-where-region"]/text()')
                        s = t[0].split(',')
                        city = s[0].strip()
                        if u'Казахстан' in city:
                            city = geo[town]

                        try:
                            if s[1].find(u'р-н') < 0:
                                t2 = link.xpath('.//*/h1/text()')[0]
                                s2 = t2.split(',')
                                region = s2[1].strip()
                            else:
                                region = s[1].strip()
                        except:
                            ok = 1
                            item = link.xpath('.//*/h1/text()')[0]
                            s = item.split(',')
                            try:
                                region = s[1].strip()
                            except:
                                continue

                        t = link.xpath('.//*[@class="a-parameters"]//text()')
                        for i in range(1, len(t)):
                            if u'Площадь участка, соток' in t[i]:
                                # Square
                                square = t[i + 2].strip()+u' :Площадь участка, соток'
                            if u'Площадь производственных помещений, кв.м' in t[i]:
                                # Square
                                square2=t[i + 2].strip()+u' :Площадь производственных помещений, кв.м'
                        #   Type
                        t=link.xpath('.//*/h1/text()')[0]
                        s = t.split(',')
                        type=s[0]

                        #    Zalog  ?
                        try:
                            t=link.xpath('.//*[@class="a-is-mortgaged"]/text()')[0]
                            zalog=1
                        except:
                            pass

                        t = ''.join(link.xpath('.//*[@class="text"]/div/text()'))
                        description = t
                        #  Phone
                        try:
                            t = link.xpath('.//*[@class="show-phones"]/@data-url')[0]
                            url_phone = urlparse.urljoin(response.url, t)
                            response = requests.get(url_phone,
                                                    headers={'X-Requested-With': 'XMLHttpRequest'})
                            phone = ', '.join(response.json()).strip()
                        except:
                            pass

                        try:
                            whois = ''.join(link.xpath('.//*[@class="user-info"]//text()')).replace('\n',
                                                                                                    '').strip()
                        except:
                            whois = u'Хозяин'
                        if whois == '':
                            whois = u'Хозяин'

                            # Data
                        t = link.xpath('.//*[@class="row"]/div/text()')
                        for it in t:
                            if u'с' in it:
                                date_applay = it.replace(u'с', '').strip()

                        room = {'entity':'factory','date_srez':date_srez,'zalog':zalog,'description':description,'contractid': contractid,
                                'date_applay': date_applay, 'city': city, 'region': region, 'square': square,'square2': square2, 'price': price,
                                'type': type, 'number': number, 'year': year,'rooms': room_count,'whois': whois }
                        #Apartments.append(room)
                        #  MongoDB   write
                        #  Find  contractid
                        collection.remove({"contractid": contractid,"date_srez":date_srez})
                        collection.save(room)

                #  page
            #  City
    except:
        log.exception("exception message")
        message = 'factory '+sys.exc_info()[1].message + ' line err ' + str(
            sys.exc_info()[2].tb_lineno)+' '+contractid

        loggingBase.save_krisha('error', message)
        exit(-1)

print ("Finita")
logging.info("Finita!!!")
loggingBase.save_krisha('factory', 'Done')


