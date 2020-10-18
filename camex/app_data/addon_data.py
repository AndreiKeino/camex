import os
from dataclasses import dataclass
from typing import List 
from widgets.input_controls import (InputControl, FileChoose, 
                                    DoubleEditInput, IntegerEditInput)
from .ui_info import main_window_title
import math


def create_path(x):
    r = ""
    for i in range(len(x)):
        r += os.path.sep + x[i]
    return r


@dataclass(frozen=True)
class InputControlInfo():
    class_name: str
    parameters: object


# class to store the addon data
@dataclass(frozen=True)
class AddonData():
    # relative path from the main executable file
    rel_path: str
    menu_name: str
    inuput_controls: List[InputControl]


# class to store data for a group of addons
@dataclass(frozen=True)
class AddonGroupData():
    menu_name: str
    addons: List[AddonData]


#  list of addons for menu 'addons' ->
addon_list = [

    AddonGroupData(
        menu_name="Convex optimization",  # 'addons' submenu name
        addons=[  # addons for "Convex optimization" submenu ->
        # addon "L1 trend filtering" data ->
AddonData(menu_name="L1 trend filtering",
          rel_path=create_path(["addons", "cvx", "L1_trend_filtering"]),
          inuput_controls = [
          InputControlInfo(DoubleEditInput.class_name(), {'var_name': 'vlambda',
                           'caption': 'Enter lambda:',
                           'msgbox_title': main_window_title,
                           'value': 1500, 'min': 0, 'max': math.inf}),

          InputControlInfo(FileChoose.class_name(), {'var_name': 'input_file',
                           'caption': 'Choose input file:',
                           'dialog_title': 'Choose input file',
                           'value': 'data' + os.path.sep + 'input_data.csv'})
          ]),
# <- addon "L1 trend filtering" data

# addon "Portfolio_optimization" data ->
AddonData(menu_name="Portfolio optimization",
          rel_path=create_path(["addons", "cvx", "Portfolio_optimization"]),
          inuput_controls=[
            InputControlInfo(IntegerEditInput.class_name(), {'var_name': 'marker_1',
                           'caption': 'Enter marker #1 value:',
                           'msgbox_title': main_window_title,
                           'value': 29, 'min': 0, 'max': 99}),              

            InputControlInfo(IntegerEditInput.class_name(), {'var_name': 'marker_2',
                           'caption': 'Enter marker #2 value:',
                           'msgbox_title': main_window_title,
                           'value': 40, 'min': 0, 'max': 99}),

          InputControlInfo(FileChoose.class_name(), {'var_name': 'mu_fname',
                           'caption': 'Choose input file for means:',
                           'dialog_title': 'Choose input file for means',
                           'value': 'data' + os.path.sep + 'mu_data.csv'}),

          InputControlInfo(FileChoose.class_name(), {'var_name': 'sigma_fname',
                           'caption': 'Choose input file for covariances:',
                           'dialog_title': 'Choose input file for covariance matrix',
                           'value': 'data' + os.path.sep + 'sigma_data.csv'}),

          ]),  #  <- addon "Portfolio_optimization" data
                ]  #  <- addons for "Convex optimization" submenu
                  )
             ]  # <- list of addons for menu 'addons'
