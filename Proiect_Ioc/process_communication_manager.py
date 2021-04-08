from multiprocessing.connection import Client


class ProcessCommunicationManager:
    def __init__(self):
        self.conn = None
        try:
            address = ('localhost', 9998)
            self.conn = Client(address, authkey=bytes('secret password', 'utf-8'))
        except Exception as e:
            print("Can not connect ", e)

    def send_message(self, message):
        self.conn.send(message)

    def close(self):
        if self.conn is not None:
            self.send_message("close")
            self.conn.close()
