import pika
import cv2
import json
import time


def open_amqp_conn():        
    print('OPENING: AMQP connection')
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('MaragiRabbit', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    print('ESTABLISHED: AMQP connection')
    return channel


def publish_video_loop(amqp):
    cam = cv2.VideoCapture(0)
    print('STARTING: video publish loop')
    while True:
        s, img = cam.read()
        img = str(json.dumps(img.tolist(), separators=(',', ':')))
        channel.basic_publish(exchange='sensor_video', body=img, routing_key='')
        time.sleep(0.25)


if __name__ == '__main__':
    while True:
        try:
            amqp = open_amqp_conn()
            publish_video_loop(amqp)
        except Exception as oops:
            print('ERROR:', oops)
