from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt


class StatusBar(QFrame):
    def __init__(self):
        super().__init__()

        self.setFixedHeight(60)

        self.layout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout.setContentsMargins(25, 5, 25, 5)

        self.title_label = QLabel("Главная")

        self.layout.addWidget(self.title_label)

    def set_title(self, title):
        self.title_label.setText(title)
