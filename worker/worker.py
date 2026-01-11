import os
import sys

import pika


def main():
    print("***starting the worker***")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="host.docker.internal")
    )
    channel = connection.channel()

    channel.queue_declare(queue="incoming_image")

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

    channel.basic_consume(
        queue="incoming_image", on_message_callback=callback, auto_ack=False
    )

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
