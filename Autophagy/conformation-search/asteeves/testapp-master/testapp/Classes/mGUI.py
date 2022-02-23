#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
"""

import sys
from PyQt5.QtWidgets import QWidget, QMessageBox, QPushButton
from PyQt5.QtCore import QCoreApplication


class QuitWindow(QWidget):

    def __init__(self):
        super().__init__()
        
        self.initUI()

    def initUI(self):
        
        qbtn = QPushButton('Quit', self)
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(50, 50)       
        
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Quit button')    
        self.show()
        self.raise_()

    def closeEvent(self, event):
        
        reply = QMessageBox.question(self, 'Message',
                            "Are you sure to quit?",
                            QMessageBox.Yes | QMessageBox.No,
                            QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()         

