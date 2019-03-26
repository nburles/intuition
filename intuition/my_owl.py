from protocol import ET, parse_datagram
import multiprocessing, datetime, time
from owl_types import OWLTypes, ChannelTypes

q = multiprocessing.Queue()

def datagram_received(self, data, address):
    data = ET.fromstring(data)
    msg = parse_datagram(data)
    timestamp = data.find('./timestamp')
    if timestamp:
        timestamp = timestamp.text
    else:
        timestamp = time.time()
    dt_utc = datetime.datetime.fromtimestamp(int(timestamp))
    self._timestamp = dt_utc.strftime('%Y-%m-%d %H:%M:%S')
    msg.enqueue()

def enqueue(self):
    q.put(self.to_dict())

def solar_dict(self):
    return {
        'type': 'solar',
        'generated_instant': str(int(1000 * self.generating.current_w)),
        'generated_cumulative': str(int(1000 * self.generating.daily_wh)),
        'exported_instant': str(int(1000 * self.exporting.current_w)),
        'exported_cumulative': str(int(1000 * self.exporting.daily_wh)),
    }

def electricity_dict(self):
    return {
        'type': 'electricity',
        'generated_instant': str(int(1000 * self.channels['1'].current_w)),
        'generated_cumulative': str(int(1000 * self.channels['1'].daily_wh)),
        'used_instant': str(int(1000 * self.channels['2'].current_w)),
        'used_cumulative': str(int(1000 * self.channels['2'].daily_wh)),
    }

def weather_dict(self):
    return {
        'type': 'weather',
        'temperature': str(self.temperature),
        'text': str(self.text),
    }

