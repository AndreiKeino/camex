from PyQt5.QtWidgets import (QMainWindow, QAction, QMessageBox, QApplication,
                             QHBoxLayout, QVBoxLayout, QSplitter, QFrame,
                             QStatusBar)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import utils.utils as utils
import widgets.browser_widget as bv
from widgets.inputs_widget import InputsWidget
import app_data.addon_data as addon_data
import os
import sys
from app_data.ui_info import (main_window_title, app_name,
                              app_version, user_guide_url,
                              author, license_url)
from qtconsole.rich_jupyter_widget import RichJupyterWidget
from qtconsole.manager import QtKernelManager


# The ID of an installed kernel, e.g. 'bash' or 'ir'. For jupyter_widget.
USE_KERNEL = 'python3'


def make_jupyter_widget_with_kernel():
    """Start a kernel, connect to it, and create a RichJupyterWidget to use it
    """
    kernel_manager = QtKernelManager(kernel_name=USE_KERNEL)
    kernel_manager.start_kernel()

    kernel_client = kernel_manager.client()
    kernel_client.start_channels()

    jupyter_widget = RichJupyterWidget()
    jupyter_widget.kernel_manager = kernel_manager
    jupyter_widget.kernel_client = kernel_client
    return jupyter_widget


def messageBox(parent, text):
    msgBox = QMessageBox(parent)
    msgBox.setWindowTitle(main_window_title)
    msgBox.setText(text)
    msgBox.exec()


class MainWindow(QMainWindow):

    frame = None
    jupyter_widget = None
    browser_widget = None
    addon_list = []
    current_addon = None  # currently shown addon

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle(main_window_title)
        self.setWindowIcon(QIcon(os.path.join(utils.get_exe_folder(), 
                           'appicon.ico')))

        self.init_jupyter_widget()
        self.init_addon_menu()  
        self.init_splitter()
        self.init_statusbar()
        self.init_help_menu()
        self.setCentralWidget(self.frame)

    def closeEvent(self, event):
        # close all the plots
        # plt.close("all")
        # nothing to close as
        # all the plots are in
        # console
        pass

    def init_help_menu(self):
        menubar = self.menuBar()
        self.__help_menu = menubar.addMenu('Help')

        action = QAction('User guide', self)
        self.__help_menu.addAction(action)
        action.triggered.connect(self.on_help_user_guide)

        action = QAction('License', self)
        self.__help_menu.addAction(action)
        action.triggered.connect(self.on_help_license)

        action = QAction('About...', self)
        self.__help_menu.addAction(action)
        action.triggered.connect(self.on_help_about)

    def on_help_license(self, q):
        self.browser_widget.load_page(license_url)

    def on_help_user_guide(self, q):
        self.browser_widget.load_page(user_guide_url)

    def on_help_about(self, q):
        # main_window_title, app_name, app_version
        text = (app_name + ' version ' + app_version
                + '.\nby ' + author + '.')
        QMessageBox.about(self, main_window_title, text)

    def init_statusbar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def init_splitter(self):
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.StyledPanel)
        hbox = QHBoxLayout()  # here should be no 'self' argument
        self.browser_widget = bv.BrowserWidget(self)
        self.top_splitter = QSplitter(Qt.Horizontal)
        frame = QFrame()
        layout = QVBoxLayout()
        for addon in self.addon_list:
            layout.addWidget(addon)
            addon.hide()
        frame.setLayout(layout)        
        self.top_splitter.addWidget(frame)
        self.current_addon = self.addon_list[0]
        self.current_addon.show_itself()
        self.top_splitter.addWidget(self.browser_widget)
        self.top_splitter.setSizes([100, 200])

        handle_width = 6

        # https://stackoverflow.com/questions/2545577/qsplitter-becoming-undistinguishable-between-qwidget-and-qtabwidget
        self.top_splitter.setOpaqueResize(False)
        self.top_splitter.setChildrenCollapsible(False)
        self.top_splitter.setHandleWidth(handle_width)

        splitter2 = QSplitter(Qt.Vertical)
        splitter2.addWidget(self.top_splitter)
        splitter2.addWidget(self.jupyter_widget)
        splitter2.setOpaqueResize(False)
        splitter2.setChildrenCollapsible(False)
        splitter2.setHandleWidth(handle_width)

        hbox.addWidget(splitter2)

        self.frame.setLayout(hbox)

    def init_jupyter_widget(self):
        self.jupyter_widget = make_jupyter_widget_with_kernel()

    def shutdown_kernel(self):
        print('Shutting down kernel...')
        self.jupyter_widget.kernel_client.stop_channels()
        self.jupyter_widget.kernel_manager.shutdown_kernel()

    def init_addon_menu(self):
        self.__menubar = self.menuBar()
        addon_list = addon_data.addon_list
        self.__addon_menu = self.__menubar.addMenu('Addons')
        for addon_group in addon_list:
            group_menu = self.__addon_menu.addMenu(addon_group.menu_name)
            for addon in addon_group.addons:
                action = QAction(addon.menu_name, self)
                group_menu.addAction(action)
                self.inputs_widget = InputsWidget(self, addon)
                action.triggered.connect(self.inputs_widget.show_itself)
                self.addon_list.append(self.inputs_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = MainWindow()
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('Test from main')
    w.showMaximized()

    sys.exit(app.exec_())
