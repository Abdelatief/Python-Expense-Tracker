from PyQt5.QtWidgets import QDialog, QApplication, QWidget
from categorieswindow import *
from addcategorydialog import *
from categories import Categories
from sys import exit
from UtilitiesMod import convert_ui


class AddDialog(QDialog):
    def __init__(self, mainwindow):
        super().__init__()
        self.ui = Ui_add_category_dialog()
        self.ui.setupUi(self)
        self.mainwindow = mainwindow
        self.show()

        self.mainwindow.setEnabled(False)
        self.label_type()

        self.ui.savecategory_pushButton.clicked.connect(self.save_category)

    def label_type(self):
        type_ = self.mainwindow.get_active_radiobtn()
        self.ui.category_label.setText(f'{type_.capitalize()} Category Name:')

    def save_category(self):
        if self.mainwindow.ui.income_radioButton.isChecked():
            category_type = 'income'
        else:
            category_type = 'expense'

        value = self.ui.category_lineEdit.text().strip()

        if value != "":
            if self.mainwindow.categories_manager.save_category(category_type, value):
                print('category saved successfully')
                self.mainwindow.load_categories()
                self.close()
        else:
            print('category line edit is empty')

    def closeEvent(self, event: QtGui.QCloseEvent):
        self.mainwindow.setEnabled(True)
        self.mainwindow.load_categories()
        event.accept()



class CategoriesWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.expense_radioButton.setChecked(True)
        self.categories_manager = Categories()
        self.load_categories()
        print(self.categories_manager)
        self.show()

        self.ui.add_pushButton.clicked.connect(self.add_button_click)
        self.ui.rename_pushButton.clicked.connect(self.rename_button_click)
        self.ui.delete_pushButton.clicked.connect(self.delete_button_click)
        self.ui.back_pushButton.clicked.connect(self.close)
        self.ui.expense_radioButton.toggled.connect(self.expense_radiobtn_active)
        self.ui.income_radioButton.toggled.connect(self.income_radiobtn_active)


    def add_button_click(self):
        add_dialog = AddDialog(self)
        add_dialog.exec_()

    def rename_button_click(self):
        pass

    def delete_button_click(self):
        pass

    def expense_radiobtn_active(self):
        if self.ui.expense_radioButton.isChecked():
            self.load_categories()

    def income_radiobtn_active(self):
        if self.ui.income_radioButton.isChecked():
            self.load_categories()

    def get_active_radiobtn(self):
        if self.ui.expense_radioButton.isChecked():
            return 'expense'
        else:
            return 'income'

    def load_categories(self):
        self.ui.categories_listWidget.clear()
        self.ui.categories_listWidget.addItems(self.categories_manager.category_list[self.get_active_radiobtn()])


if __name__ == '__main__':
    convert_ui('categorieswindow.ui', 'addcategorywidget.ui', 'renamecategorywidget.ui', 'addcategorydialog.ui')
    app = QApplication([])
    categories_window = CategoriesWindow()
    exit(app.exec_())
