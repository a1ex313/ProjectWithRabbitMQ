import pika

# Подключение к RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Consumer
queue_name = 'logs'
channel.queue_declare(queue=queue_name)

# Отправка сообщений
with open("all-logs.log", "r") as file:
    while True:
        message = file.readline().rstrip('\n')
        if not message:
            break
        channel.basic_publish(exchange='', routing_key='logs', body=message)
        print(f" [x] Sent {message}")
