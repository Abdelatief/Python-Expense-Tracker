from UtilitiesMod import convert_ui
from mainwindow import *
from categories_display import CategoriesWindow
from PyQt5.QtWidgets import QApplication, QDialog
from sys import exit


class MainWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.show()

        self.ui.categories_pushButton.clicked.connect(self.categories_button_click)
        self.ui.add_pushButton.clicked.connect(self.add_button_click)
        self.ui.edit_pushButton.clicked.connect(self.edit_button_click)
        self.ui.delete_pushButton.clicked.connect(self.delet_button_click)
        self.ui.view_pushButton.clicked.connect(self.view_button_click)

        self.ui.expense_radioButton.toggled.connect(self.expense_radiobtn_active)
        self.ui.income_radioButton.toggled.connect(self.income_radiobtn_active)

    def categories_button_click(self):
        categories_window = CategoriesWindow()
        categories_window.exec_()

    def add_button_click(self):
        pass

    def edit_button_click(self):
        pass

    def delet_button_click(self):
        pass

    def view_button_click(self):
        pass

    def expense_radiobtn_active(self):
        if self.ui.expense_radioButton.isChecked():
            pass

    def income_radiobtn_active(self):
        if self.ui.income_radioButton.isChecked():
            pass

    def closeEvent(self, event: QtGui.QCloseEvent):
        exit()
        event.accept()


if __name__ == '__main__':
    convert_ui('mainwindow.ui')
    app = QApplication([])
    window = MainWindow()
    exit(app.exec_())
