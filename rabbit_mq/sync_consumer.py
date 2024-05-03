import pika


class RabbitMQConsumer:
    def __init__(self,
                 consumer_tag: str,
                 queue_name: str,
                 host='localhost',
                 port=5672,
                 username='myuser',
                 password='mypassword',
                 virtual_host='/',
                 durable=True,
                 auto_delete=False,
                 ):
        self.consumer_tag = consumer_tag
        self.queue_name = queue_name
        # Setup connection parameters with credentials
        credentials = pika.PlainCredentials(username, password)
        self.connection_params = pika.ConnectionParameters(
            host=host,
            port=port,
            virtual_host=virtual_host,
            credentials=credentials
        )
        self.connection = None
        self.channel = None
        self.durable = durable
        self.auto_delete = auto_delete
        self._connect()

    def _connect(self):
        # Connect to the RabbitMQ server
        self.connection = pika.BlockingConnection(self.connection_params)
        self.channel = self.connection.channel()
        # Ensure that the queue exists
        self.channel.queue_declare(
            queue=self.queue_name,
            durable=self.durable,
            auto_delete=self.auto_delete
        )

    def _callback(self, ch, method, properties, body):
        # This method is called whenever a message is received
        message = body.decode('utf-8')
        print(f"Received: {message}")
        # Acknowledge the message
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        # Start consuming messages
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self._callback,
            consumer_tag=self.consumer_tag,
        )
        print("Starting to consume...")
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
            print("Stopped consuming due to keyboard interrupt.")

    def close_connection(self):
        # Close the connection
        if self.connection:
            self.connection.close()
            print("Connection closed")


# Example usage
if __name__ == "__main__":
    consumer = RabbitMQConsumer(
        consumer_tag='my_sms_consumer 2',
        queue_name="1",
        durable=False,
    )
    try:
        consumer.start_consuming()
    finally:
        consumer.close_connection()
