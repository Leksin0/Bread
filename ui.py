from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QGroupBox, QLayoutItem
from PyQt6.QtWidgets import QPushButton, QLabel, QFileDialog, QCheckBox, QDateTimeEdit, QVBoxLayout
from PyQt6.QtCore import QSize, Qt
import sys
import fileops
import datetime

#fixedsize ???

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dirwindow = None

        self.cbl1 = QCheckBox("Линия 1")
        self.cbl2 = QCheckBox("Линия 2")
        self.cbl3 = QCheckBox("Линия 3")
        lineselect = QGroupBox()
        h = QVBoxLayout()
        h.addWidget(self.cbl1)
        h.addWidget(self.cbl2)
        h.addWidget(self.cbl3)
        lineselect.setLayout(h)

        lbts = QLabel("Начало периода")
        lbte = QLabel("Конец периода")
        self.timestart = QDateTimeEdit(datetime.datetime.now())
        self.timeend = QDateTimeEdit(datetime.datetime.now())

        btresult = QPushButton("Сохранить")
        btresult.clicked.connect(self.GetResult)
        btchdir = QPushButton("Изменить папку логов")
        btchdir.clicked.connect(self.chdir_click)

        alnl = Qt.AlignmentFlag(1)
        alnr = Qt.AlignmentFlag(2)
        alnu = Qt.AlignmentFlag(0x20)
        alnp = Qt.AlignmentFlag(0x40)
        alnc = Qt.AlignmentFlag(4) and Qt.AlignmentFlag(0x80)

        layout = QGridLayout()
        layout.addWidget(lbts, 0, 0)
        layout.addWidget(lbte, 0, 2)
        layout.addWidget(self.timestart, 0, 1)
        layout.addWidget(self.timeend, 0, 3)
        layout.addWidget(lineselect, 1, 0)
        layout.addWidget(btresult, 3, 0)

        self.setWindowTitle("Статистика производства хлеба")
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def chdir_click(self):
        if self.dirwindow is None:
            self.dirwindow = DirectoryChooseWindow()
        self.dirwindow.show()

    def GetResult(self):
        lines = []
        if self.cbl1.isChecked():
            lines.append('1')
        if self.cbl2.isChecked():
            lines.append('2')
        if self.cbl3.isChecked():
            lines.append('3')
        #dtms =  TODO
        #fileops.Result(lines, dtms, dtme)


class DirectoryChooseWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        btnl1 = QPushButton("Выбрать папку линии 1")
        btnl1.clicked.connect(self.btnl1_click)
        self.lbl1 = QLabel("")
        btnl2 = QPushButton("Выбрать папку линии 2")
        btnl2.clicked.connect(self.btnl2_click)
        self.lbl2 = QLabel("")
        btnl3 = QPushButton("Выбрать папку линии 3")
        btnl3.clicked.connect(self.btnl3_click)
        self.lbl3 = QLabel("")

        btnok = QPushButton("OK")
        btnok.clicked.connect(self.ok_click)
        btncancel = QPushButton("Отмена")
        btncancel.clicked.connect(self.cancel_click)

        layout = QFormLayout()
        layout.addRow(btnl1, self.lbl1)
        layout.addRow(btnl2, self.lbl2)
        layout.addRow(btnl3, self.lbl3)
        layout.addRow(btnok, btncancel)
        #self.setLayout(layout)

        container = QWidget()
        container.setLayout(layout)
        container.setFixedSize(500, 300)
        self.setCentralWidget(container)
        self.setWindowTitle("ГДЕ ХЛЕБ ?!!??")

    def btnl1_click(self):
        res = QFileDialog.getExistingDirectory(self)
        self.lbl1.setText(res)
        return

    def btnl2_click(self):
        res = QFileDialog.getExistingDirectory(self)
        self.lbl2.setText(res)
        return

    def btnl3_click(self):
        res = QFileDialog.getExistingDirectory(self)
        self.lbl3.setText(res)
        return

    def ok_click(self):
        self.close()
        return

    def cancel_click(self):
        self.close()
        return

class WarnWindow(QMainWindow):
    msg = QLabel('Вы не указали расположение папок')
    l = QGridLayout
    l.addWidget(msg)