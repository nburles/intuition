import os, tempfile, json, datetime, multiprocessing
import my_owl

q = multiprocessing.Queue()

def write_msg(msg):
    with tempfile.NamedTemporaryFile(suffix = '.owl', dir = 'values_to_upload', mode = 'w', delete = False) as fout:
        json.dump(msg, fout)

def _read_msgs():
    for fname in os.listdir('values_to_upload'):
        if fname.endswith('.owl'):
            with open(os.path.join('values_to_upload', fname), 'r') as fin:
                my_owl.q.put(json.load(fin))
            os.remove(os.path.join('values_to_upload', fname))

def read_msgs():
    _read_msgs()
    last_date = datetime.datetime.today().strftime('%Y-%m-%d')
    while True:
        try:
            q.get(block = True, timeout = 60)
            break
        except:
            pass
        new_date = datetime.datetime.today().strftime('%Y-%m-%d')
        if new_date != last_date:
            last_date = new_date
            _read_msgs()

