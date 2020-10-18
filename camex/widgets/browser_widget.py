# https://www.learnpyqt.com/examples/mooseache/

import sys
from PyQt5.QtWidgets import (QWidget, QMainWindow, QShortcut,
                             QPushButton, QApplication,
                             QHBoxLayout, QVBoxLayout, QLabel,
                             QSizePolicy, QLineEdit, QDoubleSpinBox, QStyle)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt, QUrl


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.browser_widget = BrowserWidget(self)
        _widget = QWidget()
        _layout = QVBoxLayout(_widget)
        _layout.addWidget(self.browser_widget)
        _layout.addWidget(QPushButton('Bottom'))
        self.setCentralWidget(_widget)


class WebView(QWebEngineView):
    def __init__(self, parent):
        super(WebView, self).__init__(parent)
        self.doubleClickFunction = None
        self.mousePressFunction = None

    def mouseDoubleClickEvent(self, event):
        # https://stackoverflow.com/questions/47100945/pyside-detecting-single-and-double-clicks-on-a-qwidget
        result = QWebEngineView.mouseDoubleClickEvent(self, event)
        if self.doubleClickFunction is not None:
            self.doubleClickFunction(event)
        return result

    def mousePressEvent(self, event):
        result = QWebEngineView.mousePressEvent(self, event)   
        if self.mousePressFunction is not None:
            self.mousePressFunction(event)
        return result


class BrowserWidget(QWidget):
    def __init__(self, parent):
        super(BrowserWidget, self).__init__(parent)
        self.browser = WebView(self)
        self.__layout()
        self.__bookmark = None
        self.filename = ''

    def __layout(self):
        self.browser.loadFinished.connect(self.__onLoadFinished)
        self.__vbox = QVBoxLayout()

        self.__ctrls_layout = QHBoxLayout()
        
        self.__edit_url = QLineEdit()
        self.__ctrls_layout.addWidget(self.__edit_url)
        
        # self.__btn_go = QPushButton('Go')
        # self.__btn_go.clicked.connect(self.__on_btn_go)
        # self.__ctrls_layout.addWidget(self.__btn_go)
        # https://www.learnpyqt.com/examples/mooseache/
        # https://doc.qt.io/qt-5/qstyle.html#StandardPixmap-enum
        self.__btn_back = QPushButton()
        self.__btn_back.setIcon(self.style().standardIcon(QStyle.SP_ArrowLeft))
        self.__btn_back.setFlat(True)
        self.__btn_back.setToolTip('Back') 
        self.__btn_back.clicked.connect(self.browser.back)
        self.__ctrls_layout.addWidget(self.__btn_back)

        self.__btn_forward = QPushButton()
        self.__btn_forward.setIcon(self.style().standardIcon(QStyle.SP_ArrowForward))
        self.__btn_forward.setFlat(True)
        self.__btn_forward.setToolTip('Forward')
        self.__btn_forward.clicked.connect(self.browser.forward)
        self.__ctrls_layout.addWidget(self.__btn_forward)

        self.__btn_reload = QPushButton()
        self.__btn_reload.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        self.__btn_reload.setFlat(True)
        self.__btn_reload.setToolTip('Reload')
        self.__btn_reload.clicked.connect(self.browser.reload)
        self.__ctrls_layout.addWidget(self.__btn_reload)

        self.__btn_stop = QPushButton()
        self.__btn_stop.setIcon(self.style().standardIcon(QStyle.SP_BrowserStop))
        self.__btn_stop.setFlat(True)
        self.__btn_stop.setToolTip('Stop')
        self.__btn_stop.clicked.connect(self.browser.stop)
        self.__ctrls_layout.addWidget(self.__btn_stop)

        self.browser.urlChanged.connect(self.update_urlbar)

        self.__label_zoom = QLabel()
        self.__label_zoom.setText('Zoom')
        self.__label_zoom.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.__ctrls_layout.addWidget(self.__label_zoom, 
                                      alignment=Qt.AlignRight)

        self.__spin_zoom = QDoubleSpinBox()
        self.__spin_zoom.setRange(0.125, 15)
        self.__spin_zoom.setValue(1.0)
        self.__spin_zoom.setSingleStep(0.125)
        self.__spin_zoom.valueChanged.connect(self.__spin_zoom_valueChanged)
        self.__spin_zoom.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # https://stackoverflow.com/questions/53573382/pyqt5-set-widget-size-to-minimum-and-fix
        self.__ctrls_layout.addWidget(self.__spin_zoom, 
                                      alignment=Qt.AlignRight)
        
        self.__vbox.addLayout(self.__ctrls_layout)
        
        self.__vbox.addWidget(self.browser)
        
        self.setLayout(self.__vbox)

        self.__ctrl_plus_shortcut = QShortcut(QKeySequence("Ctrl++"), self)
        self.__ctrl_plus_shortcut .activated.connect(self.__on_ctrl_plus)

        self.__ctrl_minus_shortcut = QShortcut(QKeySequence("Ctrl+-"), self)
        self.__ctrl_minus_shortcut.activated.connect(self.__on_ctrl_minus)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.__on_btn_go()

    def update_urlbar(self, q):
        """
        if q.scheme() == 'https':
            # Secure padlock icon
            self.httpsicon.setPixmap( QPixmap( os.path.join('icons','lock-ssl.png') ) )

        else:
            # Insecure padlock icon
            self.httpsicon.setPixmap( QPixmap( os.path.join('icons','lock-nossl.png') ) )
        """
        self.__edit_url.setText(q.toString())
        self.__edit_url.setCursorPosition(0)

    def __onLoadFinished(self, ok):
        if self.__bookmark is not None:
            self.__spin_zoom.setValue(self.__bookmark.zoomFactor)                            
            text = self.__bookmark.text
            if len(text) > 0:
                self.browser.findText(text)
        self.__bookmark = None

    def __spin_zoom_valueChanged(self, value):
        self.browser.setZoomFactor(value)

    def __on_ctrl_plus(self):
        self.__spin_zoom.setValue(self.__spin_zoom.value() +
                                  self.__spin_zoom.singleStep())

    def __on_ctrl_minus(self):
        self.__spin_zoom.setValue(self.__spin_zoom.value() - self.__spin_zoom.singleStep())

    def load_page(self, url):
        qurl = QUrl(url)
        self.__edit_url.setText(qurl.toString())
        self.browser.stop()
        self.browser.load(qurl)

    def __on_btn_go(self, *args):
        if len(self.__edit_url.text()) > 0:
            self.filename = self.__edit_url.text()
            self.load_page(QUrl.fromUserInput(self.filename))

    def open_local_text(self, textFile):
        if len(textFile) > 0:
            self.filename = textFile
            self.load_page(QUrl.fromUserInput(textFile))

    def toggle_internet_controls(self, show=True):
        if show:
            self.__edit_url.show()
            self.__btn_go.show()
        else:
            self.__edit_url.hide()
            self.__btn_go.hide()
            # https://doc.qt.io/qtforpython/PySide2/QtWidgets/QBoxLayout.html#PySide2.QtWidgets.PySide2.QtWidgets.QBoxLayout.insertStretch
            self.__ctrls_layout.insertStretch(0, stretch=0)
        return self


def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    # "https://pythonspot.com"
    win.browser_widget.load_page("https://pythonspot.com")
    win.show()
    app.exec_()


if __name__ == '__main__':
    sys.exit(main()) 
    # correct way!!!
