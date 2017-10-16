# coding = utf8

import pika

conn = pika.BlockingConnection(pika.ConnectionParameters(host="47.93.5.189"))

channel = conn.channel()

channel.queue_declare(queue="hello", durable=True)

channel.basic_publish(exchange="",
                      routing_key="hello",
                      body="hello world",
                      properties=pika.BasicProperties(delivery_mode=2))

print(" sent message : hello world")

conn.close()