import tendo.singleton
from protocol import *
import multiprocessing
import time
from datetime import datetime
import os

me = tendo.singleton.SingleInstance()

q = multiprocessing.Queue()

def find_timestamp(data):
    timestamp = data.find('./timestamp')
    if timestamp:
        timestamp = timestamp.text
    else:
        timestamp = time.time()
    dt_utc = datetime.fromtimestamp(int(timestamp))
    return dt_utc.strftime('%Y-%m-%d %H:%M:%S')

def enqueue(data, msg_type, args):
    q.put((
        find_timestamp(data),
        msg_type,
        *args
    ))

def my_solar_enqueue(self, data):
    enqueue(
        data,
        's',
        (
            *self.generating.as_tuple('g'),
            *self.exporting.as_tuple('e')
        )
    )

def my_electricity_enqueue(self, data):
    enqueue(
        data,
        'e',
        (
            *self.channels['1'].as_tuple('s'),
            *self.channels['2'].as_tuple('u')
        )
    )

def my_weather_enqueue(self, data):
    enqueue(
        data,
        'w',
        (
            self.temperature,
            self.text
        )
    )

def my_owl_channel_tuple(self, channel_type):
    return (
        channel_type,
        int(1000 * self.current_w),
        int(1000 * self.daily_wh)
    )

def my_datagram_received(self, data, address):
    data = ET.fromstring(data)
    msg = parse_datagram(data)
    msg.enqueue(data)

def read():
    if not os.path.exists('output'):
        os.makedirs('output')
    while True:
        msg = q.get()
        if msg == None:
            break
        with open(os.path.join('output', msg[0][:10] + '.csv'), 'a+') as csv_file:
            csv_file.write(','.join(map(str, msg)))
            csv_file.write('\n')

def main():
    proc = multiprocessing.Process(target = read)
    proc.start()

    OwlIntuitionProtocol.datagram_received = my_datagram_received
    OwlSolar.enqueue = my_solar_enqueue
    OwlElectricity.enqueue = my_electricity_enqueue
    OwlWeather.enqueue = my_weather_enqueue
    OwlChannel.as_tuple = my_owl_channel_tuple
    start_listening()

    q.put(None)
    proc.join()

if __name__ == "__main__":
    main()

