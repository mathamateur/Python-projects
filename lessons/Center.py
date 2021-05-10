from PyQt5.QtWidgets import QDesktopWidget, QWidget


class Center(QWidget):
    def __init__(self):
        super().__init__()
        framegm = self.frameGeometry()
        centerpoint = QDesktopWidget().availableGeometry().center()
        framegm.moveCenter(centerpoint)
        self.move(framegm.topLeft())
        self.resize(700, 500)
        self.setWindowTitle('Chinese lessons')
        self.setStyleSheet('background-color: lightcoral')