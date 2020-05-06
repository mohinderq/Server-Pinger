import platform
from subprocess import call, PIPE
from time import sleep
from datetime import datetime
import argparse
from telebot import TeleBot


class Host(object):
    host = None
    is_running = None

    def __init__(self, host: str, timeout: int) -> type(None):
        self.host = host
        self.timeout = timeout
        self.is_running = self.__ping()

    def __ping(self) -> bool:
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', self.host]
        return call(command, stdout=PIPE) == 0

    def __log(self, message: str) -> type(None):
        print('$$ {} {}'.format(datetime.now(), str(message)))

    def run(self) -> type(None):
        self.is_running = self.__ping()
        status_now = self.__ping()
        self.__log("Host {} | Connection {}".format(self.host, str(status_now)))
        if status_now is not self.is_running:
            self.is_running = status_now
            sleep(self.timeout)
            status_after_timeout = self.__ping()
            if self.is_running is status_after_timeout:
                self.__log('Host {} | Connection switched | Notify user'.format(self.host))
                Notifier(self)
            else:
                self.is_running = status_after_timeout


class Notifier(object):
    _API_KEY = '1149529360:AAEhj_pATeppJAP04JLZ-9jqQNXNN1lk7Z0'
    _CHAT_ID = '207313997'
    _bot = None

    def __init__(self, host: Host) -> type(None):
        self.host = host
        self._bot = TeleBot(self._API_KEY)
        self._notify()

    def _notify(self) -> type(None):
        self._bot.send_message(self._CHAT_ID, "Host {} | Connection {}"
                               .format(str(self.host.host), str(self.host.is_running)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Server pinger')
    parser.add_argument('--ip', required=True, type=str, help='A list of ip\'s to ping')
    parser.add_argument('--interval', default=10, required=False, type=int, help='Pinging every X second to IP')
    parser.add_argument('--timeout', default=30, required=False, type=int, help='Checking connectivity status again '
                                                                                'to verify it after X seconds')
    args = parser.parse_args()
    ips = str(args.ip).split(',')

    hosts = []

    for ip in ips:
        h = Host(ip, args.timeout)
        hosts.append(h)

    while True:
        for host in hosts:
            host.run()
        sleep(args.interval)