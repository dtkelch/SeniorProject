import output as ui_plot
import sys
import numpy
from PyQt4 import QtCore, QtGui
import PyQt4.Qwt5 as Qwt
from recorder import *



def plotSomething():
    if recorder.newAudio==False: 
        return
    xs,ys=recorder.fft()
    #chord = recorder.getNote(xs, ys)
    chord = recorder.getChord(xs, ys)    
    if chord:    
        uiplot.currentLabel.setText("Current: " + chord[0])
        uiplot.nextLabel.setText("Next: " + ', '.join(chord[1][1:]))

    c.setData(xs,ys)
    uiplot.qwtPlot.replot()
    recorder.newAudio=False
        
def thresholdChange():
    threshold = uiplot.threshold_slider.value()
    recorder.updateThreshold(threshold)
#    xt = [threshold for _ in range(204)]
#    yt = [i for i in range(204)]
#    t.setData(xt, yt)
#    uiplot.qwtPlot.replot()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    
    win_plot = ui_plot.QtGui.QMainWindow()
    uiplot = ui_plot.Ui_win_plot()
    uiplot.setupUi(win_plot)
    #uiplot.btnB.clicked.connect(lambda: uiplot.timer.setInterval(100.0))
    
    c=Qwt.QwtPlotCurve()  
    c.attach(uiplot.qwtPlot)
    
#    t=Qwt.QwtPlotCurve()
#    t.attach(uiplot.qwtPlot)
    
    uiplot.qwtPlot.setAxisScale(uiplot.qwtPlot.yLeft, 0, 100000)
    
    uiplot.timer = QtCore.QTimer()
    uiplot.timer.start(1.0)
    
    win_plot.connect(uiplot.timer, QtCore.SIGNAL('timeout()'), plotSomething) 
    
    recorder = Recorder()
    recorder.setup()
    recorder.continuousStart()
    
    uiplot.threshold_slider.setValue(50000)
    uiplot.threshold_slider.sliderReleased.connect(lambda: thresholdChange())    
    
    
#    uiplot.btnA.clicked.connect(recorder.increaseThreshold())

   
    ### DISPLAY WINDOWS
    win_plot.show()
    code=app.exec_()
    recorder.close()
    sys.exit(code)