try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *


class TruemaxExportWidg(QGroupBox):
    """Object which is put into the State Manager.
    """

    def __init__(self, core, parent):
        super(TruemaxExportWidg, self).__init__(parent)

        layout = QHBoxLayout(self)
        self.setLayout(layout)
        self.substance_button = QPushButton("Substance", self)
        self.substance_button.setGeometry(QRect(10, 10, 75, 23))
        self.substance_button.setToolTip("Export Substance ready file.")
        layout.addWidget(self.substance_button)
        self.anim_button = QPushButton("Anim", self)
        self.anim_button.setGeometry(QRect(100, 10, 75, 23))
        self.anim_button.setToolTip("Export animation.")
        layout.addWidget(self.anim_button)
