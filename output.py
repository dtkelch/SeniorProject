# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_plot_tab.ui'
#
# Created: Tue Apr 26 18:34:30 2016
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_win_plot(object):
    def setupUi(self, win_plot):
        win_plot.setObjectName(_fromUtf8("win_plot"))
        win_plot.resize(800, 600)
        self.centralwidget = QtGui.QWidget(win_plot)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.verticalLayout_1 = QtGui.QVBoxLayout()
        self.verticalLayout_1.setObjectName(_fromUtf8("verticalLayout_1"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab_1 = QtGui.QWidget()
        self.tab_1.setObjectName(_fromUtf8("tab_1"))
        self.qwtPlot = Qwt5.QwtPlot(self.tab_1)
        self.qwtPlot.setGeometry(QtCore.QRect(10, 10, 751, 491))
        self.qwtPlot.setObjectName(_fromUtf8("qwtPlot"))
        self.tabWidget.addTab(self.tab_1, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.tab_2)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 751, 491))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.chordBox = QtGui.QTextBrowser(self.horizontalLayoutWidget)
        self.chordBox.setObjectName(_fromUtf8("chordBox"))
        self.horizontalLayout.addWidget(self.chordBox)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.currentLabel = QtGui.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(18)
        self.currentLabel.setFont(font)
        self.currentLabel.setObjectName(_fromUtf8("currentLabel"))
        self.verticalLayout_3.addWidget(self.currentLabel)
        self.nextLabel = QtGui.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(18)
        self.nextLabel.setFont(font)
        self.nextLabel.setObjectName(_fromUtf8("nextLabel"))
        self.verticalLayout_3.addWidget(self.nextLabel)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_3.addItem(spacerItem)
        self.clearButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clearButton.sizePolicy().hasHeightForWidth())
        self.clearButton.setSizePolicy(sizePolicy)
        self.clearButton.setObjectName(_fromUtf8("clearButton"))
        self.verticalLayout_3.addWidget(self.clearButton)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.verticalLayout_1.addWidget(self.tabWidget)
        self.threshold_label = QtGui.QLabel(self.centralwidget)
        self.threshold_label.setObjectName(_fromUtf8("threshold_label"))
        self.verticalLayout_1.addWidget(self.threshold_label)
        self.threshold_slider = QtGui.QSlider(self.centralwidget)
        self.threshold_slider.setOrientation(QtCore.Qt.Horizontal)
        self.threshold_slider.setObjectName(_fromUtf8("threshold_slider"))
        self.threshold_slider.setMinimum(30000)   
        self.threshold_slider.setMaximum(100000)
        self.threshold_slider.setValue(50000)
                
        
        
        
        self.verticalLayout_1.addWidget(self.threshold_slider)
        self.verticalLayout.addLayout(self.verticalLayout_1)
        win_plot.setCentralWidget(self.centralwidget)

        self.retranslateUi(win_plot)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(win_plot)

    def retranslateUi(self, win_plot):
        win_plot.setWindowTitle(_translate("win_plot", "MainWindow", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("win_plot", "Graph", None))
        self.currentLabel.setText(_translate("win_plot", "Current:", None))
        self.nextLabel.setText(_translate("win_plot", "Next: ", None))
        self.clearButton.setText(_translate("win_plot", "Clear", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("win_plot", "Chords", None))
        self.threshold_label.setText(_translate("win_plot", "Threshold", None))

from PyQt4 import Qwt5
