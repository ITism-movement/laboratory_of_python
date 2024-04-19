from rabbit_mq.sync_sender import RabbitMQSender

SCOOTER_IDS = ["1A", "2B", "3C"]


def read_release():
    with open("release.txt", "r") as release_file:
        release_data = release_file.read()
    return release_data


if __name__ == "__main__":
    sender = RabbitMQSender()
    for queue_name in SCOOTER_IDS:
        sender.declare_queue(queue_name=queue_name, auto_delete=True)

    release_data = read_release()

    for queue_name in SCOOTER_IDS:
        sender.send_message(routing_key=queue_name, message=release_data)
    sender.close_connection()
