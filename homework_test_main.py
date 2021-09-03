import sys
import numpy as np
#from AD import read,setup
from homework import Ui_homework
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from matplotlib.figure import Figure 
from matplotlib.backends.backend_qt5agg import FigureCanvas
from PyQt5.QtGui import *
from sklearn.linear_model import LinearRegression

def LR_fit(x_hat):
    LR=LinearRegression()
    x=np.array([23.16,23.12,24.09,24.28,24.38,24.62,24.88,24.93,
                24.99,25.09,25.04,25.09,25.18,25.29,25.46,25.74,25.84,25.8,25.83]).reshape(-1,1)
    y=np.arange(0,95,5)
    LR.fit(x, y)
    y_out=LR.predict(x_hat)
    return y_out    


class function(QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui=Ui_homework()
        self.ui.setupUi(self)
        self.i=0
        self.x=np.empty(0)
        self.y=np.empty(0)
        self.value=0
        self.timer=QTime()
        self.__time_combobox()
        #figure create
        self.__fig=Figure()
        self.figCanvas=FigureCanvas(self.__fig)
        self.ui.tabWidget.addTab(self.figCanvas,'figure')
        self.ui.tabWidget.setCurrentWidget(self.figCanvas)
        self.__createFigure()  
        self.ui.spinbox_time.setValue(10)
        self.multiply_power_2=1
        self.ui.pbt_pause.setDisabled(True)
        self.header=['x','y']
        self.__table_view()
        self.__dial_initial()
        
        #setup(0x48)
        
    def __dial_initial(self):
        self.ui.dial.setNotchesVisible(True)
        self.ui.dial.valueChanged.connect(self.__lineEdit_show)

    def __time_combobox(self):
        items=['h','m','s']
        for i in items:
            self.ui.combobox_time.addItem(i)
        self.ui.combobox_time.setCurrentIndex(2)  
    #hand control
    @pyqtSlot()
    def on_pbt_hand_clicked(self):
        if self.ui.pbt_hand.isChecked():
            print('on')
        else:
            print('off')
    #value change        
    @pyqtSlot(str)      
    def on_combobox_time_currentIndexChanged(self,curText):
        global multiply_power_2
        if curText=='s':
            self.multiply_power_2=1
        elif curText=='m':
            self.multiply_power_2=60
        elif curText=='h':
            self.multiply_power_2=3600
        self.measure_time=self.value*self.multiply_power_2
    @pyqtSlot(float)
    def on_spinbox_time_valueChanged(self,value):
        self.measure_time=value*self.multiply_power_2
        self.value=value
    #create figure
    def __createFigure(self):
        self.axes=self.__fig.add_subplot(111)
        self.timer.start()
        self._timer=self.figCanvas.new_timer(1,callbacks=[(self.__draw, (), {})]) 
    def __draw(self):
        time=self.timer.elapsed()/100
        if time<=self.measure_time:
            print(time,self.measure_time)
            self.axes.cla()
            self.x=np.append(self.x,self.i)
            self.data=np.round(25*np.sin(self.i*2),3)#read(0)  
            self.y=np.append(self.y,self.data) 
            self.__lineEdit_show()
            
            # Shift the sinusoid as a function of time.
            if self.i<100:
                self.axes.plot(self.x,self.y,color='red')
            else:
                self.axes.plot(self.x[self.i-100:self.i],self.y[self.i-100:self.i],color='red')
            self.axes.set_xlabel('t')
            self.axes.set_ylabel('degree')
            self.axes.grid()
            self.__do_curChanged()
            self.axes.figure.canvas.draw()
            self.axes.figure.canvas.flush_events() 
        else:
            self.__stop()
        
    def __lineEdit_show(self):
        predict_data=LR_fit([[self.data]])
        for i in np.nditer(predict_data):
            self.ui.lineEdit.setText(str(i.round(3)))
            self.ui.dial.setValue(i+800)
    @pyqtSlot()
    def on_pbt_start_clicked(self):
        self.ui.combobox_time.setDisabled(True)
        self.ui.spinbox_time.setDisabled(True)
        self.ui.pbt_start.setDisabled(True)
        self.ui.pbt_pause.setDisabled(False)
        self._timer.start()
        self.timer.start()
    @pyqtSlot()    
    def on_pbt_pause_clicked(self):
        self.__stop()
    def __stop(self):
        self._timer.stop() 
        self.ui.combobox_time.setDisabled(False)
        self.ui.spinbox_time.setDisabled(False)
        self.ui.pbt_start.setDisabled(False)
        self.ui.pbt_pause.setDisabled(True)
    @pyqtSlot()
    def on_pbt_clear_clicked(self):
        self.__fig.clf()
        self.x=np.empty(0)
        self.y=np.empty(0)
        self.ui.lineEdit.setText('')
        self.itemModel.removeRows(0,self.itemModel.rowCount())
        self.__table_view()
        self.i=0
        self.__createFigure()
        print('clear')     
    @pyqtSlot()
    def on_pbt_csv_clicked(self):
        curPath=QDir.currentPath()
        title='save txt file'
        filt='txt(*.txt)'
        fileName,flt=QFileDialog.getSaveFileName(self,title,curPath,filt)
        if (fileName==""):
            return
        else: 
            try:
                self.__saveByIODevice(fileName)
            except:
                QMessageBox.critical(self,'error',"can't save file")  
    def __saveByIODevice(self,fileName):
        print('save your file')  
        save_data=np.concatenate((self.x.reshape(-1,1),self.y.reshape(-1,1)),axis=1)
        np.savetxt(fileName,save_data,fmt='%.3f',encoding='utf8',delimiter=',')
        print('successfully save')
    def __table_view(self):
        self.itemModel=QStandardItemModel(1,2,self)
        self.selectionModel=QItemSelectionModel(self.itemModel)
        self.ui.tableView.setModel(self.itemModel)
        self.ui.tableView.setSelectionModel(self.selectionModel)
        self.ui.tableView.setAlternatingRowColors(True)
        self.itemModel.setHorizontalHeaderLabels(self.header)
        self.selectionModel.currentChanged.connect(self.__do_curChanged)
    def __do_curChanged(self):
        x=QStandardItem(str(self.i))
        y=QStandardItem(str(self.data))
        self.itemModel.setItem(self.i,0,x)
        self.itemModel.setItem(self.i,1,y)
        self.i+=1
        
    
if __name__ == '__main__':
    app=QApplication(sys.argv)
    form=function()
    form.show()    
    
    sys.exit(app.exec_())