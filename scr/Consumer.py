import re

import pika
from Writer import (
    createdb,
    insertdata
)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

queue_name = 'logs'
channel.queue_declare(queue=queue_name)


def parser(message):
    pattern = re.compile("^\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2}\s(\w+-)+\w+\s\w.+\[\d+\]:")

    month = ""
    day = ""
    time = ""
    user = ""
    device = ""
    process = ""
    description = ""

    if pattern.match(message):
        month = re.search(r'(^\w{3})', message).group()
        day = re.search(r'(\d{1,2})', message).group()
        time = re.search(r'(\d{2}:\d{2}:\d{2})', message).group()
        line = re.search(r'(\w+-)', message).group()
        user = line[:-1]
        line = re.search(r'(-\w+)+', message).group()
        device = line[1:]
        line = re.search(r'(\w+\[\d+\]:\s)', message)
        pos = line.end()
        line = re.search(r'(\w+\[\d+\]:\s)', message).group()
        process = line[:-2]
        description = message[pos:]

    return month, day, time, user, device, process, description


def callback(ch, method, properties, body):
    message = body.__str__()[2:-1]
    print(message)
    month, day, time, user, device, process, description = parser(message)
    createdb()
    if not month:
        print("Неверные данные")
    else:
        insertdata(month, day, time, user, device, process, description)


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
