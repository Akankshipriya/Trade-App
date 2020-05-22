from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit,QDialog,QTableWidgetItem
import datetime
import pandas as pd
import sys
import MaPlots
import EmaPlots
import Values
import PriceChart
import scraper
import s1Ts
import s1Port
import s2Ts
import s2Port
import date_value_check

start = None 
techa = None
funa = None 
rst = None
ts = None
al = None

tableui = None


class Start(QDialog,QMainWindow):
    def __init__(self):
        super(Start, self).__init__()
        uic.loadUi("start.ui", self)
        self.show()
        self.btn_ta.clicked.connect(self.clickedta)
        self.btn_fa.clicked.connect(self.clickedfa)
        self.btn_ts.clicked.connect(self.clickedts)
        self.btn_exit.clicked.connect(self.clickedExit)

    def clickedta(self):
        self.accept()
        techa.show()

    def clickedfa(self):
        self.accept()
        funa.show()

    def clickedts(self):
        self.accept()
        ts.show()

    def clickedExit(self):
        self.close()


class techA(QDialog,QMainWindow):
    def __init__(self):
        super(techA, self).__init__()
        uic.loadUi("techa.ui", self)
        
        self.comboBox.currentIndexChanged.connect(self.pressed)
        
        self.btn_view.clicked.connect(self.clickedTabView)

        self.btn_ma.clicked.connect(self.clickedMaPlot)
        self.btn_ema.clicked.connect(self.clickedEmaPlot)
        self.btn_rsi.clicked.connect(self.clickedRsiPlot)
        self.btn_cc.clicked.connect(self.clickedCcPlot)

        self.btn_bk.clicked.connect(self.clickedBack)

    def pressed(self):
        sel = self.comboBox.currentText()
        if sel == 'Simple Moving Average':
            self.btn_sub.clicked.connect(self.smaVal)

        elif sel == 'Exponential Moving Average':
            self.btn_sub.clicked.connect(self.emaVal)

        elif sel == 'Resistance Strength Index':
            self.btn_sub.clicked.connect(self.RSIVal)



    def clickedTabView(self):
        tableui.show()

    def clickedBack(self):
        self.accept()
        start.show()
        self.close()


    def clickedMaPlot(self):
        st = self.le_st.text()
        ed = self.le_ed.text()
        cur = self.le_currency.text()
        dp = self.le_dp.text()
        dp2 = self.le_dp2.text()
        if date_value_check.date_check(st) or date_value_check.date_check(ed):
            dtal.show()
        elif date_value_check.value_check(dp,dp2):
            al.show()
        else:
            MaPlots.smaPlot(st,ed,cur,dp,dp2) # ret returned

    def clickedEmaPlot(self):
        st = self.le_st.text()
        ed = self.le_ed.text()
        cur = self.le_currency.text()
        dp = self.le_dp.text()
        dp2 = self.le_dp2.text()
        if date_value_check.date_check(st) or date_value_check.date_check(ed):
            dtal.show()
        elif date_value_check.value_check(dp,dp2):
            al.show()
        else:
            EmaPlots.emaPlot(st,ed,cur,dp,dp2) # ret returned

    def clickedRsiPlot(self):
        st = self.le_st.text()
        ed = self.le_ed.text()
        cur = self.le_currency.text()
        dp = self.le_dp.text()
        dp2 = self.le_dp2.text()
        if date_value_check.date_check(st) or date_value_check.date_check(ed):
            dtal.show()
        elif date_value_check.value_check2(dp):
            al.show()
        else:
            Values.plotRSI(st,ed,cur,dp) # ret returned

    def clickedCcPlot(self):
        st = self.le_st.text()
        ed = self.le_ed.text()
        cur = self.le_currency.text()
        if date_value_check.date_check(st) or date_value_check.date_check(ed):
            dtal.show()
        else:
            PriceChart.plotPrice(st,ed,cur)
        



    def smaVal(self):
        tableui.tw_val.setHorizontalHeaderLabels(['Date','Currency Price','SMA'])
        st = self.le_st.text()
        ed = self.le_ed.text()
        cur = self.le_currency.text()
        dp = self.le_dp.text()
        if date_value_check.date_check(st) or date_value_check.date_check(ed):
            dtal.show()
        elif date_value_check.value_check2(dp):
            al.show()
        else:    
            tableui.tw_val.setRowCount(0)
            val = Values.getSMA(st,ed,cur,dp) # ret returned
            size = val.shape[0]
            for i in range(size):
                rowPosition = tableui.tw_val.rowCount()
                tableui.tw_val.insertRow(rowPosition)
                tableui.tw_val.setItem(rowPosition, 0, QTableWidgetItem(str(val['Date'][i])))
                tableui.tw_val.setItem(rowPosition, 1, QTableWidgetItem(str(val['Currency Price'][i])))
                tableui.tw_val.setItem(rowPosition, 2, QTableWidgetItem(str(val['SMA'][i])))

    def emaVal(self):
        tableui.tw_val.setHorizontalHeaderLabels(['Date','Currency Price','EMA'])
        st = self.le_st.text()
        ed = self.le_ed.text()
        cur = self.le_currency.text()
        dp = self.le_dp.text()
        if date_value_check.date_check(st) or date_value_check.date_check(ed):
            dtal.show()
        elif date_value_check.value_check2(dp):
            al.show()
        else:   
            tableui.tw_val.setRowCount(0)
            val = Values.getEMA(st,ed,cur,dp) # ret returned
            size = val.shape[0]
            for i in range(size):
                rowPosition = tableui.tw_val.rowCount()
                tableui.tw_val.insertRow(rowPosition)
                tableui.tw_val.setItem(rowPosition, 0, QTableWidgetItem(str(val['Date'][i])))
                tableui.tw_val.setItem(rowPosition, 1, QTableWidgetItem(str(val['Currency Price'][i])))
                tableui.tw_val.setItem(rowPosition, 2, QTableWidgetItem(str(val['EMA'][i])))

        
    def RSIVal(self):
        tableui.tw_val.setHorizontalHeaderLabels(['Date','Currency Price','RSI'])
        st = self.le_st.text()
        ed = self.le_ed.text()
        cur = self.le_currency.text()
        dp = self.le_dp.text()
        if date_value_check.date_check(st) or date_value_check.date_check(ed):
            dtal.show()
        elif date_value_check.value_check2(dp):
            al.show()
        else: 
            tableui.tw_val.setRowCount(0)
            val = Values.getRSI(st,ed,cur,dp)
            val.fillna(0,inplace=True)  
            size = val.shape[0]

            for i in range(size):
                rowPosition = tableui.tw_val.rowCount()
                tableui.tw_val.insertRow(rowPosition)
                tableui.tw_val.setItem(rowPosition, 0, QTableWidgetItem(str(val['Date'][i])))
                tableui.tw_val.setItem(rowPosition, 1, QTableWidgetItem(str(val['Currency Price'][i])))
                tableui.tw_val.setItem(rowPosition, 2, QTableWidgetItem(str(val['RSI'][i])))

        

        
class TableUI(QDialog):
    def __init__(self):
        super(TableUI, self).__init__()
        uic.loadUi("table.ui", self)
        
        
        self.btn_back.clicked.connect(self.clickedBack)

    def clickedBack(self):
        techa.show()
        tableui.close()

#Fundemental Analysis Scraper




class funA(QDialog):
    def __init__(self):
        super(funA, self).__init__()
        uic.loadUi("funa.ui", self)
        self.btn_scrap.clicked.connect(self.scrap)
        self.btn_bk.clicked.connect(self.clickedBack2)

    def clickedBack2(self):
        self.accept()
        start.show()
        self.close()



    def scrap(self):
        keyCur = self.le_nc.text()
        print(keyCur)
        keyData = scraper.start(keyCur)
        rst.tableWidget.setRowCount(0)

        size = len(keyData)

        for i in range(size):
            rowPosition = rst.tableWidget.rowCount()
            rst.tableWidget.insertRow(rowPosition) #insert row at row position
            rst.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(str(keyData[i]['title'])))
            rst.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(str(keyData[i]['url'])))
            rst.tableWidget.setItem(rowPosition, 2, QTableWidgetItem(str(keyData[i]['date'])))

        rst.exec()
        

class rsT(QDialog):
        
    def __init__(self):
        super(rsT, self).__init__()
        uic.loadUi("rst.ui", self)
        
             
class TS(QDialog):
    def __init__(self):
        super(TS, self).__init__()
        uic.loadUi("ts.ui", self)
        self.btn_sig1.clicked.connect(self.clickedS1ts)
        self.btn_port1.clicked.connect(self.clickedS1port)
        self.btn_sig2.clicked.connect(self.clickedS2ts)
        self.btn_port2.clicked.connect(self.clickedS2port)
        
        self.btn_bk.clicked.connect(self.clickedBack)

    def clickedS1ts(self):
        st = self.le_st.text()
        ed = self.le_ed.text()
        shortMa = self.dp1.text()
        longMa = self.dp2.text()
        
        if date_value_check.date_check(st) or date_value_check.date_check(ed):
            dtal.show()
        elif date_value_check.value_check(shortMa,longMa):
            al.show()
        else:
            s1Ts.plotTSs1(st,ed,shortMa,longMa)

              
    def clickedS1port(self):

        st = self.le_st.text()
        ed = self.le_ed.text()
        shortMa = self.dp1.text()
        longMa = self.dp2.text()
        if date_value_check.date_check(st) or date_value_check.date_check(ed):
            dtal.show()
        elif date_value_check.value_check(shortMa,longMa):
            al.show()
        else:
            s1Port.plotPorts1(st,ed,shortMa,longMa)

    def clickedS2ts(self):
        st = self.le_st.text()
        ed = self.le_ed.text()
        if date_value_check.date_check(st) or date_value_check.date_check(ed):
            dtal.show()
        else:
            s2Ts.plotTsS2(st,ed)


    def clickedS2port(self):
        st = self.le_st.text()
        ed = self.le_ed.text()
        if date_value_check.date_check(st) or date_value_check.date_check(ed):
            dtal.show()
        else:
            s2Port.plotPorts2(st,ed)
    def clickedBack(self):
        start.show()
        self.close()

class alert(QDialog):
    def __init__(self):
        super(alert, self).__init__()
        uic.loadUi("alert.ui", self)
        self.btn_ok.clicked.connect(self.clickedOk)


    def clickedOk(self):
        self.close()


class date_alert(QDialog):
    def __init__(self):
        super(date_alert, self).__init__()
        uic.loadUi("date_alert.ui", self)
        self.btn_ok.clicked.connect(self.clickedOk)


    def clickedOk(self):
        self.close()



app = QApplication(sys.argv)


dtal= date_alert()
start = Start()
rst = rsT()
funa = funA()
ts = TS ()
al = alert()
techa = techA()
funa = funA()
tableui = TableUI()
app.exec_()