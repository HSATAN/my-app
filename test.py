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

class Getter():
    def getdata(self, x):
        d = defer.Deferred()
        reactor.callLater(1, d.callback, 5)
        return d

    def printdata(self, d):
        print d

print '------------------'

# g= Getter()
# d = g.getdata(2)
# d.addCallback(g.printdata)
# reactor.callLater(2, reactor.stop)
# dbpool.runInteraction("select * from mzhan_user limit 10").addCallback(printData)

import eventlet

def eventFunc(*args):
    print 'start eventFunc ---- %s ' % args[0]
    # if args[0] == "huangkaijie":
    #     eventlet.sleep(2)
    print args
    print 'end eventFunc ----'
    return "----------------------"
pool = eventlet.GreenPool()
res = pool.spawn(eventFunc, "huangkaijie")
print pool.running()
print pool.free()
print 'running here '
res2 = pool.spawn(eventFunc, "second")
def test(gt, name):
    print name
res.link(test,"----huangkaijie---------")
print pool.running()
print pool.free()
print res.wait()

third = eventlet.spawn_after(2, eventFunc, "third_n")
third.wait()

# reactor.run()
from eventlet.green import urllib2

urls = ['http://eventlet.net/',
        'http://us.i1.yimg.com/us.yimg.com/i/ww/beta/y3.gif',
        'https://www.baidu.com/s?tn=baidu&rsv_idx=1&wd=python%20eventlet&rsv_crq=6&bs=python%20eventlet']

def fetch(url):
    return urllib2.urlopen(url).read()

for body in pool.imap(fetch,urls):
    print len(body)