from flask import Flask, jsonify

from rabbit_mq.sync_sender import RabbitMQSender
import random


class ScooterDBClient:
    def __init__(self, url):
        self.url = url

    def fetch_data(self):
        # Example method to simulate fetching data
        return [x for x in range(0, 20)]


class MyApp(Flask):
    def __init__(
            self,
            scooter_db: ScooterDBClient,
            rmq_sender: RabbitMQSender,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.scooter_db = scooter_db
        self.rmq_sender = rmq_sender
        self.has_been_set_up = False

    def setup(self):
        self.rmq_sender.setup()
        self.has_been_set_up = True


# Initialize MyClient with a specific URL
client = ScooterDBClient("https://api.example.com")
rmq_sender = RabbitMQSender(
    exchange_name="releases",
    exchange_type="fanout",
)
app = MyApp(client, rmq_sender, __name__)
app.setup()


RELEASE_NOTE = "My shiny release for %d"


@app.route('/send_release')
def send_release():
    # Use the global client instance
    serial_numbers = app.scooter_db.fetch_data()
    # for serial_number in serial_numbers:
        # app.rmq_sender.declare_queue(
        #     queue_name=str(serial_number),
        #     durable=False,
        # )
        # app.rmq_sender.channel.queue_bind(
        #     queue=str(serial_number),
        #     exchange=app.rmq_sender.exchange_name,
        #     routing_key=str(serial_number)
        # )
    app.rmq_sender.send_message(
        message=RELEASE_NOTE % 123123123,
        # routing_key=str(serial_number),
    )
    return jsonify({"result": serial_numbers})


if __name__ == '__main__':
    app.run(debug=True)
