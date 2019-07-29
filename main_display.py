from UtilitiesMod import convert_ui, create_database
from Transactions import Transactions
from categories import Categories
from mainwindow import *
from addtransactionwindow import *
from edittransactionwindow import *
from datetime import date
from categories_display import CategoriesWindow
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import QDate
from sys import exit


class AddDialog(QDialog):
    def __init__(self, mainwindow):
        super().__init__()
        self.ui = Ui_add_transaction_dialog()
        self.ui.setupUi(self)
        self.mainwindow = mainwindow
        self.ui.expense_radioButton.setChecked(True)
        self.category_manager = Categories()
        self.transactions = Transactions()
        self.load_categories()
        self.ui.dateEdit.setDate(QDate(date.today().year, date.today().month, date.today().day))

        self.show()

        self.ui.expense_radioButton.toggled.connect(self.expense_radiobtn_active)
        self.ui.income_radioButton.toggled.connect(self.income_radiobtn_active)
        self.ui.savebutton.clicked.connect(self.save_category)
        self.ui.back_pushButton.clicked.connect(self.close)

        self.mainwindow.setEnabled(False)

    def expense_radiobtn_active(self):
        if self.ui.expense_radioButton.isChecked():
            self.load_categories()

    def income_radiobtn_active(self):
        if self.ui.income_radioButton.isChecked():
            self.load_categories()

    def save_category(self):
        if self.ui.categories_combobox.count() > 0 and self.ui.amountlineEdit.text() != "":
            category_type = self.get_active_radiobtn()
            category = self.ui.categories_combobox.currentText()
            amount = self.ui.amountlineEdit.text()
            date_ = self.ui.dateEdit.date().toPyDate()
            note = self.ui.notelineEdit.text()
            print(category_type, category, amount, date_, note)
            try:
                amount = float(amount)
                self.transactions.add(category, amount, date_, note, category_type)
                self.mainwindow.load_table()
                self.close()
                QMessageBox.information(self,
                                        'Transaction Saved',
                                        f"{category.capitalize()} transaction is saved successfuly")
            except ValueError as verr:
                QMessageBox.warning(self,
                                    'Wrong Format',
                                    'The amount entered is not a proper number format\nplease check it again',
                                    QMessageBox.Ok)
        else:
            QMessageBox.warning(self,
                                'Fields Missing',
                                'Please insert all the required information about the transaction and try again',
                                QMessageBox.Ok)

    def get_active_radiobtn(self):
        if self.ui.expense_radioButton.isChecked():
            return 'expense'
        else:
            return 'income'

    def load_categories(self):
        self.ui.categories_combobox.clear()
        self.ui.categories_combobox.addItems(self.category_manager.category_list[self.get_active_radiobtn()])

    def closeEvent(self, event: QtGui.QCloseEvent):
        self.mainwindow.setEnabled(True)
        event.accept()


class EditDialog(QDialog):
    def __init__(self, transaction, mainwindow):
        super().__init__()
        self.ui = Ui_edit_transaction_dialog()
        self.ui.setupUi(self)
        self.mainwindow = mainwindow
        self.transaction = transaction
        self.mainwindow.setEnabled(False)
        self.transaction_manager = Transactions()
        self.categories = Categories().category_list[self.transaction['type']]
        self.laod_transaction()
        self.show()

        self.ui.back_pushButton.clicked.connect(self.close)
        self.ui.savebutton.clicked.connect(self.edit)
        print(transaction)

    def laod_transaction(self):
        self.ui.type_label.setText(self.transaction['type'])
        self.ui.amountlineEdit.setText(self.transaction['amount'])
        date_ = [int(part) for part in self.transaction['date'].split('-')]
        self.ui.dateEdit.setDate(QDate(date_[0], date_[1], date_[2]))
        self.ui.notelineEdit.setText(self.transaction['note'])
        self.ui.categories_combobox.clear()
        self.ui.categories_combobox.addItems(self.categories)
        self.ui.categories_combobox.setCurrentIndex(self.categories.index(self.transaction['category']))

    def change(self):
        ui_date = self.ui.dateEdit.date().toPyDate()
        entry_date = [int(part) for part in self.transaction['date'].split('-')]
        entry_date = date(entry_date[0], entry_date[1], entry_date[2])

        ui_amount = float(self.ui.amountlineEdit.text())
        entry_amount = float(self.transaction['amount'])

        ui_category = self.ui.categories_combobox.currentText()
        entry_category = self.transaction['category']

        ui_note = self.ui.notelineEdit.text().strip()
        entry_note = self.transaction['note']

        print(ui_note, entry_note)

        return not (ui_amount == entry_amount and ui_category == entry_category and ui_note == entry_note and ui_date == entry_date)


    def edit(self):
        if self.change():
            row_id = self.transaction['row_id']
            category = self.ui.categories_combobox.currentText()
            amount = float(self.ui.amountlineEdit.text())
            note = self.ui.notelineEdit.text().strip()
            date_ = str(self.ui.dateEdit.date().toPyDate())
            self.transaction_manager.edit(row_id, category, amount, date_, note)
            self.transaction_manager.refresh()
            self.mainwindow.load_table()
            self.close()
            QMessageBox.information(self,
                                    'Transaction Updated',
                                    'Transaction is updated successfully',
                                    QMessageBox.Ok)

            self.transaction['category'] = category
            self.transaction['amount'] = amount
            self.transaction['date'] = date_
            self.transaction['note'] = note
        else:
            QMessageBox.warning(self,
                                'Can\'t update',
                                'Nothing is edited to update\nPlease edit the transaction entry first before clicking edit',
                                QMessageBox.Ok)


    def closeEvent(self, event: QtGui.QCloseEvent):
        self.mainwindow.setEnabled(True)
        event.accept()


class MainWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.transactions = Transactions()
        self.show()

        self.ui.categories_pushButton.clicked.connect(self.categories_button_click)
        self.ui.add_pushButton.clicked.connect(self.add_button_click)
        self.ui.edit_pushButton.clicked.connect(self.edit_button_click)
        self.ui.delete_pushButton.clicked.connect(self.delet_button_click)
        self.ui.view_pushButton.clicked.connect(self.view_button_click)

        self.ui.expense_radioButton.toggled.connect(self.expense_radiobtn_active)
        self.ui.income_radioButton.toggled.connect(self.income_radiobtn_active)

        self.ui.expense_radioButton.setChecked(True)
        self.load_table()

    def categories_button_click(self):
        categories_window = CategoriesWindow()
        categories_window.exec_()

    def add_button_click(self):
        add_window = AddDialog(self)
        add_window.exec_()

    def edit_button_click(self):
        selection = self.get_table_selection()
        if selection:
            edit_dialog = EditDialog(self.get_table_selection(), self)
            edit_dialog.exec_()
        else:
            QMessageBox.warning(self,
                                'No Transaction Selected',
                                'Please select a transaction before clicking the edit button again',
                                QMessageBox.Ok)

    def delet_button_click(self):
        selected_transaction = self.get_table_selection()
        if selected_transaction:
            delete_question = QMessageBox.question(self,
                                                   'Delete Transaction',
                                                   'Are you sure you want to delete the selected transaction',
                                                   QMessageBox.Yes | QMessageBox.No)
            if delete_question == QMessageBox.Yes:
                self.transactions.delete(selected_transaction['row_id'])
                self.load_table()
        else:
            QMessageBox.warning(self,
                                'Nothing is selected',
                                'Please select something first before you click the delete button again',
                                QMessageBox.Ok)

    def view_button_click(self):
        pass

    def expense_radiobtn_active(self):
        if self.ui.expense_radioButton.isChecked():
            self.load_table()

    def income_radiobtn_active(self):
        if self.ui.income_radioButton.isChecked():
            self.load_table()

    def get_active_radiobtn(self):
        if self.ui.income_radioButton.isChecked():
            return 'income'
        else:
            return 'expense'

    def load_table(self):
        self.ui.tableWidget.clearContents()
        dataframe = self.transactions.transactions_dict[self.get_active_radiobtn()]
        print(dataframe)
        r, c = dataframe.shape
        self.ui.tableWidget.setRowCount(r)
        self.ui.tableWidget.setColumnCount(c + 1)
        self.ui.tableWidget.setHorizontalHeaderLabels(['#', 'Category', 'Amount', 'Date', 'Memo', 'Type'])
        row_count = 0
        for row_index, row_data in dataframe.iterrows():
            self.ui.tableWidget.setItem(row_count, 0, QTableWidgetItem(str(row_index)))
            self.ui.tableWidget.setItem(row_count, 1, QTableWidgetItem(row_data['category']))
            self.ui.tableWidget.setItem(row_count, 2, QTableWidgetItem(str(row_data['amount'])))
            self.ui.tableWidget.setItem(row_count, 3, QTableWidgetItem(row_data['date']))
            self.ui.tableWidget.setItem(row_count, 4, QTableWidgetItem(row_data['note']))
            self.ui.tableWidget.setItem(row_count, 5, QTableWidgetItem(row_data['type']))
            row_count += 1
        header = self.ui.tableWidget.horizontalHeader()
        for i in range(6):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)

    def get_table_selection(self):
        items = [item.text() for item in self.ui.tableWidget.selectedItems()]
        if items:
            return {'row_id': items[0],
                    'category': items[1],
                    'amount': items[2],
                    'date': items[3],
                    'note': items[4],
                    'type': items[5],
                    }
        else:
            return False


    def closeEvent(self, event: QtGui.QCloseEvent):
        exit()
        event.accept()


if __name__ == '__main__':
    convert_ui('mainwindow.ui', 'addtransactionwindow.ui', 'edittransactionwindow.ui')
    create_database()
    app = QApplication([])
    window = MainWindow()
    exit(app.exec_())
