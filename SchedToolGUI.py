# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sched_tool.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from enum import Enum, IntEnum

class TskCols():
    Name = 0
    Period = 1
    Deadline = 2
    Execution = 3
    Priority = 4
    Wcrt = 0
    Lub = 1
    Rtt = 2

class Ui_SchedTestWindow(object):
    tblTaskSetHeads = ["Name", "Period", "Deadline", "Execution", "Priority"]
    tblSchedResHeads = ["WCRT", "LUB Test", "RT Test"]
    tblTaskSetColN = len(tblTaskSetHeads)
    tblSchedResColN = len(tblSchedResHeads)
 
    def setupUi(self, SchedTestWindow):
        SchedTestWindow.setObjectName("SchedTestWindow")
        SchedTestWindow.resize(821, 380)
        self.centralwidget = QtWidgets.QWidget(SchedTestWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pbSchedCal = QtWidgets.QPushButton(self.centralwidget)
        self.pbSchedCal.setGeometry(QtCore.QRect(490, 300, 161, 21))
        self.pbSchedCal.setObjectName("pbSchedCal")
        self.cbPD = QtWidgets.QCheckBox(self.centralwidget)
        self.cbPD.setGeometry(QtCore.QRect(180, 300, 61, 23))
        self.cbPD.setObjectName("cbPD")
        self.lblSchedulable = QtWidgets.QLabel(self.centralwidget)
        self.lblSchedulable.setGeometry(QtCore.QRect(660, 300, 91, 21))
        self.lblSchedulable.setObjectName("lblSchedulable")
        self.leSchedRes = QtWidgets.QLineEdit(self.centralwidget)
        self.leSchedRes.setGeometry(QtCore.QRect(760, 300, 51, 21))
        self.leSchedRes.setReadOnly(True)
        self.leSchedRes.setObjectName("leSchedRes")
        self.pbAddTask = QtWidgets.QPushButton(self.centralwidget)
        self.pbAddTask.setGeometry(QtCore.QRect(10, 300, 161, 21))
        self.pbAddTask.setObjectName("pbAddTask")
        self.pbClearAll = QtWidgets.QPushButton(self.centralwidget)
        self.pbClearAll.setGeometry(QtCore.QRect(350, 300, 131, 21))
        self.pbClearAll.setObjectName("pbClearAll")
        self.pbDelRow = QtWidgets.QPushButton(self.centralwidget)
        self.pbDelRow.setGeometry(QtCore.QRect(250, 300, 91, 21))
        self.pbDelRow.setObjectName("pbDelRow")
        self.tblTaskSet = QtWidgets.QTableWidget(self.centralwidget)
        self.tblTaskSet.setGeometry(QtCore.QRect(10, 10, 471, 281))
        self.tblTaskSet.setObjectName("tblTaskSet")
        self.tblTaskSet.setColumnCount(0)
        self.tblTaskSet.setRowCount(0)
        self.tblSchedRes = QtWidgets.QTableWidget(self.centralwidget)
        self.tblSchedRes.setGeometry(QtCore.QRect(490, 10, 321, 281))
        self.tblSchedRes.setObjectName("tblSchedRes")
        self.tblSchedRes.setColumnCount(0)
        self.tblSchedRes.setRowCount(0)
        SchedTestWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(SchedTestWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 821, 22))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        SchedTestWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(SchedTestWindow)
        self.statusbar.setObjectName("statusbar")
        SchedTestWindow.setStatusBar(self.statusbar)
        self.actionAbout = QtWidgets.QAction(SchedTestWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(SchedTestWindow)
        QtCore.QMetaObject.connectSlotsByName(SchedTestWindow)

    def retranslateUi(self, SchedTestWindow):
        _translate = QtCore.QCoreApplication.translate
        SchedTestWindow.setWindowTitle(_translate("SchedTestWindow", "Schedulability Test"))
        self.pbSchedCal.setText(_translate("SchedTestWindow", "Schedulability Test"))
        self.cbPD.setText(_translate("SchedTestWindow", "P=D?"))
        self.lblSchedulable.setText(_translate("SchedTestWindow", "Schedulable?"))
        self.pbAddTask.setText(_translate("SchedTestWindow", "Add Task"))
        self.pbClearAll.setText(_translate("SchedTestWindow", "Clear All"))
        self.pbDelRow.setText(_translate("SchedTestWindow", "Delete Row"))
        self.menuHelp.setTitle(_translate("SchedTestWindow", "Help"))
        self.actionAbout.setText(_translate("SchedTestWindow", "About"))

    def _initTables(self):
        self.tblRowCnt = 0
        self.tblTaskSet.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.tblTaskSet.setRowCount(self.tblRowCnt)
        self.tblTaskSet.setColumnCount(len(self.tblTaskSetHeads))
        self.tblTaskSet.setHorizontalHeaderLabels(self.tblTaskSetHeads)
        self.tblTaskSet.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.Stretch)

        self.tblSchedRes.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.tblSchedRes.setRowCount(self.tblRowCnt)
        self.tblSchedRes.setColumnCount(len(self.tblSchedResHeads))
        self.tblSchedRes.setHorizontalHeaderLabels(self.tblSchedResHeads)
        self.tblSchedRes.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.Stretch)
        self.pbClearAll.setEnabled(False)
        self.pbDelRow.setEnabled(False)

        self.tblTaskSet.clicked.connect(lambda: self.tblItemSelect(0))
        self.tblSchedRes.clicked.connect(lambda: self.tblItemSelect(1))

        

    def tblItemSelect(self, select):
        if select == 0:
            curRow = self.tblTaskSet.currentRow()
            self.tblSchedRes.selectRow(curRow)
        else:
            curRow = self.tblSchedRes.currentRow()
            self.tblTaskSet.selectRow(curRow)

def CritMsgBox(text,detailed_text):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText(text)
    msg.setDetailedText(detailed_text)
    msg.exec_()

def InfoMsgBox(text,detailed_text):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText(text)
    msg.setDetailedText(detailed_text)
    msg.exec_()