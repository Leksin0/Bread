from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QFormLayout, QGroupBox
from PyQt6.QtWidgets import QPushButton, QLabel, QFileDialog, QCheckBox, QDateTimeEdit, QVBoxLayout
from PyQt6.QtCore import QSize
import sys
import fileops
import datetime

#fixedsize ???

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dirwindow = None

        chdir = QPushButton()
        chdir.clicked.connect(self.chdir_click)

        self.cbl1 = QCheckBox("Линия 1")
        self.cbl2 = QCheckBox("Линия 2")
        self.cbl3 = QCheckBox("Линия 3")
        lineselect = QGroupBox()
        h = QVBoxLayout()
        h.addWidget(self.cbl1)
        h.addWidget(self.cbl2)
        h.addWidget(self.cbl3)
        lineselect.setLayout(h)
        lineselect.setAlignment(1)# align left

        lbts = QLabel("Начало периода")
        lbts.setAlignment(1)
        lbte = QLabel("Конец периода")
        lbte.setAlignment(1)
        self.timestart = QDateTimeEdit(datetime.datetime.now())
        self.timestart.setAlignment(2)
        self.timeend = QDateTimeEdit(datetime.datetime.now())
        self.timeend.setAlignment(2)

        btresult = QPushButton("Сохранить")
        btresult.clicked.connect(self.GetResult)
        btchdir = QPushButton("Изменить папку логов")
        btchdir.clicked.connect(self.chdir_click)

        layout = QFormLayout()
        layout.addRow(lbts, self.timestart)
        layout.addRow(lbte, self.timeend)
        layout.addWidget(lineselect)
        layout.addRow(btresult, btchdir)

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


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
