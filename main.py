from fileops import *
from ui import MainWindow
from multiprocessing import pool, process, queues

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()