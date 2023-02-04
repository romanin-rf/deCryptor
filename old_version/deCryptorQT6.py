import sys
from style import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mainWindow = None
        self.setWindowTitle('deCryptor')
        self.setStyleSheet("background-color: #442a36;")
        self.move(300, 300)
        self.resize(650, 450)
        self.setFixedSize(650, 450)
        self.start_win()

    def start_win(self):
        wel = QLabel('Welcome To', self)
        wel.setFont(QFont('Arial', 18))
        wel.move(255, 40)
        wel.resize(580, 70)

        title = QLabel('deCryptor', self)
        title.setFont(QFont('Arial', 48))
        title.move(195, 110)
        title.resize(580, 60)

        but = QPushButton('Next', self)
        but.setGeometry(420, 585, 130, 60)
        but.clicked.connect(self.next_win)
        but.move(260, 250)
        but.setStyleSheet(pushButton_StyleSheet)
        but.setObjectName("Button")

    def next_win(self):
        win.close()
        self.mainWindow = MainWindow()
        self.mainWindow.show()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('deCryptor')
        self.setStyleSheet("background-color: #442a36;")
        self.move(300, 300)
        self.resize(650, 450)
        self.setFixedSize(650, 450)
        self.next_win = None
        self.fname = None
        self.main()

    def main(self):
        text = QLabel('Choice a File', self)
        text.setFont(QFont('Arial', 28))
        text.move(220, 60)
        text.resize(580, 70)

        self.fname = QLineEdit('Enter a file path...', self)
        self.fname.setStyleSheet(lineEdit_StyleSheet)
        self.fname.setObjectName("Line")
        self.fname.resize(310, 40)
        self.fname.move(100, 200)

        but = QPushButton('Brouse', self)
        but.resize(120, 40)
        but.clicked.connect(self.brouse)
        but.setStyleSheet(pushButton_StyleSheet)
        but.setObjectName("Button")
        but.move(430, 200)

        but1 = QPushButton('Next', self)
        but1.resize(120, 40)
        but1.clicked.connect(self.next)
        but1.setStyleSheet(pushButton_StyleSheet)
        but1.setObjectName("Button")
        but1.move(335, 300)

        but2 = QPushButton('Back', self)
        but2.resize(120, 40)
        but2.clicked.connect(self.back2start)
        but2.setStyleSheet(pushButton1_StyleSheet)
        but2.setObjectName("Button")
        but2.move(195, 300)
    
    def back2start(self): ...

    def next(self): 
        if self.fname.text() == '' or self.fname.text() == 'Enter a file path...':
            QMessageBox.warning(self, 'Warning', 'Please enter a file path')
        else:
            self.close()
            self.progress = ProgressWindow()
            self.progress.show()

    def brouse(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '/home')
        self.fname.setText(filename[0])



class ProgressWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Progress')
        self.setStyleSheet("background-color: #442a36;")
        self.move(925, 625)
        self.resize(300, 200)
        self.setFixedSize(300, 200)
        self.next_win = None
        self.progress()

    def progress(self):
        self.progress_bar = QProgressBar(self)

        for i in range(len(list(MainWindow.fname.text().iterdir()))):
            self.progress_bar.setValue(i/100)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # win = Window()
    # win.show()
    win = MainWindow()
    win.show()

    sys.exit(app.exec())