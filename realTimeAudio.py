import ui_plot
import sys
import numpy
from PyQt4 import QtCore, QtGui
import PyQt4.Qwt5 as Qwt
from recorder import *



def plotSomething():
    if recorder.newAudio==False: 
        return
    xs,ys=recorder.fft()
    chord = recorder.getNote(xs, ys)
    if chord:    
        uiplot.currentNote.setText("Current Note: " + chord[0])
        uiplot.nextNote.setText("Try Playing: " + ', '.join(chord[1][1:]))

    c.setData(xs,ys)
    uiplot.qwtPlot.replot()
    recorder.newAudio=False
        

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    
    win_plot = ui_plot.QtGui.QMainWindow()
    uiplot = ui_plot.Ui_win_plot()
    uiplot.setupUi(win_plot)
    #uiplot.btnB.clicked.connect(lambda: uiplot.timer.setInterval(100.0))
    
    c=Qwt.QwtPlotCurve()  
    c.attach(uiplot.qwtPlot)
    
    uiplot.qwtPlot.setAxisScale(uiplot.qwtPlot.yLeft, 0, 10000)
    
    uiplot.timer = QtCore.QTimer()
    uiplot.timer.start(1.0)
    
    win_plot.connect(uiplot.timer, QtCore.SIGNAL('timeout()'), plotSomething) 
    
    recorder = Recorder()
    recorder.setup()
    recorder.continuousStart()
    
#    uiplot.btnA.clicked.connect(recorder.increaseThreshold())

   
    ### DISPLAY WINDOWS
    win_plot.show()
    code=app.exec_()
    recorder.close()
    sys.exit(code)