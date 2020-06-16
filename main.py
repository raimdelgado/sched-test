import sys
from PyQt5 import QtWidgets, uic
from SchedToolGUI import *
from RtTasks import *

class MainWindow(QtWidgets.QMainWindow, Ui_SchedTestWindow):
    tblRowCnt = int()

    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._initState()

    def _initState(self):
        self._initPushButtons()
        self._initTables()

        # checkbox toggle callback
        self.cbPD.toggled.connect(self.cbPDCB)

    def _getRowCnt(self):
        return self.tblRowCnt

    def _initPushButtons(self):
        self.pbSchedCal.setEnabled(False)
        
        # connect callbacks
        self.pbAddTask.clicked.connect(self.pbAddTaskCB)
        self.pbClearAll.clicked.connect(self.pbClearAllCB)
        self.pbDelRow.clicked.connect(self.pbDelRowCB)
        self.pbSchedCal.clicked.connect(self.pbSchedCalCB)

    ## Callbacks ##
    def pbAddTaskCB(self):
        self.tblRowCnt += 1
        self.tblSchedRes.setRowCount(self.tblRowCnt)
        self.tblTaskSet.setRowCount(self.tblRowCnt)

        for i in range(self.tblTaskSetColN):
            self.setTaskItem(self.tblRowCnt-1,i,"")
            
        if self.pbClearAll.isEnabled() is False and self.pbDelRow.isEnabled() is False:
            self.pbClearAll.setEnabled(True)
            self.pbDelRow.setEnabled(True)
            self.pbSchedCal.setEnabled(True)

    def pbClearAllCB(self):
        self._initTables()

    def pbDelRowCB(self):
        self.tblTaskSet.removeRow(self.tblTaskSet.currentRow())
        self.tblSchedRes.removeRow(self.tblSchedRes.currentRow())
        self.tblRowCnt -= 1

    def pbSchedCalCB(self):        
        if self.checkCellSanity() & 1:
            pass
        else:
            tasks = [RtTask(0,0,0) for i in range(self.tblRowCnt)] # create list of dummy RtTask
            taskset = RtTaskset() 

            for i, task in enumerate(tasks):
                name, prd = self.getTaskItem(i,TskCols.Name), self.getTaskItem(i,TskCols.Period)
                ddline, exc  = self.getTaskItem(i,TskCols.Deadline), self.getTaskItem(i,TskCols.Execution)
                prio = self.getTaskItem(i,TskCols.Priority)
                task.__init__(prd,exc,prio,name,ddline)
                taskset.add_rt_task(task)

            LUBTest(taskset)
            rtt_issched = RTTest(taskset)

            taskset_issched = "yes" if rtt_issched is True else "no"
            self.leSchedRes.setText(taskset_issched)

            for i, task in enumerate(tasks):
                self.setResItem(i,TskCols.Wcrt,str(task.wcrt))
                self.setResItem(i,TskCols.Lub,str(task.lub_issched))
                self.setResItem(i,TskCols.Rtt,str(task.rtt_issched))

    def getTaskItem(self, r, c):
        return self.tblTaskSet.item(r,c).text()

    def setTaskItem(self, r, c, item):
        self.tblTaskSet.setItem(r,c, QtWidgets.QTableWidgetItem(item))

    def setResItem(self, r, c, item):
        items = QtWidgets.QTableWidgetItem(item)
        items.setFlags(items.flags() ^ QtCore.Qt.ItemIsEditable)
        self.tblSchedRes.setItem(r,c, items)

    def checkCellSanity(self):
        misses = 0
        for i in range(self.tblRowCnt):
            if self.getTaskItem(i,TskCols.Period) == "" or self.getTaskItem(i,TskCols.Execution) == "" or self.getTaskItem(i,TskCols.Priority) == "":
                misses += 1
            if self.tblTaskSet.item(i,TskCols.Name).text() == "" or self.tblTaskSet.item(i,TskCols.Deadline).text() == "":
                misses += 2
        if misses & 1:
            CritMsgBox("Missing either Period, Execution, or Priority","Check row contents or delete unused rows!")
        if misses & 2 :
            InfoMsgBox("Name or Deadline is missing","If Name is blank, the tasks will be set to default. In case of deadline, deadline = period")
        return misses
            
    def cbPDCB(self):
        for i in range(self.tblRowCnt):
            period = self.getTaskItem(i,TskCols.Period) if self.cbPD.isChecked() else ""
            self.setTaskItem(i,TskCols.Deadline,period)

## Main ##
###################################################################################
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    GUI = MainWindow()    
    GUI.show()
    app.exec()

    # print(TaskCols.Name)

# directly load the .ui (should use absolute path)
#### app = QtWidgets.QApplication(sys.argv)
#### window = uic.loadUi("/home/raim/sample_gui/sample_window.ui")
#### window.show()
#### app.exec()