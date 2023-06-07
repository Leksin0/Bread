import os
import sqlite3
import csv
from datetime import datetime
from openpyxl import Workbook
from openpyxl.chart import LineChart, Reference
from openpyxl.chart.axis import DateAxis



#======= global
lineonedir = '/Users/maksim/Desktop/Лицейский проект/Логи хлебопечек/Линия 1' # TODO UI
global linetwodir
global linethreedir
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

def DBReset():
    os.remove('BreadHistory.db')
    return

#======================================================================================================================= settings

def SaveSettings(l1lt, l1dir, l2lt, l2dir, l3lt, l3dir): #TODO
    doc = open('settings.txt', 's')
    doc.write(f"{l1lastime}\n")
    doc.write(f"{l2lastime}\n")
    doc.write(f"{l3lastime}\n")
    return

def LoadSettings():
    doc = open('settings.txt', 'r')  #TODO
    return

#======================================================================================================================= data operations

def LoadData(line, lasttime):
    next = lasttime.split(';')[thingmabob]#TODO


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

def SearchData(timestart, timeend, lines):
    res = []
    for line in lines:
        for i in sqlconsole.execute(f'''SELECT loafs, defective, time FROM Main
                                    WHERE time BETWEEN {timestart} AND {timeend}''' ): #TODO
            pass
    return res

#======================================================================================================================= result
def Result(): # TODO
    wb = Workbook()
    ws = wb.active
    #rows = SearchData(1, 2, 3) # TODO </ref> SearcData <ref>
    for row in rows:
        ws.append(row)

    chart = LineChart()
    chart.title = ""
    chart.style = 1
    chart.y_axis.title = "Size"
    chart.y_axis.crossAx = 500
    chart.x_axis = DateAxis(crossAx=100)
    chart.x_axis.number_format = 'd-mmm'
    chart.x_axis.majorTimeUnit = "days"
    chart.x_axis.title = "Date"

    data = Reference(ws, min_col=2, min_row=1, max_col=4, max_row=7)
    chart.add_data(data, titles_from_data=True)
    dates = Reference(ws, min_col=1, min_row=2, max_row=7)
    chart.set_categories(dates)
    ws.add_chart(chart, "E1")

    wb.save("some_cringe_name.xlsx")

#============ TEST CODE


