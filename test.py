# coding=utf8

from twisted.internet import reactor, defer
from twisted.enterprise.adbapi import ConnectionPool
import psycopg2
import psycopg2.extras
from eventlet.twistedutil import block_on
import time

dbpool = ConnectionPool("psycopg2",
                        host="47.93.5.189",
                        user="huangkaijie",
                        password="edison",
                        database="mzhan",
                        cursor_factory=psycopg2.extras.DictCursor)

def _getData(txn, user):
    txn.execute("select * from mzhan_tag limit 10")
    result = txn.fetchall()
    if result:
        return result
    return None

def getData(user):
    return (dbpool.runInteraction(_getData, user))

def printData(data):
    if data:
        for index, item in enumerate(data):
            print data[index][1]

getData("huangkaijie").addCallback(printData)

reactor.callLater(5,reactor.stop)
reactor.run()