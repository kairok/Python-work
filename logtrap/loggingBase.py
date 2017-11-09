# -*- coding: utf-8 -*-

from pymongo import MongoClient

from Configbase import DBconf
import datetime

dbConf = DBconf.ConfigClass()

host=dbConf.host
port=dbConf.port
client =MongoClient(host)
log = client.loggin.logavto
logkrisha = client.loggin.logkrisha



def save_error(type,text):
    doc={'date':datetime.datetime.now().strftime("%d-%m-%Y"), 'time':datetime.datetime.now().strftime("%H-%M"),'type':type, 'text':text}
    log.save(doc)


def save_krisha(type,text):
    doc={'date':datetime.datetime.now().strftime("%d-%m-%Y"),'time':datetime.datetime.now().strftime("%H-%M"), 'type':type, 'text':text}
    logkrisha.save(doc)

