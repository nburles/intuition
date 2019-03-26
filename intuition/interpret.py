import tendo.singleton
import subprocess
import os
import csv
from datetime import datetime, timedelta
import time
import plotly
from decimal import Decimal
import shutil
import sftp

me = tendo.singleton.SingleInstance()

HEAD_0 = '<html><head><meta charset="utf-8" /><meta http-equiv="refresh" content="60"><script src="plotly.min.js"></script></head><body>'
HEAD_2 = '<html><head><meta charset="utf-8" /><script src="../../graphs/plotly.min.js"></script></head><body>'
HEAD_3 = '<html><head><meta charset="utf-8" /><script src="../../../graphs/plotly.min.js"></script></head><body>'
TAIL = '</body></html>'

def make_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def make_folders(folders):
    for folder in folders:
        make_folder(os.path.join('output', *folder))

def backup():
    if not os.path.exists('backup'):
        print('Please create the symlink "backup"')
        sys.exit(1)
    subprocess.check_call('rsync --archive --delete ./output/ ./backup/', shell=True)

def upload():
    subprocess.check_call('rsync -ave "ssh -i {} -p {}" output/graphs/ {}@{}:{}'.format(sftp.KEY, str(sftp.PORT), sftp.USER, sftp.HOST, sftp.PATH), shell=True)

strp_ymdhms = lambda s : datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
dec = lambda s,d=1000 : Decimal(s) / d
trace = lambda x_,y_,n,f='tozeroy' : plotly.graph_objs.Scatter(x=x_, y=y_, name=n, mode='lines', fill=f)
layout = lambda t,yt : plotly.graph_objs.Layout(title=t, xaxis=dict(title='Time'), yaxis=dict(title=yt))
plot = lambda d,l,p=False : plotly.offline.plot({'data':d, 'layout':l}, output_type='div', include_plotlyjs=p, include_mathjax=False, show_link=False)

class PacketExtractor:
    def __init__(self, fname):
        self._solar, self._weather, self._electricity = [], [], []
        with open(os.path.join('output', fname), 'r') as fin:
            for row in csv.reader(fin):
                if row[1] == 's':   self._solar.append(row)
                elif row[1] == 'e': self._electricity.append(row)
                elif row[1] == 'w': self._weather.append(row)
        self._fname = fname
        make_folder(os.path.join('output', 'daily', self._fname[:4], self._fname[5:7]))

    def daily(self):
        last_e = self._electricity[-1] if self._electricity else ['']
        last_s = self._solar[-1] if self._solar else ['']
        generated = last_s[4] if last_s[0] > last_e[0] else last_e[4] if last_e[0] > last_s[0] else '0'
        exported = last_s[7] if last_s[0] else '0'
        used = last_e[7] if last_e[0] else '0'
        with open(os.path.join('output', 'daily', '.'.join([self._fname[:4], 'csv'])), 'a+') as fout:
            fout.write(','.join([self._fname[:10], generated, exported, used]) + '\n')

    def hourly(self):
        cum_g, cum_u, cum_e = [0] * 24, [0] * 24, [0] * 24
        for e in self._electricity:
            hour = int(e[0][11:13])
            cum_g[hour], cum_u[hour] = [int(e[i]) if int(e[i]) > t else t for i, t in ((4, cum_g[hour]), (7, cum_u[hour]))]
        for s in self._solar:
            hour = int(s[0][11:13])
            cum_g[hour], cum_e[hour] = [int(s[i]) if int(s[i]) > t else t for i, t in ((4, cum_g[hour]), (7, cum_e[hour]))]
        generated, exported, used = [[t[0]] + [t[i] - t[i-1] for i in range(1, 24)] for t in (cum_g, cum_e, cum_u)]
        final = [self._fname[:10]] + [item for hour in zip(cum_g, generated, cum_e, exported, cum_u, used) for item in hour]
        with open(os.path.join('output', 'hourly', '.'.join([self._fname[:4], 'csv'])), 'a+') as fout:
            fout.write(','.join(map(str, final)) + '\n')

    def daily_graph(self, today=False):
        gen_ex_x, generated_y, exported_y = zip(*[(strp_ymdhms(row[0]), dec(row[3]), dec(row[6])) for row in self._solar])
        used_x, used_y = zip(*sorted([(strp_ymdhms(row[0]), dec(row[6])) for row in self._electricity]))
        div = plot([
            trace(gen_ex_x, generated_y, 'Generated', None),
            trace(gen_ex_x, exported_y, 'Exported', None),
            trace(used_x, used_y, 'Used', None)
        ], layout(self._fname[:10], 'Watts'))
        with open(os.path.join('output', 'daily', self._fname[:4], self._fname[5:7], self._fname[:10] + '.html'), 'w') as fout:
            fout.write(HEAD_3 + div + TAIL)
        if today:
            with open(os.path.join('output', 'graphs', 'today.html'), 'w') as fout:
                fout.write(HEAD_0 + div + TAIL)
        if self._fname[:10] == (datetime.today() - timedelta(1)).strftime('%Y-%m-%d'):
            with open(os.path.join('output', 'graphs', 'yesterday.html'), 'w') as fout:
                fout.write(HEAD_0 + div + TAIL)

class HourlyExtractor:
    def __init__(self, fname):
        self._timestamps, self._generated, self._exported, self._used = [], [], [], []
        with open(os.path.join('output', 'hourly', fname), 'r') as fin:
            for row in csv.reader(fin):
                for hour in range(24):
                    self._timestamps.append(strp_ymdhms(' '.join([row[0], '{:02d}:59:59'.format(hour)])))
                    self._generated.append(dec(row[hour*6 + 2]))
                    self._exported.append(dec(row[hour*6 + 4]))
                    self._used.append(dec(row[hour*6 + 6]))
        self._fname = fname

    def hourly_graph(self, today=False):
        div = plot([
            trace(self._timestamps, self._generated, 'Generated'),
            trace(self._timestamps, self._exported, 'Exported'),
            trace(self._timestamps, self._used, 'Used')
        ], layout(self._fname[:4], 'Watt-Hours'))
        with open(os.path.join('output', 'hourly', 'graphs', '.'.join([self._fname[:4], 'html'])), 'w') as fout:
            fout.write(HEAD_2 + div + TAIL)
        if today:
            with open(os.path.join('output', 'graphs', 'hourly.html'), 'w') as fout:
                fout.write(HEAD_0 + div + TAIL)

class DailyExtractor:
    def __init__(self, fname):
        self._timestamps, self._generated, self._exported, self._used = [], [], [], []
        with open(os.path.join('output', 'daily', fname), 'r') as fin:
            for row in csv.reader(fin):
                self._timestamps.append(strp_ymdhms(' '.join([row[0], '23:59:59'])))
                self._generated.append(dec(row[1], 1000000))
                self._exported.append(dec(row[2], 1000000))
                self._used.append(dec(row[3], 1000000))
        self._fname = fname

    def year_by_day_graph(self, today=False):
        div = plot([
            trace(self._timestamps, self._generated, 'Generated'),
            trace(self._timestamps, self._exported, 'Exported'),
            trace(self._timestamps, self._used, 'Used')
        ], layout(self._fname[:4], 'Kilowatt-Hours'))
        with open(os.path.join('output', 'daily', 'graphs_by_day', '.'.join([self._fname[:4], 'html'])), 'w') as fout:
            fout.write(HEAD_2 + div + TAIL)
        if today:
            with open(os.path.join('output', 'graphs', 'daily.html'), 'w') as fout:
                fout.write(HEAD_0 + div + TAIL)

    def year_by_month_graph(self, today=False):
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        generated, exported, used = [0] * 12, [0] * 12, [0] * 12
        for t, g, e, u in zip(self._timestamps, self._generated, self._exported, self._used):
            generated[t.month - 1] += g
            exported[t.month - 1] += e
            used[t.month - 1] += u
        div = plot([
            trace(months, generated, 'Generated'),
            trace(months, exported, 'Exported'),
            trace(months, used, 'Used')
        ], layout(self._fname[:4], 'Kilowatt-Hours'))
        with open(os.path.join('output', 'daily', 'graphs_by_month', '.'.join([self._fname[:4], 'html'])), 'w') as fout:
            fout.write(HEAD_2 + div + TAIL)
        if today:
            with open(os.path.join('output', 'graphs', 'monthly.html'), 'w') as fout:
                fout.write(HEAD_0 + div + TAIL)

def main():
    for folder in (('original',), ('hourly', 'original'), ('hourly', 'graphs'), ('daily', 'original'), ('daily', 'graphs_by_day'), ('daily', 'graphs_by_month'), ('graphs',)):
        if not os.path.exists(os.path.join('output', *folder)):
            os.makedirs(os.path.join('output', *folder))
    with open(os.path.join('output', 'hourly', 'header.csv'), 'w') as fout:
        fout.write('YYYY-MM-DD')
        for hour in range(24):
            fout.write(',generated (cumulative, {0}, mwh),generated ({0}, mwh),exported (cumulative, {0}, mwh),exported ({0}, mwh),used (cumulative, {0}, mwh),used ({0}, mwh)'.format('{:02d}-{:02d}'.format(hour, hour+1)))
    with open(os.path.join('output', 'daily', 'header.csv'), 'w') as fout:
        fout.write('YYYY-MM-DD,generated (mwh),exported (mwh),used (mwh)')
    last_run = ''
    plotly.offline.plot({'data':[trace([1],[2],'')], 'layout':plotly.graph_objs.Layout()}, output_type='file', include_plotlyjs='directory', filename=os.path.join('output', 'graphs', 'today.html'))
    while True:
        if datetime.now().hour < 2:
            time.sleep(3600)
            continue
        date_today = datetime.today().strftime('%Y-%m-%d')
        today = '.'.join([date_today, 'csv'])
        files = sorted([f for f in os.listdir('output') if not f in [today, 'original', 'hourly', 'daily', 'graphs']])
        for fname in files:
            pe = PacketExtractor(fname)
            pe.daily()
            pe.hourly()
            pe.daily_graph()
            os.rename(os.path.join('output', fname), os.path.join('output', 'original', fname))
        if os.path.exists(os.path.join('output', today)):
            pe = PacketExtractor(today)
            pe.daily_graph(today=True)
        today_year = '.'.join([date_today[:4], 'csv'])
        files = sorted([f for f in os.listdir(os.path.join('output', 'hourly')) if f.endswith('.csv') and not f in ['header.csv', today_year]])
        for fname in files:
            he = HourlyExtractor(fname)
            he.hourly_graph()
            os.rename(os.path.join('output', 'hourly', fname), os.path.join('output', 'hourly', 'original', fname))
        files = sorted([f for f in os.listdir(os.path.join('output', 'daily')) if f.endswith('.csv') and not f in ['header.csv', today_year]])
        for fname in files:
            de = DailyExtractor(fname)
            de.year_by_day_graph()
            de.year_by_month_graph()
            os.rename(os.path.join('output', 'daily', fname), os.path.join('output', 'daily', 'original', fname))
        if last_run != today and datetime.now().hour > 2:
            if os.path.exists(os.path.join('output', 'hourly', today_year)):
                he = HourlyExtractor(today_year)
                he.hourly_graph(today=True)
            if os.path.exists(os.path.join('output', 'daily', today_year)):
                de = DailyExtractor(today_year)
                de.year_by_day_graph(today=True)
                de.year_by_month_graph(today=True)
            last_run = today
        backup()
        upload()
        time.sleep(300)

if __name__ == "__main__":
    main()

