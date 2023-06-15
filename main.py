import fileops
from fileops import *
import sqlite3
import sys
from datetime import datetime
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QGroupBox, QVBoxLayout, QFormLayout
from PyQt6.QtWidgets import QPushButton, QLabel, QFileDialog, QCheckBox, QDateTimeEdit, QRadioButton, QLineEdit
from PyQt6.QtGui import QIntValidator

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dirwindow = None

        self.cbl1 = QCheckBox("Линия 1")
        self.cbl1.clicked.connect(self.rborcb_click)
        self.cbl2 = QCheckBox("Линия 2")
        self.cbl2.clicked.connect(self.rborcb_click)
        self.cbl3 = QCheckBox("Линия 3")
        self.cbl3.clicked.connect(self.rborcb_click)
        linhelp = QVBoxLayout()
        linhelp.addWidget(self.cbl1)
        linhelp.addWidget(self.cbl2)
        linhelp.addWidget(self.cbl3)
        lineselect = QGroupBox("Линии")
        lineselect.setLayout(linhelp)

        self.rbu1 = QRadioButton("Час")
        self.rbu1.clicked.connect(self.rborcb_click)
        self.rbu2 = QRadioButton("Сутки")
        self.rbu2.clicked.connect(self.rborcb_click)
        self.rbu3 = QRadioButton("Неделя")
        self.rbu3.clicked.connect(self.rborcb_click)
        self.rbu4 = QRadioButton("Месяц")
        self.rbu4.clicked.connect(self.rborcb_click)
        unhelp = QVBoxLayout()
        unhelp.addWidget(self.rbu1)
        unhelp.addWidget(self.rbu2)
        unhelp.addWidget(self.rbu3)
        unhelp.addWidget(self.rbu4)
        unitselect = QGroupBox("Единица времени")
        unitselect.setLayout(unhelp)

        self.cbchart = QCheckBox("Добавить график")
        self.cberp = QCheckBox("Сравнить с нормой производства")
        dophelp = QVBoxLayout()
        dophelp.addWidget(self.cbchart)
        dophelp.addWidget(self.cberp)
        addition = QGroupBox("Дополнительно")
        addition.setLayout(dophelp)

        lbts = QLabel("Начало периода")
        lbte = QLabel("Конец периода")
        self.timestart = QDateTimeEdit()
        self.timeend = QDateTimeEdit()

        lberp = QLabel("Норма производства")
        self.txerp = QLineEdit()
        self.txerp.setValidator(QIntValidator())

        btchdir = QPushButton("Указать расположение первичных данных")
        btchdir.clicked.connect(self.chdir_click)
        self.btresult = QPushButton("Готово")
        self.btresult.clicked.connect(self.GetResult)

        layout = QGridLayout()
        layout.addWidget(lbts, 0, 0)
        layout.addWidget(self.timestart, 0, 1)
        layout.addWidget(lbte, 1, 0)
        layout.addWidget(self.timeend, 1, 1)
        layout.addWidget(lberp, 0, 2)
        layout.addWidget(self.txerp, 1, 2)
        layout.addWidget(unitselect, 2, 0, 1, 1)
        layout.addWidget(lineselect, 2, 1, 1, 1)
        layout.addWidget(addition, 2, 2, 1, 1)
        layout.addWidget(btchdir, 3, 0)
        layout.addWidget(self.btresult, 3, 1)

        self.setWindowTitle("Статистика производства хлеба")
        self.container = QWidget()
        self.container.setLayout(layout)
        self.setCentralWidget(self.container)

    def chdir_click(self):
        if self.dirwindow is None:
            self.dirwindow = DirectoryChooseWindow()
        self.dirwindow.show()

    def bterp_click(self):
        if self.erpwindow is None:
            self.erpwindow = ERPInput()
        self.erpwindow.show()

    def rborcb_click(self):
        self.btresult.setText("Готово")

    def GetResult(self):
        if LoadSettings("1path") is None or LoadSettings("2path") is None or LoadSettings("3path") is None:
            self.btresult.setText("Укажите папки первичных данных")
            return
        else:
            pass
        if not self.rbu1.isChecked() and not self.rbu2.isChecked() and not self.rbu3.isChecked() and not self.rbu4.isChecked():
            self.btresult.setText("Выберите еденицу времени")
            return
        else:
            if self.rbu1.isChecked():
                unit = 'h'
            elif self.rbu2.isChecked():
                unit = 'd'
            elif self.rbu3.isChecked():
                unit = 'w'
            elif self.rbu4.isChecked():
                unit = 'm'
        if not self.cbl1.isChecked() and not self.cbl2.isChecked() and not self.cbl3.isChecked():
            self.btresult.setText("Выберите хотя бы одну линию")
            return
        else:
            lines = []
            if self.cbl1.isChecked():
                lines.append('1')
            if self.cbl2.isChecked():
                lines.append('2')
            if self.cbl3.isChecked():
                lines.append('3')
        try:
            a = int(self.txerp.text())
        except:
            if self.cberp.isChecked():
                self.btresult.setText("Укажите норму производства")
                return
        if self.cberp.isChecked():
            erp = [True, a]
        else:
            erp = [False]
        if self.cbchart.isChecked():
            chart = True
        else:
            chart = False
        dtms = self.timestart.text()
        log = []
        for j in dtms.split(' ')[0].split('.'):
            log.append(j)
        for h in dtms.split(' ')[1].split(':'):
            log.append(h)
        dtms = datetime(int(log[2]), int(log[1]), int(log[0]), int(log[3]), int(log[4]))
        dtme = self.timeend.text()
        log = []
        for i in dtme.split(' ')[0].split('.'):
            log.append(i)
        for k in dtme.split(' ')[1].split(':'):
            log.append(k)
        dtme = datetime(int(log[2]), int(log[1]), int(log[0]), int(log[3]), int(log[4]))
        Result(dtms, dtme, lines, unit, chart, erp)

class DirectoryChooseWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        if LoadSettings("1path") is None:
            self.btnl1 = QPushButton("Укажите папку")
        else:
            self.btnl1 = QPushButton(LoadSettings("1path"))
        self.btnl1.clicked.connect(self.btnl1_click)
        if LoadSettings("2path") is None:
            self.btnl2 = QPushButton("Укажите папку")
        else:
            self.btnl2 = QPushButton(LoadSettings("2path"))
        self.btnl2.clicked.connect(self.btnl2_click)
        if LoadSettings("3path") is None:
            self.btnl3 = QPushButton("Укажите папку")
        else:
            self.btnl3 = QPushButton(LoadSettings("3path"))
        self.btnl3.clicked.connect(self.btnl3_click)
        lbl1 = QLabel("Линия 1")
        lbl2 = QLabel("Линия 2")
        lbl3 = QLabel("Линия 3")
        btnok = QPushButton("OK")
        btnok.clicked.connect(self.ok_click)
        btncancel = QPushButton("Отмена")
        btncancel.clicked.connect(self.cancel_click)
        layout = QFormLayout()
        layout.addRow(lbl1, self.btnl1)
        layout.addRow(lbl2, self.btnl2)
        layout.addRow(lbl3, self.btnl3)
        layout.addRow(btnok, btncancel)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.setWindowTitle("")

    def btnl1_click(self):
        res = QFileDialog.getExistingDirectory(self)
        self.btnl1.setText(res)
        return

    def btnl2_click(self):
        res = QFileDialog.getExistingDirectory(self)
        self.btnl2.setText(res)
        return

    def btnl3_click(self):
        res = QFileDialog.getExistingDirectory(self)
        self.btnl3.setText(res)
        return

    def ok_click(self):
        if self.btnl1.text() != "Укажите папку":
            SaveSettings("1path", self.btnl1.text())
        else:
            SaveSettings("1path", None)
        if self.btnl2.text() != "Укажите папку":
            SaveSettings("2path", self.btnl2.text())
        else:
            SaveSettings("2path", None)
        if self.btnl3.text() != "Укажите папку":
            SaveSettings("3path", self.btnl3.text())
        else:
            SaveSettings("3path", None)
        self.close()
        window.btresult.setText("Готово")
        return

    def cancel_click(self):
        self.close()
        return

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()