from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from DataBase import DataBase
from random import randint, shuffle, choice
from lessons.Center import Center


class Difficulty(Center):
    def __init__(self, menu, test):
        super().__init__()

        self.db = DataBase()
        self.nl = self.db.num_lessons
        self.menu = menu
        self.test = test
        self.que = QLabel(self)
        self.que.setText("SELECT THE DIFFICULTY")
        self.que.setFont(QFont('Arial', 40))
        self.que.adjustSize()
        self.que.move(50, 100)

        self.labels = ["EASY", "MEDIUM", "HARD"]
        self.pos = [10, 240, 470]
        self.buttons = [QPushButton(l, self) for l in self.labels]
        [b.clicked.connect(self.set_test) for b in self.buttons]
        [b.setFont(QFont('Arial', 30)) for b in self.buttons]
        [self.buttons[i].move(p, 210) for i, p in enumerate(self.pos)]
        [b.resize(220, 80) for b in self.buttons]

        self.show()

    def set_test(self):
        self.l_titles = set()
        self.l = []
        sender = self.sender()
        while len(self.l) < 20:
            n = randint(1, self.nl)
            if n not in self.l_titles:
                self.l_titles.add(n)
                lesson = self.db.get_lesson(f"lesson{n}")
                if sender.text() == "EASY":
                    lesson = lesson[:len(lesson) // 3]
                elif sender.text() == "MEDIUM":
                    lesson = lesson[len(lesson) // 3:len(lesson) * 2 // 3]
                else:
                    lesson = lesson[len(lesson) * 2 // 3:]
                self.l.extend(lesson)
        shuffle(self.l)
        if self.test is None:
            self.test = Test(self.l[:20], self.menu)
        else:
            self.test.set_task(self.l[:20])
            self.test.show()
        self.hide()


class Test(Center):
    def __init__(self, lesson, menu):
        super().__init__()

        self.menu = menu
        self.lesson = lesson
        self.ln = len(self.lesson)

        self.prog_bar = QProgressBar(self)
        self.prog_bar.setGeometry(150, 15, 400, 30)

        self.button_next = QPushButton("Next")
        self.button_next.clicked.connect(self.next_st)
        self.button_next.setFont(QFont('Arial', 30))

        self.button_prev = QPushButton("Back")
        self.button_prev.clicked.connect(self.prev_st)
        self.button_prev.setFont(QFont('Arial', 30))

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.button_prev)
        self.hbox.addWidget(self.button_next)

        self.button_sub = QPushButton("SUBMIT")
        self.button_sub.clicked.connect(self.submit)
        self.button_sub.setFont(QFont('Arial', 25))

        self.label_prob = QLabel()
        self.label_prob.setFont(QFont('Arial', 40))
        self.label_prob.setAlignment(Qt.AlignCenter)

        self.label_task = QLabel()
        self.label_task.setFont(QFont('Arial', 30))
        self.label_task.setAlignment(Qt.AlignCenter)

        self.line_ans = QLineEdit()
        self.line_ans.setFixedWidth(400)
        self.line_ans.setAlignment(Qt.AlignCenter)
        self.line_ans.setFont(QFont('Arial', 20))
        self.line_ans.setStyleSheet('background-color: peachpuff')

        self.label_reply = QLabel()
        self.label_reply.setFont(QFont('Arial', 30))

        self.button_chars = [QPushButton(self) for _ in range(4)]
        [b.clicked.connect(self.submit_char) for b in self.button_chars]
        [b.setFont(QFont('Arial', 35)) for b in self.button_chars]
        self.gbc = QGridLayout()
        for i in range(2):
            for j in range(2):
                n = 2 * i + j
                self.gbc.addWidget(self.button_chars[n], i, j)

        self.button_menu = QPushButton("Main menu", self)
        self.button_menu.clicked.connect(self.to_menu)
        self.button_menu.move(10, 10)

        self.button_fin = QPushButton("FINISH")
        self.button_fin.clicked.connect(self.finish)
        self.button_fin.setFont(QFont('Arial', 25))

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.label_prob)
        self.vbox.addWidget(self.label_task)
        self.vbox.addWidget(self.line_ans)
        self.vbox.addWidget(self.label_reply)
        self.vbox.addWidget(self.button_sub)
        self.vbox.addLayout(self.gbc)
        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.button_fin)
        self.vbox.setContentsMargins(150, 60, 150, 15)

        self.setLayout(self.vbox)

        self.set_task(self.lesson)
        self.show()

    def set_task(self, lesson):
        self.lesson = lesson

        self.forms = [self.set_form1, self.set_form2]
        self.ffs = [self.forms[randint(0, 1)] for _ in range(20)]
        self.steps = [""] * 20
        self.cur_s = -1
        self.len_s = self.ln - 1
        self.res = 0
        self.user_ans = [True] * 20

        self.prog_bar.setValue(0)
        self.prog_bar.setRange(0, self.ln - 1)

        self.line_ans.hide()

        self.button_prev.hide()

        self.button_sub.hide()

        self.label_reply.hide()

        self.next_st()

    def update_pp(self):
        self.prog_bar.setValue(self.cur_s)

    @staticmethod
    def update_l(label, text):
        label.setText(text)
        label.adjustSize()
        label.show()

    def set_form1(self):
        self.update_l(self.label_prob, self.lesson[self.cur_s][2])
        self.update_l(self.label_task, "Enter meaning:")
        self.line_ans.clear()
        if self.user_ans[self.cur_s]:
            self.line_ans.show()
            self.button_sub.show()
            self.label_reply.hide()
        else:
            self.label_reply.setText(self.steps[self.cur_s])
            self.label_reply.show()
            self.button_sub.hide()
            self.line_ans.hide()
        self.cor_char = self.lesson[self.cur_s][3]
        [b.hide() for b in self.button_chars]

    def set_form2(self):
        self.update_l(self.label_prob, self.lesson[self.cur_s][3])
        self.update_l(self.label_task, "Select a correct character:")
        self.cor_char = self.lesson[self.cur_s][2]
        if self.user_ans[self.cur_s]:
            chars = [self.cor_char]
            while len(chars) < 4:
                char = choice(self.lesson)[2]
                if char not in chars:
                    chars.append(char)
            shuffle(chars)
            [b.setText(c) for c, b in zip(chars, self.button_chars)]
            [b.show() for b in self.button_chars]
            self.label_reply.hide()
        else:
            self.label_reply.setText(self.steps[self.cur_s])
            self.label_reply.show()
        self.line_ans.hide()
        self.button_sub.hide()

    def check_button(self):
        if self.cur_s <= 0:
            self.button_prev.hide()
        elif self.cur_s == self.len_s - 1:
            self.button_next.hide()
        else:
            self.button_prev.show()
            self.button_next.show()

    def new_step(self):
        self.check_button()
        self.ffs[self.cur_s]()
        self.update_pp()

    def to_menu(self):
        self.menu.show()
        self.hide()

    def submit(self):
        if self.cor_char.lower() == self.line_ans.text().lower():
            self.res += 1
            self.user_ans[self.cur_s] = False
            self.label_reply.setText("Correct!")
        else:
            self.label_reply.setText("Wrong!")
        self.button_sub.hide()
        self.line_ans.hide()
        self.steps[self.cur_s] = self.label_reply.text()
        self.label_reply.show()

    def next_st(self):
        self.cur_s += 1
        self.new_step()

    def prev_st(self):
        self.cur_s -= 1
        self.new_step()

    def submit_char(self):
        sender = self.sender()
        if sender.text() == self.cor_char:
            self.res += 1
            self.user_ans[self.cur_s] = False
            self.label_reply.setText("Correct!")
        else:
            self.label_reply.setText("Wrong!")
        [b.hide() for b in self.button_chars]
        self.steps[self.cur_s] = self.label_reply.text()
        self.label_reply.show()

    def finish(self):
        rep = "You need more practice"
        if 0.6 <= self.res / self.ln < 0.75:
            rep = "Satisfied"
        elif 0.75 <= self.res / self.ln < 0.9:
            rep = "Well done!\nBut you might be better"
        elif self.res / self.ln >= 0.9:
            rep = "Excellent!\nIs Chinese your native language?"
        msg = QMessageBox()
        msg.setWindowTitle("Result")
        msg.setText(f"Your result is {self.res}/20\n{rep}")
        msg.exec_()
        self.to_menu()
