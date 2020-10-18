import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QHBoxLayout,
                             QVBoxLayout, QLineEdit, QMessageBox, QLabel,
                             QSizePolicy, QFileDialog, QPlainTextEdit)

from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtCore import QSize
import math
from abc import ABC, abstractmethod


# base class for all the input controls
class InputControl(ABC):

    @abstractmethod
    def get_value(self):
        pass

    @abstractmethod
    def get_var_name(self):
        pass


class FileChoose(InputControl):

    def __init__(self, var_name, caption, dialog_title,
                 value, layout=None, parent=None, edit_size=QSize(252, 120)):
        self.__var_name = var_name
        self.caption = caption
        self.dialog_title = dialog_title
        self.layout = layout
        self.parent = parent
        self.value = value
        self.edit_size = edit_size

        self.label = QLabel(caption)
        self.layout.addWidget(self.label)

        self.text_file_path = QPlainTextEdit(parent)
        self.text_file_path.setPlainText(self.value)
        self.text_file_path.setFixedSize(self.edit_size.width(),
                                         self.edit_size.height())
        self.text_file_path.setSizePolicy(QSizePolicy.Fixed,
                                          QSizePolicy.Fixed)
        self.text_file_path.setReadOnly(True)
        self.layout.addWidget(self.text_file_path)

        self.btn_choose = QPushButton("Choose file...")
        self.btn_choose.setSizePolicy(QSizePolicy.Fixed,  QSizePolicy.Fixed)
        self.btn_choose.clicked.connect(self.on_btn_choose)
        self.layout.addWidget(self.btn_choose)

    @staticmethod
    def class_name():
        return 'FileChoose'

    def on_btn_choose(self, q):
        fname = QFileDialog.getOpenFileName(self.parent,
                                            self.dialog_title)[0]
        if fname != '':
            self.text_file_path.setPlainText(fname)

    def get_value(self):
        return self.text_file_path.toPlainText()

    def get_var_name(self):
        # variable name
        # used for creating corresponding variable in the
        # source code to execute
        return self.__var_name


class DoubleEditInput(InputControl):
    # https://python-forum.io/Thread-How-to-accept-only-float-number-in-QLineEdit-input
    # https://doc.qt.io/qtforpython/PySide2/QtGui/QIntValidator.html
    # https://doc.qt.io/qtforpython/PySide2/QtGui/QDoubleValidator.html

    def __init__(self, var_name, caption, msgbox_title,
                 value, layout=None, parent=None, min=-math.inf,
                 max=math.inf, func=float):
        # variable name
        # used for creating corresponding variable in the
        # source code to execute
        self.__var_name = var_name
        self.min = min
        self.max = max
        self.caption = caption
        self.msgbox_title = msgbox_title
        self.layout = layout
        self.parent = parent
        self.value = value
        self.label = QLabel(caption)
        self.layout.addWidget(self.label)
        self.edit = QLineEdit(str(self.value))
        self.edit.setSizePolicy(QSizePolicy.Fixed,  QSizePolicy.Fixed)
        self.edit.setValidator(QDoubleValidator(bottom=self.min,
                                                top=self.max))
        self.layout.addWidget(self.edit)
        self.__func = func
        self.__msg = ("\nPlease enter a valid float in the range ["
                    + str(self.min) + ", " + str(self.max) + "]" +
                    " in the \'" + self.caption + "\' field")

    @staticmethod
    def class_name():
        return 'DoubleEditInput'

    def get_value(self):

        try:
            value = self.__func(self.edit.text())
        except Exception:
            value = None

        if value is not None and (value < self.min or value > self.max):
            value = None

        if value is None:
            QMessageBox.critical(self.parent, self.msgbox_title,
                                 self.__msg)
            self.edit.setFocus()
            self.edit.selectAll()
        return value

    def get_var_name(self):
        # variable name
        # used for creating corresponding variable in the
        # source code to execute
        return self.__var_name

    def set_func(self, func):
        self.__func = func

    def set_msg(self, msg):
        self.__msg = msg

    def set_validator(self, validator):
        self.edit.setValidator(validator)


class IntegerEditInput(DoubleEditInput):
    def __init__(self, var_name, caption, msgbox_title,
                 value, layout=None, parent=None, min=-math.inf, max=math.inf):
        super().__init__(var_name, caption, msgbox_title,
                         value, layout, parent, min, max)

        self.set_func(int)

        self.set_validator(
            QIntValidator(bottom=self.min, top=self.max))

        self.set_msg(("\nPlease enter a valid integer in the range ["
                      + str(self.min) + ", " + str(self.max) + "]" +
                      " in the \'" + self.caption + "\' field"))

    @staticmethod
    def class_name():
        return 'IntegerEditInput'


# class factory
def create_input_control(name, args):

    if name == IntegerEditInput.class_name():
        return IntegerEditInput(**args)
    elif name == DoubleEditInput.class_name():
        return DoubleEditInput(**args)
    elif name == FileChoose.class_name():
        return FileChoose(**args)
    else:
        raise Exception('create_input: unkonwn input type')
