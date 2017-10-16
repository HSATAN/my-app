# -*- coding: utf8 -*-


import pika
conn = pika.BlockingConnection(pika.ConnectionParameters(host="47.93.5.189"))

channel = conn.channel()
channel.queue_declare(queue="hello", durable=True)

def callback(ch, method, property, body):
    print(" [X] received %r " %body)
    import time
    time.sleep(2)
    print("ok")
    #ch.basic_ack(delivery_tag=method.delevery_tag)

channel.basic_consume(callback,
                      queue="hello",
                      no_ack=False)

print(" waiting for message ...  press CTRL+C to exit")
channel.start_consuming()