import sys
import os


path_to_add = os.path.dirname(__file__)
if path_to_add not in sys.path:
    sys.path.append(path_to_add)

font_size = 12


def main():
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtGui import QFont
    import widgets.main_widget as mw

    app = QApplication(sys.argv)
    app.setStyleSheet(
        "QSplitter::handle { background-color: rgb(192, 192, 192)}")
    # set the application font size globally
    font = QFont(app.font().family(), font_size, app.font().weight(),
                 app.font().italic())
    app.setFont(font)

    app.setStyle('QtCurve')
    # ['Breeze', 'Oxygen', 'QtCurve', 'Windows', 'Fusion']  windowsvista
    window = mw.MainWindow()
    window.showMaximized()
    app.aboutToQuit.connect(window.shutdown_kernel)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
