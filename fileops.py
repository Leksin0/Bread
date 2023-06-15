import sqlite3
import csv
import json
import os
from datetime import datetime
from openpyxl import Workbook
from openpyxl.chart import LineChart, Reference
from openpyxl.chart.axis import DateAxis

def Setup():
    try:
        doc = open('settings.json', mode='r')
        json.load(doc)
        doc.close()
    except:
        doc = open('settings.json', mode='w')
        json.dump({}, doc)
        doc.close()
        SaveSettings("1time", "2022-11-28-07-00-00")
        SaveSettings("2time", "2022-11-28-07-00-00")
        SaveSettings("3time", "2022-11-28-07-00-00")
    try:
        DBInit()
    except:
        pass

def Reset():#DANGEROUS
    try:
        os.remove('settings.json')
    except:
        pass
    try:
        os.remove('BreadHistory.db')
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
    doc.close()
    data.update({key: value})
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

def LoadData(line):
    dirpath = LoadSettings(f"{line}path")
    nextime = LoadSettings(f"{line}time")
    while True:
        try:
            pattern = "/Detailed min</>.csv.csv"
            name = pattern.replace('</>', nextime)
            path = dirpath + name
            LoadLogFile(line, path)
        except FileNotFoundError:
            break
        else:
            log = nextime.split('-')
            nextime = datetime(int(log[0]), int(log[1]), int(log[2]), int(log[3]))
            if nextime.hour == 7:
                nextime = nextime.replace(hour=19)
            else:
                try:
                    nextime = nextime.replace(day=nextime.day + 1, hour=7)
                except:
                    try:
                        nextime = nextime.replace(month=nextime.month + 1, day=1, hour=7)
                    except:
                        nextime = nextime.replace(year=nextime.year + 1, month=1, day=1, hour=7)
            temp = []
            temp.append(str(nextime.year))
            temp.append(str(nextime.month))
            if len(temp[1]) == 1:
                temp[1] = "0" + temp[1]
            temp.append(str(nextime.day))
            if len(temp[2]) == 1:
                temp[2] = "0" + temp[2]
            temp.append(str(nextime.hour))
            if len(temp[3]) == 1:
                temp[3] = "0" + temp[3]
            temp.append("00")
            temp.append("00")
            nextime = "-".join(temp)
    log = nextime.split('-')
    nextime = datetime(int(log[0]), int(log[1]), int(log[2]), int(log[3]))
    if nextime.hour == 7:
        nextime = nextime.replace(hour=19)
    else:
        nextime = nextime.replace(hour=7)
        try:
            nextime = nextime.replace(day=nextime.day + 1)
        except:
            try:
                nextime = nextime.replace(month=nextime.month + 1, day=1)
            except:
                nextime = nextime.replace(year=nextime.year + 1, month=1, day=1)
    temp = []
    temp.append(str(nextime.year))
    temp.append(str(nextime.month))
    if len(temp[1]) == 1:
        temp[1] = "0" + temp[1]
    temp.append(str(nextime.day))
    if len(temp[2]) == 1:
        temp[2] = "0" + temp[2]
    temp.append(str(nextime.hour))
    if len(temp[3]) == 1:
        temp[3] = "0" + temp[3]
    temp.append("00")
    temp.append("00")
    nextime = "-".join(temp)
    SaveSettings(f"{line}time", nextime)

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
        row = row[0].split(';')
        log = row[0]
        dt = log.split('  ')[0].split('.')
        tm = log.split('  ')[1].split(':')
        dtm = datetime.datetime(int(dt[2]), int(dt[1]), int(dt[0]), int(tm[0]), int(tm[1]))
        DBCursor().execute(f"INSERT INTO {line} (time, loafs, defective) VALUES ('{str(dtm)}', {row[2]}, {row[1]})")

def SearchData(timestart, timeend, line):
    if line == '1':
        res = DBCursor().execute(f"SELECT loafs, defective, time FROM LineOne WHERE time BETWEEN {str(timestart)} AND {str(timeend)}")
    elif line == '2':
        res = DBCursor().execute(f"SELECT loafs, defective, time FROM LineTwo WHERE time BETWEEN {str(timestart)} AND {str(timeend)}")
    elif line == '3':
        res = DBCursor().execute(f"SELECT loafs, defective, time FROM LineThree WHERE time BETWEEN {str(timestart)} AND {str(timeend)}")
    return res

def Result(dtms, dtme, lines, unit, chart, erp):
    frow = [""]
    for line in [1, 2, 3]:
        LoadData(line)#DB update
    for l in lines:
        frow.append(f"Линия {l}")
    if erp[0]:
        frow.append("")
        frow.append(f"Норма")
    wb = Workbook()
    ws = wb.active
    for l in lines:
        rows = SearchData(dtms, dtme, l)
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
        if unit == 'h':
            chart.x_axis.number_format = 'dd-mmm-hh:mm'
            chart.x_axis.majorTimeUnit = "hours"
        elif unit == 'd':
            chart.x_axis.number_format = 'dd-mmm'
            chart.x_axis.majorTimeUnit = "days"
        elif unit == 'w':
            chart.x_axis.number_format = 'dd-mmm'
            chart.x_axis.majorTimeUnit = "days"
        elif unit == 'm':
            chart.x_axis.number_format = 'mmm-yyyy'
            chart.x_axis.majorTimeUnit = "months"

        data = Reference(ws, min_col=2, min_row=1, max_col=4, max_row=7)
        chart.add_data(data, titles_from_data=True)
        dates = Reference(ws, min_col=1, min_row=2, max_row=7)
        chart.set_categories(dates)
        ws.add_chart(chart, "E1")

    wb.save(f"Отчет за {dtms.day}.{dtms.month}-{dtme.day}.{dtme.month}.xlsx")
    return