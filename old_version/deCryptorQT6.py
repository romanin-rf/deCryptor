import sys
import os
import time
from style import *
from PyQt6.QtGui import *
import deCryptorLib
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
        wel.setFont(QFont('Montserrat', 18))
        wel.setStyleSheet("color: #f4f9f1")
        wel.move(255, 40)
        wel.resize(580, 70)

        title = QLabel('deCryptor', self)
        title.setFont(QFont('Montserrat', 48))
        title.setStyleSheet("color: #f4f9f1")
        title.move(195, 110)
        title.resize(580, 75)

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
        text.setFont(QFont('Montserrat', 28))
        text.setStyleSheet("color: #f4f9f1")
        text.move(220, 60)
        text.resize(580, 70)

        self.fname = QLineEdit('Enter a file path...', self)
        self.fname.setStyleSheet(lineEdit_StyleSheet)
        self.fname.setObjectName("Line")
        self.fname.resize(310, 40)
        self.fname.move(100, 200)

        mode = QRadioButton('File', self)
        mode.setChecked(True)
        mode.move(220, 150)

        mode1 = QRadioButton('Directory', self)
        mode1.move(370, 150)

        but = QPushButton('Browse', self)
        but.resize(120, 40)
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

        if mode:
            but.clicked.connect(self.browse_file)
        elif mode1:
            but.clicked.connect(self.browse_directory)
        else:
            QMessageBox.warning(self, "Warning", "Choose what exactly you want to work with: file or directory?")

    def browse_directory(self):
        global filename
        filename = QFileDialog.getExistingDirectory(self, 'Open File', '/home')
        self.fname.setText(filename)

    def browse_file(self):
        global filename
        filename = QFileDialog.getOpenFileName(self, 'Open File', '/home')
        self.fname.setText(filename[0])

    def back2start(self):
        self.close()
        window = Window()
        window.show()

    def next(self):
        if self.fname.text() == '' or self.fname.text() == 'Enter a file path...':
            QMessageBox.warning(self, 'Warning', 'Please enter a file path')
        else:
            self.next_win = ModeWindow()
            self.next_win.show()


class ModeWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('deCryptor')
        self.setStyleSheet("background-color: #442a36;")
        self.move(300, 300)
        self.resize(650, 450)
        self.setFixedSize(650, 450)
        self.Decryptor = deCryptorLib.deCryptor()
        self.key_path = os.getcwd()
        self.path2key = None
        self.but = None
        self.but1 = None
        self.main_mode()

    def encoding(self):
        """Шифровать"""
        pprint(self.DeCryptor.encode_file(filename, key_path))

    def decoding(self):
        pprint(self.DeCryptor.decode_file(filename, path2key))

    def main_mode(self):
        text = QLabel('Choose a operation', self)
        text.setFont(QFont('Montserrat', 28))
        text.setStyleSheet("color: #f4f9f1")
        text.move(170, 120)
        text.resize(580, 70)

        self.but = QPushButton('Decode', self)
        self.but.resize(120, 40)
        self.but.clicked.connect(self.decoding)
        self.but.setStyleSheet(pushButton_StyleSheet)
        self.but.setObjectName("Button")
        self.but.move(180, 300)

        self.but1 = QPushButton('Encode', self)
        self.but1.resize(120, 40)
        self.but1.clicked.connect(self.choose_key)
        self.but1.setStyleSheet(pushButton_StyleSheet)
        self.but1.setObjectName("Button")
        self.but1.move(360, 300)

    def choose_key(self):
        self.path2key = QLineEdit(self)
        self.path2key.setStyleSheet(lineEdit_StyleSheet)
        self.path2key.setObjectName("Line")
        self.path2key.resize(310, 40)
        self.path2key.move(120, 200)
        self.path2key.show()

        but2 = QPushButton('Browse', self)
        but2.resize(120, 40)
        but2.setStyleSheet(pushButton_StyleSheet)
        but2.setObjectName("Button")
        but2.move(440, 200)
        but2.show()
        but2.clicked.connect(self.browse_key)

    def browse_key(self):
        key = QFileDialog.getOpenFileName(None, 'Open File', '/home')
        self.path2key.setText(key[0])

        self.but.hide()
        self.but1.hide()

        nextbtn = QPushButton('Next', self)
        nextbtn.resize(120, 40)
        nextbtn.clicked.connect(self.encoding)
        nextbtn.setStyleSheet(pushButton_StyleSheet)
        nextbtn.setObjectName("Button")
        nextbtn.move(360, 300)
        nextbtn.show()

        backbtn = QPushButton('Back', self)
        backbtn.resize(120, 40)
        backbtn.clicked.connect(self.back)
        backbtn.setStyleSheet(pushButton1_StyleSheet)
        backbtn.setObjectName("Button")
        backbtn.move(180, 300)
        backbtn.show()

    def back(self): ...


class ProgressWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Progress')
        self.setStyleSheet("background-color: #442a36;")
        self.move(925, 625)
        self.resize(300, 200)
        self.setFixedSize(300, 200)
        self.next_win = None
        self.progress_bar = None
        self.progress()

    def progress(self):
        self.progress_bar = QProgressBar(self)
        for i in range(int(sum([len(files) for files in os.walk(r'{0}'.format(filename))]))):
            self.progress_bar.setValue(i)

        self.progress_bar.hide()

        text = QLabel('Successful!', self)
        text.setStyleSheet("color: #f4f9f1")
        text.move(200, 200)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    # win = MainWindow()
    # win = ModeWindow()
    win.show()
    sys.exit(app.exec())
