from fileops import *
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QGroupBox, QVBoxLayout, QFormLayout
from PyQt6.QtWidgets import QPushButton, QLabel, QFileDialog, QCheckBox, QDateTimeEdit, QRadioButton, QTextEdit



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dirwindow = None
        self.lbwait = QLabel("Пожалуйста, подождите")

        self.cbl1 = QCheckBox("Линия 1")
        self.cbl2 = QCheckBox("Линия 2")
        self.cbl3 = QCheckBox("Линия 3")
        linhelp = QVBoxLayout()
        linhelp.addWidget(self.cbl1)
        linhelp.addWidget(self.cbl2)
        linhelp.addWidget(self.cbl3)
        lineselect = QGroupBox("Линии")
        lineselect.setLayout(linhelp)

        self.rbu1 = QRadioButton("Час")
        self.rbu2 = QRadioButton("Сутки")
        self.rbu3 = QRadioButton("Неделя")
        self.rbu4 = QRadioButton("Месяц")
        unhelp = QVBoxLayout()
        unhelp.addWidget(self.rbu1)
        unhelp.addWidget(self.rbu2)
        unhelp.addWidget(self.rbu3)
        unhelp.addWidget(self.rbu4)
        unitselect = QGroupBox("Единица времени")
        unitselect.setLayout(unhelp)

        self.cbchart = QCheckBox("Добавить график")
        self.cberp = QCheckBox("Сравнить с нормативом")
        dophelp = QVBoxLayout()
        dophelp.addWidget(self.cbchart)
        dophelp.addWidget(self.cberp)
        addition = QGroupBox("Дополнительно")
        addition.setLayout(dophelp)

        lbts = QLabel("Начало периода")
        lbte = QLabel("Конец периода")
        self.timestart = QDateTimeEdit()
        self.timeend = QDateTimeEdit()

        self.btresult = QPushButton("Готово")
        self.btresult.clicked.connect(self.GetResult)#TODO              > > > H E R E < < <
        btchdir = QPushButton("Указать папку первичныых данных")
        btchdir.clicked.connect(self.chdir_click)#TODO              > > > H E R E < < <

        layout = QGridLayout()
        layout.addWidget(lbts, 0, 0)
        layout.addWidget(self.timestart, 0, 1)
        layout.addWidget(lbte, 1, 0)
        layout.addWidget(self.timeend, 1, 1)
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

    def GetResult(self):
        dirscorr = False
        while not dirscorr:
            if LoadSettings("1path") != None and LoadSettings("1path") != None and LoadSettings("1path") != None:
                dirscorr = True
            else:
                self.btresult.setText("Укажите папки первичных данных")
                return
        dtms = self.timestart.text()
        dtme = self.timeend.text()
        lines = []
        unit = ''
        chart = False
        erp = False
        if self.cbl1.isChecked():
            lines.append('1')
        if self.cbl2.isChecked():
            lines.append('2')
        if self.cbl3.isChecked():
            lines.append('3')
        else:
            pass
        if self.rbu1.isChecked():
            unit = 'h'
        elif self.rbu2.isChecked():
            unit = 'd'
        elif self.rbu3.isChecked():
            unit = 'w'
        elif self.rbu4.isChecked():
            unit = 'm'
        else:
            pass
        if self.cbchart.isChecked():
            chart = True
        if self.cberp:
            erp = True
        self.setCentralWidget(self.lbwait)
        Result(dtms, dtme, lines, unit, chart, erp)
        self.setCentralWidget(self.container)


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
        return

    def cancel_click(self):
        self.close()
        return


class ERPInput(QMainWindow):
    def __init__(self):
        super().__init__()

        self.rbu1 = QRadioButton("Час")
        self.rbu2 = QRadioButton("Сутки")
        self.rbu3 = QRadioButton("Месяц")
        self.rbu4 = QRadioButton("Год")
        unhelp = QVBoxLayout()
        unhelp.addWidget(self.rbu1)
        unhelp.addWidget(self.rbu2)
        unhelp.addWidget(self.rbu3)
        unhelp.addWidget(self.rbu4)
        unitselect = QGroupBox("Мера времени")
        unitselect.setLayout(unhelp)

        btnok = QPushButton("OK")
        btnok.clicked.connect(self.ok_click)
        btncancel = QPushButton("Отмена")
        btncancel.clicked.connect(self.cancel_click)

        layout = QFormLayout()
        layout.addRow(btnl1, self.lbl1)
        layout.addRow(btnl2, self.lbl2)
        layout.addRow(btnl3, self.lbl3)
        layout.addRow(btnok, btncancel)

        container = QWidget()
        container.setLayout(layout)
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