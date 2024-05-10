import PCANBasic
import types
from pcan import CAN
from threading import Event


class Robomaster():
    exit = Event()

    def __init__(self):
        self.can1 = CAN(bitrate=PCANBasic.PCAN_BAUD_1M)

        self.run()

    def run(self):
        while not self.exit.is_set():
            result = PCANBasic.PCAN_ERROR_OK
            if not (result & PCANBasic.PCAN_ERROR_QRCVEMPTY):
                result, message, timestamp = self.can1.read()
                if result != PCANBasic.PCAN_ERROR_OK and result != PCANBasic.PCAN_ERROR_QRCVEMPTY:
                    print(self.can1.get_error_text(result))
                    return
                else:
                    print(timestamp, self.can1.get_message_id_text(message), self.can1.get_message_hex(message))

        # perform any cleanup here
        print('Stopping')


def quit(signo, _frame):
    print("Interrupted by %d, shutting down" % signo)
    exit.set()


if __name__ == '__main__':
    import signal
    for sig in ('TERM', 'INT'):  # 'HUP'
        signal.signal(getattr(signal, 'SIG'+sig), quit)

    robo = Robomaster()
