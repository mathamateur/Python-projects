import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QLabel,
                             QPushButton)

from Menu import Menu
from lessons.Center import Center


class Main(Center):
    def __init__(self):
        super().__init__()

        self.label_name = QLabel(self)
        self.label_name.setText("Chinese lessons")
        self.label_name.setFont(QFont('Arial', 60))
        self.label_name.adjustSize()
        self.label_name.move(50, 100)

        self.start_button = QPushButton(self)
        self.start_button.clicked.connect(self.start)
        self.start_button.setText("START")
        self.start_button.setFont(QFont('Arial', 40))
        self.start_button.adjustSize()
        self.start_button.move(280, 210)

    def start(self):
        self.menu = Menu(None, None)
        self.close()


app = QApplication(sys.argv)
w = Main()
w.show()
app.exec_()
