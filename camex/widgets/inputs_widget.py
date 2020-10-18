# widget for editing user input and run sourdce
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (QWidget, QScrollArea, QComboBox,
                             QVBoxLayout, QGroupBox,
                             QPushButton, QSizePolicy, QMessageBox,
                             QPlainTextEdit, QLabel, QHBoxLayout, QGridLayout)
from app_data.ui_info import main_window_title
from app_data.addon_data import AddonData
import utils.utils as utils
import widgets.input_controls as ic
import os


class InputsWidget(QWidget):

    jupyter_widget = None
    parent = None

    def __init__(self, parent, addon_data: AddonData):
        super().__init__()
        self.__input_control_list = []
        self.title = "PyQt5 Scroll Bar"
        self.top = 200
        self.left = 500
        self.width = 400
        self.height = 300
        self.form_layout = QVBoxLayout()
        self.addon_data = addon_data
        self.groupbox = QGroupBox(self.addon_data.menu_name)
        self.parent = parent
        self.jupyter_widget = self.parent.jupyter_widget
        self.tools_layout = QGridLayout()

        self.btn_run = QPushButton("Run...")
        self.btn_run.setSizePolicy(QSizePolicy.Fixed,  QSizePolicy.Fixed)
        self.btn_run.clicked.connect(self.on_btn_run)
        self.tools_layout.addWidget(self.btn_run, 1, 1)

        self.btn_stop = QPushButton("Stop")
        self.btn_stop.setSizePolicy(QSizePolicy.Fixed,  QSizePolicy.Fixed)
        self.btn_stop.clicked.connect(self.on_btn_stop)
        self.tools_layout.addWidget(self.btn_stop, 1, 2)

        self.btn_restart_kernel = QPushButton("Restart kernel...")
        self.btn_restart_kernel.setSizePolicy(QSizePolicy.Fixed,
                                              QSizePolicy.Fixed)
        self.btn_restart_kernel.clicked.connect(self.on_btn_restart_kernel)
        self.tools_layout.addWidget(self.btn_restart_kernel, 2, 1)

        self.btn_clear_console = QPushButton("Clear console")
        self.btn_clear_console.setSizePolicy(QSizePolicy.Fixed,
                                             QSizePolicy.Fixed)
        self.btn_clear_console.clicked.connect(self.on_btn_clear_console)
        self.tools_layout.addWidget(self.btn_clear_console, 2, 2)

        #  prevent the grid layout from resizing
        self.tools_layout.setColumnStretch(3, 1)

        self.form_layout.addLayout(self.tools_layout)

        self.lbl_backend = QLabel("Choose potting backend:")
        self.lbl_backend.setSizePolicy(QSizePolicy.Minimum,
                                       QSizePolicy.Minimum)

        self.combo_backend = QComboBox()
        self.combo_backend.setSizePolicy(QSizePolicy.Minimum,
                                         QSizePolicy.Minimum)
        self.combo_backend.addItem('inline')
        self.combo_backend.addItem('qt5')

        self.layout_backend = QHBoxLayout()
        self.layout_backend.addWidget(self.combo_backend)
        self.layout_backend.addStretch(1)
        self.form_layout.addWidget(self.lbl_backend)
        self.form_layout.addLayout(self.layout_backend)

        self.combo_backend.currentIndexChanged.connect(
            self.on_combo_backend_currentIndexChanged)

        # textbox with addon directory path
        self.lbl_addon_dir = QLabel("Addon folder:")
        self.lbl_addon_dir.setSizePolicy(QSizePolicy.Fixed,  QSizePolicy.Fixed)
        self.form_layout.addWidget(self.lbl_addon_dir)
        self.addon_path = os.path.dirname(os.path.dirname(__file__))
        self.addon_path += self.addon_data.rel_path

        self.text_addon_dir = QPlainTextEdit(self)
        self.text_addon_dir.setPlainText(self.addon_path)
        self.text_addon_dir.setFixedSize(252, 120)
        self.text_addon_dir.setSizePolicy(QSizePolicy.Fixed,  
                                          QSizePolicy.Fixed)
        self.text_addon_dir.setReadOnly(True)
        self.form_layout.addWidget(self.text_addon_dir)

        # TODO: move the input controls
        # to a child QFrame

        # add the input controls to the layout
        for c in self.addon_data.inuput_controls:
            c.parameters["parent"] = self
            c.parameters["layout"] = self.form_layout
            if c.class_name == ic.FileChoose.class_name():
                # in this case 'value' is just the filename
                # make it the file path
                c.parameters["value"] = (self.addon_path
                                         + os.path.sep
                                         + c.parameters["value"])
            control = ic.create_input_control(c.class_name, c.parameters)
            self.__input_control_list.append(control)
        # input controls added

        self.form_layout.addStretch(1)
        self.groupbox.setLayout(self.form_layout)
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.groupbox)
        self.scroll.setWidgetResizable(True)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.scroll)

    def on_combo_backend_currentIndexChanged(self, q):
        # set selectioon index for combo_backend
        # for all the instances of the InputsWidget

        # TODO: move the input controls
        # to a child QFrame

        instances = self.parent.addon_list
        cur_ind = self.combo_backend.currentIndex()
        for instance in instances:
            if instance.combo_backend.currentIndex() != cur_ind:
                instance.combo_backend.setCurrentIndex(cur_ind)
        if not self.jupyter_widget._executing:
            command = ('%matplotlib '
                       + str(self.combo_backend.currentText())
                       + '\n')
            self.jupyter_widget.execute(source=command, hidden=False)     

    def on_btn_clear_console(self, q):
        if not self.jupyter_widget._executing:
            self.jupyter_widget.execute(source='%clear', hidden=False)

    def on_btn_restart_kernel(self, q):
        if self.jupyter_widget._executing:
            return
        self.jupyter_widget.request_restart_kernel()
        self.__enable_restart_controls_val = False
        self.enable_restart_controls()
        self.__enable_restart_controls_val = True
        QTimer.singleShot(2000, self.enable_restart_controls)

    def enable_restart_controls(self):
        enable = self.__enable_restart_controls_val
        self.btn_run.setEnabled(enable)
        self.btn_stop.setEnabled(enable)
        self.btn_restart_kernel.setEnabled(enable)
        self.btn_clear_console.setEnabled(enable)

    def on_btn_run(self, q):
        # set the self.jupyter_widget variable from parent
        self.jupyter_widget = self.parent.jupyter_widget
        # do nothing if jupyter_widget already executing
        if self.jupyter_widget._executing:
            return
        # read the source file
        try:
            with open(os.path.join(self.addon_path, 'execute.py'), "r") as py_file:
                source = py_file.read()
        except Exception as e:
            QMessageBox.critical(self.parent, main_window_title,
                                 'Error loading the code: ' + str(e))
            return str(e)
        finally:
            pass
        # print the input parameter values as the
        # python source code
        params = ''
        for c in self.__input_control_list:
            value = c.get_value()
            if value is None:  # incorrect user input
                return
            if isinstance(value, str):
                value = 'r"' + value + '"'  # enclosing string in quotes
            var_name = c.get_var_name()
            var_name.strip()
            if (' ') in var_name:
                msg = "variable " + var_name + ' has spaces'
                QMessageBox.critical(self.parent, main_window_title, msg)
                return

            params = (params + var_name
                      + ' = ' + str(value)
                      + '\n')

        # backend
        params += ('%matplotlib '
                   + str(self.combo_backend.currentText())
                   + '\n')

        # prepending the read source code with the
        # parameter initialization

        source = params + '\n' + source
        # write the created source in the file for debugging
        with open(self.addon_path + '/saved.py', "w") as text_file:
            text_file.write(source)

        # and finally run the code in the jupyter_widget
        self.jupyter_widget.execute(source=source, hidden=False)

    def on_btn_stop(self, q):
        if self.jupyter_widget._executing:
            self.jupyter_widget.request_interrupt_kernel()

    def show_itself(self):
        self.parent.current_addon.hide()
        self.show()
        self.parent.current_addon = self
        html_path = os.path.join(self.addon_path, 'html')
        html_path = os.path.join(html_path, 'help.html')
        self.parent.browser_widget.open_local_text(html_path)
