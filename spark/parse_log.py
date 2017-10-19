# -*- coding: utf8 -*-
from collections import defaultdict
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("log").config("log", "value").getOrCreate()
sc = spark.sparkContext
file = sc.textFile("file:///home/data/haproxy.log-20171010-1")

def split_item(line):

    line = line.replace("- - --", "")
    lines = line.split(" ")
    return line
    item = defaultdict(lambda: "")
    # try:
    #     item['month'] = lines[0]
    # except:pass
    # try:
    #     item['day'] = lines[1]
    # except:pass
    # try:
    #     item['date'] = lines[6]
    # except:pass
    # try:
    #     item['ip'] = lines[5]
    # except:pass
    # try:
    #     item['server'] = lines[8]
    # except:pass
    # try:
    #     item['interface'] = lines[-2].split('?')[0]
    # except:pass
    # try:
    #     item['method'] = lines[-3]
    # except:pass
    # try:
    #     if '/v1.0/callback/ios_click' in item['interface']:
    #         item['download_user'] = lines[-2].split('?')[1].split('&')[0].split('=')[1].split('ios_')[0]
    # except:pass
    return item

rdd = file.map(split_item)

rdd.take(10)