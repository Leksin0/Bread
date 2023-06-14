import sqlite3
import csv
import json
import os
from datetime import datetime
from openpyxl import Workbook
from openpyxl.chart import LineChart, Reference
from openpyxl.chart.axis import DateAxis


def Setup():
    doc = open('settings.json', mode='w')
    json.dump({1}, doc)
    DBInit()

def Reset():#DANGEROUS
    try:
        os.remove('settings.json')
        doc = open('settings.json', mode='w')
        json.dump({}, doc)
    except:
        pass
    try:
        os.remove('BreadHistory.db')
        DBInit()
    except:
        pass


def DBCursor():
    dbConnection = sqlite3.connect('BreadHistory.db')
    return dbConnection.cursor()

def DBInit():
    q1 = '''CREATE TABLE LineOne (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time DATETIME NOT NULL,
            loafs INTEGER NOT NULL,
            defective INTEGER NOT NULL)'''
    q2 = '''CREATE TABLE LineTwo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time DATETIME NOT NULL,
            loafs INTEGER NOT NULL,
            defective INTEGER NOT NULL)'''
    q3 = '''CREATE TABLE LineThree (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time DATETIME NOT NULL,
            loafs INTEGER NOT NULL,
            defective INTEGER NOT NULL)'''
    DBCursor().execute(q1)
    DBCursor().execute(q2)
    DBCursor().execute(q3)

def SaveSettings(key, value):
    doc = open('settings.json', mode='r')
    data = json.load(doc)
    data.update({key: value})
    doc.close()
    os.remove('settings.json')
    doc = open('settings.json', mode='w')
    json.dump(data, doc)
    doc.close()

def LoadSettings(key):
    doc = open('settings.json', mode='r')
    data = json.load(doc)
    doc.close
    try:
        return data[key]
    except:
        SaveSettings(key, None)
        return None


def LoadData(line, lastime):
    dirpath = LoadSettings(f"{line}path")
    while True:
        try:
            pattern = "/Detailed min</>.csv.csv"
            new = str(lastime)
            new = new.replace(' ', '-')
            new = new.replace(':', '-')
            path = dirpath + pattern.replace('</>', new)
            LoadLogFile(line, path)
        except:
            break
        else:
            if lastime.hour == 7:
                lastime = lastime.replace(hour=19)
            else:
                try:
                    lastime = lastime.replace(day=lastime.day+1, hour=7)
                except:
                    try:
                        lastime = lastime.replace(month=lastime.month+1, day=1, hour=7)
                    except:
                        lastime = lastime.replace(year=lastime.year+1, month=1, day=1, hour=7)
    SaveSettings(f"{line}time", lastime)

def LoadLogFile(lnum, filepath):
    if lnum == 1:
        line = 'LineOne'
    elif lnum == 2:
        line = 'LineTwo'
    elif lnum == 3:
        line = 'LineThree'
    doc = open(filepath, encoding='Windows-1251')
    reader = csv.reader(doc)
    reader.__next__()
    reader.__next__()
    for row in reader:
        st = row[0]
        log = [st.split('  ')[0]]
        for j in st.split('  ')[1].split(';'):
            log.append(j)
        dtm = (log[0].split('.'))[::-1] + log[1].split(':')
        for d in dtm:
            log.append(d)
        del log[0]
        del log[0]
        dtm = datetime(int(log[2]), int(log[3]), int(log[4]), int(log[5]), int(log[6]))
        DBCursor().execute(f"INSERT INTO {line} (time, loafs, defective) VALUES ('{dtm}', {log[1]}, {log[0]})")

def SearchData(timestart, timeend, line):
    if line == 1:
        res = DBCursor().execute(f"SELECT loafs, defective, time FROM LineOne WHERE time BETWEEN {timestart} AND {timeend}")
    elif line == 2:
        res = DBCursor().execute(f"SELECT loafs, defective, time FROM LineTwo WHERE time BETWEEN {timestart} AND {timeend}")
    elif line == 3:
        res = DBCursor().execute(f"SELECT loafs, defective, time FROM LineThree WHERE time BETWEEN {timestart} AND {timeend}")
    return res

#TODO                                >  >  RR  EE  SS  UU  LL  TT  <  <

def Result(dtms, dtme, lines, unit, chart, erp): # TODO
    for line in [1, 2, 3]: #DB update
        LoadData(line, LoadSettings(f"{line}time"))

    wb = Workbook()
    ws = wb.active
    for l in lines:# TODO ---
        rows = SearchData(dtms, dtme, line)
        if unit == 'h':
            pass
        if unit == 'd':
            pass
        if unit == 'w':
            pass
        if unit == 'm':
            pass
        for row in rows:
            ws.append(row)
    if chart:
        chart = LineChart()
        chart.title = ""
        chart.style = 1
        chart.y_axis.title = "Size"
        chart.y_axis.crossAx = 500
        chart.x_axis.title = "Date"
        chart.x_axis = DateAxis(crossAx=100)
        if true: #TODO
            chart.x_axis.number_format = 'dd-mmm'
        else:
            a #TODO
            chart.x_axis.majorTimeUnit = "days"

        data = Reference(ws, min_col=2, min_row=1, max_col=4, max_row=7)
        chart.add_data(data, titles_from_data=True)
        dates = Reference(ws, min_col=1, min_row=2, max_row=7)
        chart.set_categories(dates)
        ws.add_chart(chart, "E1")

    wb.save("some_cringe_name.xlsx")
    return

# кто прочитал тот лох