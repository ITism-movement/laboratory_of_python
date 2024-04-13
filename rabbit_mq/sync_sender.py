import pika


class RabbitMQSender:
    def __init__(self, host='localhost', port=5672, username='myuser', password='mypassword'):
        self.host = host
        self.port = port
        self.credentials = pika.PlainCredentials(username, password)
        self.connection_params = pika.ConnectionParameters(
            host=host,
            port=port,
            credentials=self.credentials
        )
        self.connection = None
        self.channel = None
        self._connect()

    def _connect(self):
        self.connection = pika.BlockingConnection(
            self.connection_params)
        self.channel = self.connection.channel()

    def declare_queue(self, queue_name: str):
        self.channel.queue_declare(queue=queue_name, durable=True)

    def send_message(self, message: str, routing_key: str, exchange: str = ""):
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=message
        )
        print(f"Sent: {message}")

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Connection closed")


if __name__ == "__main__":
    sender = RabbitMQSender()
    sender.declare_queue("emails")
    for message in range(1_000_000_000):
        sender.send_message(routing_key="emails", message=f'{message} Hello RabbitMQ!')
    sender.close_connection()
