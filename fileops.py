import os
import sqlite3
import csv
from datetime import datetime
from openpyxl import Workbook
from openpyxl.chart import LineChart, Reference
from openpyxl.chart.axis import DateAxis

#======= global
linestmdir = []
sqlconsole = object
'''cumpleted '''
#======================================================================================================================= database

def DBConnect():
    global sqlconsole
    dbConnection = sqlite3.connect('BreadHistory.db')
    sqlconsole = dbConnection.cursor()
    try:
        DBInit()
    except:
        pass
    return

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

    sqlconsole.execute(q1)
    sqlconsole.execute(q2)
    sqlconsole.execute(q3)

'''cumpleted '''
#======================================================================================================================= settings

def SaveSettings(l1lt, l1dir, l2lt, l2dir, l3lt, l3dir):
    doc = open('settings.txt', 's')
    doc.write(f"{l1dir};;{l1lastime}\n")
    doc.write(f"{l2dir};;{l2lastime}\n")
    doc.write(f"{l3dir};;{l3lastime}\n")
    doc.close()
    return

def LoadSettings():
    global linestmdir
    doc = open('settings.txt', 'r')
    linestmdir.append(doc.read().split(';;'))
    linestmdir.append(doc.read().split(';;'))
    linestmdir.append(doc.read().split(';;'))
    doc.close()
    return

#======================================================================================================================= data operations

def LoadData(line, lasttime):
    path = linestmdir[line - 1][0]
    pattern = "Detailed min</>.csv.csv" #2022 - 11 - 28 - 19 - 00 - 00


def LoadLogFile(filepath):
    if lineonedir in filepath:
        line = 'LineOne'
    elif linetwodir in filepath:
        line = 'LineTwo'
    elif linethreedir in filepath:
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
      dtm = datetime(int(log[2]), int(log[3]), int(log[4]), int(log[5]), int(log[6]), 0)
      print(dtm)
      print(row)
      sqlconsole.execute(f"INSERT INTO {line} (time, loafs, defective) VALUES ('{dtm}', {log[1]}, {log[0]})")
    return

def SearchData(timestart, timeend, line):
    res = [[]]
    for line in lines:
        if 1 in lines:
            r1 = sqlconsole.execute(f"SELECT loafs, defective, time FROM LineOne WHERE time BETWEEN {timestart} AND {timeend}")
            res[0].append(1)
            res.append(list(r1))
        if 2 in lines:
            r1 = sqlconsole.execute(f"SELECT loafs, defective, time FROM LineTwo WHERE time BETWEEN {timestart} AND {timeend}")
            res[0].append(2)
            res.append(list(r2))
        if 3 in lines:
            r1 = sqlconsole.execute(f"SELECT loafs, defective, time FROM LineThree WHERE time BETWEEN {timestart} AND {timeend}")
            res[0].append(3)
            res.append(list(r3))
    return res

#======================================================================================================================= result
def Result(dtms, dtme, lines, chart): # TODO
    wb = Workbook()
    ws = wb.active
    #rows = SearchData(1, 2, 3) # TODO </ref> SearcData <ref>
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
        if #TODO
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

#============ TEST CODE


