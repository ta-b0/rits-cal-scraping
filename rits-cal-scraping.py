import pandas as pd
import datetime
import csv
from icalendar import Calendar, Event
from datetime import datetime
import pytz

def read_cal():
    url = "http://www.ritsumei.ac.jp/profile/info/calendar/2020/"
    data = pd.read_html(url,header = 0)
    for semester in range(2):
        df = data[semester]
        # print(df)
        parse_cal(df)
        parse_cal_in_ics(df)

def parse_cal(df):
    tocsv = [["Subject","Start Date","End Date","Description","Location"]]
    for i in range(len(df)):
        date = Date(df, i)
        event = df.at[i,'行事']
        contents = []
        contents.append(event)
        contents.append(date.csv_datetime())
        contents.append(date.csv_datetime())
        contents.append('立命館大学')
        # print(contents)
        tocsv.append(contents)
    print(tocsv)
    with open("cal.csv","a") as f:
        writer = csv.writer(f)
        writer.writerows(tocsv)

# ics形式で出力させる
def parse_cal_in_ics(df):
    cal = Calendar()
    for i in range(len(df)):
        event = Event()
        # 日付の処理
        date = Date(df, i)
        summary = df.at[i,'行事']
        # 開始時間と終了時間を同じ日にしている，これで終日になる??
        event.add('dtstart', date.ical_datetime())
        event.add('dtend', date.ical_datetime())
        event.add('summary', summary)
        event.add('location', "立命館大学")
        cal.add_component(event)

    with open("cal.ics","a") as f:
        print(display(cal))
        f.write(display(cal))

# icalをデコードして表示する用にするfunction
def display(cal):
    return cal.to_ical().decode('utf-8').replace('\r\n', '\n').strip()

class Date():
    # データと行を与えて日付を抽出する
    def __init__(self, df, i):
        self.month = df.at[i,'月']
        self.day = df.at[i,'日']

        if self.month >= 4:
            self.year = 2020
        elif self.month == 3 and self.day == 31 and i == 0:
            self.year = 2020
        else:
            self.year = 2021
        self.month = '%02d' % int(self.month)
        self.day = '%02d' % int(self.day)

    # csv形式で出力
    def csv_datetime(self):
        return '{0}-{1}-{2}'.format(self.year, self.month, self.day)

    # ical形式の日付を出力する
    def ical_datetime(self):
        return datetime(int(self.year), int(self.month), int(self.day), tzinfo=pytz.timezone("Asia/Tokyo"))

def main():
    read_cal()

if __name__ == '__main__':
    main()