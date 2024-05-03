import pika


class RabbitMQSender:
    def __init__(self, exchange_name: str, exchange_type: str, host='localhost', port=5672, username='myuser', password='mypassword'):
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
        self.exchange_name = exchange_name
        self.exchange_type = exchange_type
        self.exchange = None

    def setup(self):
        self._connect()
        self.channel.exchange_declare(
            exchange=self.exchange_name,
            exchange_type=self.exchange_type,
            durable=True
        )

    def _connect(self):
        self.connection = pika.BlockingConnection(
            self.connection_params)
        self.channel = self.connection.channel()

    def declare_queue(self, queue_name: str, auto_delete=False, durable=True):
        self.channel.queue_declare(queue=queue_name, durable=durable, auto_delete=auto_delete)

    def send_message(self, message: str, routing_key: str = "", exchange: str = "", properties: pika.BasicProperties = None):
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=message,
            properties=properties,
        )
        print(f"Sent: {message}")

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Connection closed")


# if __name__ == "__main__":
#     properties = pika.BasicProperties(expiration='10000')
#     sender = RabbitMQSender()
#     sender.declare_queue("non_durable_auto_deletable_queue")
#     for message in range(10):
#         sender.send_message(routing_key="non_durable_auto_deletable_queue", message=f'{message} Hello RabbitMQ!', properties=properties)
#     sender.close_connection()
