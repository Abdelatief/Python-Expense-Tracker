from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
from categorieswindow import *
from addcategorydialog import *
from renamecategorydialog import *
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
        category_type = self.mainwindow.get_active_radiobtn()

        value = self.ui.category_lineEdit.text().strip()

        if value != "":
            if self.mainwindow.categories_manager.save_category(category_type, value):
                print('category saved successfully')
                self.mainwindow.load_categories()
                self.close()
                QMessageBox.information(self,
                                        'Category Saved',
                                        f"{value} category is added to {category_type} successfully",
                                        QMessageBox.Ok)
            else:
                QMessageBox.warning(self,
                                    'Category Already Exists',
                                    f"{value.capitalize()} category already exists in {category_type} categories",
                                    )
        else:
            QMessageBox.warning(self,
                                'Required Fields',
                                'Can\'t add empty category name',
                                QMessageBox.Ok)

    def closeEvent(self, event: QtGui.QCloseEvent):
        self.mainwindow.setEnabled(True)
        self.mainwindow.load_categories()
        event.accept()


class RenameDialog(QDialog):
    def __init__(self, mainwindow, category):
        super().__init__()
        self.ui = Ui_rename_category_dialog()
        self.ui.setupUi(self)
        self.mainwindow = mainwindow
        self.category = category
        self.show()

        self.ui.renamecategory_pushButton.clicked.connect(self.rename_category)

        self.ui.category_lineEdit.setText(self.category['category'])

    def rename_category(self):
        new_category = self.ui.category_lineEdit.text().strip()
        if new_category != "":
            if self.mainwindow.categories_manager.edit(self.category['type'], self.category['category'], new_category):
                print("Category renamed successfully")
                self.mainwindow.load_categories()
                self.close()
            else:
                QMessageBox.warning(self,
                                    'Category Already Exists',
                                    'The new category name already exists\nplease enter another name',
                                    QMessageBox.Ok)
                # self.ui.category_lineEdit.clear()
        else:
            QMessageBox.warning(self,
                                'Required Fields',
                                'Please fill the required new category name field',
                                QMessageBox.Ok)


    def closeEvent(self, event: QtGui.QCloseEvent):
        if __name__ == '__main__':
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
        selected_category = self.get_selected_category()
        if selected_category:
            rename_dialog = RenameDialog(self, selected_category)
            rename_dialog.exec_()
        else:
            QMessageBox.warning(self,
                                'Fields Required',
                                'Please select a category before clicking the rename button again',
                                QMessageBox.Ok)

    def delete_button_click(self):
        selected_category = self.get_selected_category()
        if selected_category:
            delete_query = QMessageBox.warning(self,
                                              'Delete Category',
                                              f"Are you sure you want to delete category: {selected_category['category']}",
                                              QMessageBox.Yes | QMessageBox.No)
            if delete_query == QMessageBox.Yes:
                self.categories_manager.delete(selected_category['type'], selected_category['category'])
                self.load_categories()
                print(f"{selected_category['category']} is deleted successfully")
            else:
                print('delete query no')
        else:
            print('no item is selected')

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

    def get_selected_category(self):
        selected_items = self.ui.categories_listWidget.selectedItems()
        if selected_items:
            selected_category =  self.ui.categories_listWidget.selectedItems()[0].text()
            return {'type': self.get_active_radiobtn(), 'category': selected_category}


if __name__ == '__main__':
    convert_ui('categorieswindow.ui', 'addcategorydialog.ui', 'renamecategorydialog.ui')
    app = QApplication([])
    categories_window = CategoriesWindow()
    exit(app.exec_())
