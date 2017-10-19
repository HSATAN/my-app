# -*- coding: utf8 -*-


import pika

conn = pika.BlockingConnection(pika.ConnectionParameters(
    credentials=pika.PlainCredentials("guest","guest"),
    host="47.93.5.189"))

channel = conn.channel()
channel.exchange_declare(exchange="logs",

                         exchange_type="fanout")
channel.queue_declare(queue="log1", durable=True)
channel.queue_declare(queue="log2", durable=True)

channel.queue_bind(queue="log1",
                   routing_key="log",
                   exchange="logs")
channel.queue_bind(queue="log2",
                   routing_key="huangkaijie",
                   exchange="logs")


channel.exchange_declare(exchange="topic",
                         exchange_type="topic")

channel.queue_declare(queue="topic_huang",
                      durable=True)
channel.queue_declare(queue="topic_xiong",
                      durable=True)

channel.queue_bind(queue="topic_huang",
                   routing_key="*.huang",
                   exchange="topic")
channel.queue_bind(queue="topic_xiong",
                   routing_key="*.huang",
                   exchange="topic")
channel.basic_publish(exchange="",
                      routing_key="topic.huang",
                      body="这是topic——黄",
                      properties=pika.BasicProperties(delivery_mode=2))

print(" sent message : hello world")

conn.close()