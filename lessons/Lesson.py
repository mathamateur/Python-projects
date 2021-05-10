from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from DataBase import DataBase
from lessons.Center import Center


class Lesson(Center):
    def __init__(self, menu):

        super().__init__()
        self.menu = menu
        self.db = DataBase()
        self.num_lessons = self.db.num_lessons

        self.character = QLabel()
        self.character.setFont(QFont('Arial', 120))
        self.character.setAlignment(Qt.AlignCenter)

        self.about = QLabel()
        self.about.setFont(QFont('Arial', 30))
        self.about.setAlignment(Qt.AlignCenter)

        self.progress = QLabel()
        self.progress.setFont(QFont('Arial', 20))
        self.progress.setAlignment(Qt.AlignCenter)

        self.button_next = QPushButton("Next")
        self.button_next.clicked.connect(self.next_ch)
        self.button_next.setFont(QFont('Arial', 30))

        self.button_prev = QPushButton("Back")
        self.button_prev.clicked.connect(self.prev_ch)
        self.button_prev.setFont(QFont('Arial', 30))

        self.buttons = QHBoxLayout()
        self.buttons.addWidget(self.button_prev)
        self.buttons.addWidget(self.button_next)
        self.buttons.setContentsMargins(120, 0, 150, 0)

        self.les_list = QComboBox()
        self.les_list.setStyleSheet('background-color: peachpuff')
        self.les_labels = [f'Lesson{i + 1}' for i in range(self.num_lessons)]
        self.les_list.addItems(self.les_labels)

        self.button_go = QPushButton("GO")
        self.button_go.clicked.connect(self.go)

        self.button_menu = QPushButton("Main menu")
        self.button_menu.clicked.connect(self.to_menu)

        self.lwb = QGridLayout()
        self.lwb.addWidget(self.les_list, 0, 0)
        self.lwb.addWidget(self.button_go, 0, 1)
        self.lwb.addWidget(self.button_menu, 1, 1)

        self.grid = QGridLayout()
        self.grid.addLayout(self.lwb, 0, 0)
        self.grid.addWidget(self.progress, 0, 2)
        self.grid.addWidget(self.character, 1, 1)
        self.grid.addWidget(self.about, 2, 1)
        self.grid.addLayout(self.buttons, 3, 1)

        self.setLayout(self.grid)

        self.go()
        self.show()

    @staticmethod
    def update_l(label, text):
        label.setText(text)
        label.adjustSize()

    def check_button(self):
        if self.cur_l <= 0:
            self.button_prev.hide()
        elif self.cur_l == self.len_l - 1:
            self.button_next.hide()
        else:
            self.button_prev.show()
            self.button_next.show()

    def new_lesson(self):
        self.check_button()
        self.update_l(self.character, self.lesson[self.cur_l][2])
        self.update_l(self.about, self.lesson[self.cur_l][3])
        self.txt = self.progress.text().split('\n')[0]
        self.s = f'{self.txt}\n{self.cur_l + 1}/{self.len_l}'
        self.update_l(self.progress, self.s)

    def next_ch(self):
        self.cur_l += 1
        self.new_lesson()

    def prev_ch(self):
        self.cur_l -= 1
        self.new_lesson()

    def go(self):
        self.lesson = self.db.get_lesson(self.les_list.currentText().lower())
        self.progress.setText(self.les_list.currentText().lower().capitalize())
        self.button_prev.hide()
        self.cur_l = -1
        self.len_l = len(self.lesson)

        self.next_ch()

    def to_menu(self):
        self.menu.show()
        self.hide()
