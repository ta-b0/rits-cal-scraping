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
        # parse_cal_in_ics(df)

def parse_cal(df):
    tocsv = [["Subject","Start Date","End Date","Description","Location"]]
    for i in range(len(df)):
        # print(df.iloc[i])
        month = df.at[i,'月']
        day = df.at[i,'日']
        event = df.at[i,'行事']
        if month >= 4:
            year = 2020
        elif month == 3 and day == 31 and i == 0:
            year = 2020
        else:
            year = 2021
        month = '%02d' % int(month)
        day = '%02d' % int(day)
        date = '{0}-{1}-{2}'.format(year,month,day)
        contents = []
        contents.append(event)
        contents.append(date)
        contents.append(date)
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
        month = df.at[i,'月']
        day = df.at[i,'日']
        summary = df.at[i,'行事']
        if month >= 4:
            year = 2020
        elif month == 3 and day == 31 and i == 0:
            year = 2020
        else:
            year = 2021
        month = '%02d' % int(month)
        day = '%02d' % int(day)
        # 開始時間と終了時間を同じ日にしている，これで終日になる??
        event.add('dtstart', datetime(int(year), int(month), int(day), tzinfo=pytz.timezone("Asia/Tokyo")))
        event.add('dtend', datetime(int(year), int(month), int(day), tzinfo=pytz.timezone("Asia/Tokyo")))
        event.add('summary', summary)
        event.add('location', "立命館大学")
        cal.add_component(event)

    with open("cal.ics","a") as f:
        print(display(cal))
        f.write(display(cal))

# icalをデコードして表示する用にするfunction
def display(cal):
    return cal.to_ical().decode('utf-8').replace('\r\n', '\n').strip()
def main():
    read_cal()

if __name__ == '__main__':
    main()