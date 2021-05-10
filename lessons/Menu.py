from Lesson import Lesson
from Test import Difficulty
from PyQt5.QtWidgets import (QPushButton, QVBoxLayout, QHBoxLayout,
                             QLabel)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from lessons.Center import Center


class Menu(Center):
    def __init__(self, lesson, diff):
        super().__init__()
        self.lesson = lesson
        self.diff = diff
        self.learn_button = QPushButton("LEARN")
        self.learn_button.setFont(QFont('Arial', 30))
        self.learn_button.clicked.connect(self.learn)

        self.test_button = QPushButton("TEST")
        self.test_button.setFont(QFont('Arial', 30))
        self.test_button.clicked.connect(self.test)

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.learn_button)
        self.hbox.addWidget(self.test_button)

        self.que = QLabel("What do you want?")
        self.que.setFont(QFont('Arial', 40))
        self.que.setAlignment(Qt.AlignCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.que)
        self.vbox.addLayout(self.hbox)
        self.vbox.setContentsMargins(150, 0, 150, 15)

        self.setLayout(self.vbox)
        self.show()

    def learn(self):
        if self.lesson is None:
            self.lesson = Lesson(self)
        else:
            self.lesson.go()
            self.lesson.show()
        self.hide()

    def test(self):
        if self.diff is None:
            self.diff = Difficulty(self, None)
        else:
            self.diff.show()
        self.hide()
