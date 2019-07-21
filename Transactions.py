from UtilitiesMod import DatabaseManager
import datetime
import pandas as pd


class Transactions:
    class __Transactions:
        def __init__(self):
            self.expense_transactions = pd.DataFrame()
            self.income_transactions = pd.DataFrame()
            self.transactions_dict = {}
            self.refresh()

        def refresh(self):
            # we want to get the transactions of the current month
            today = datetime.date.today()
            query_date = today.strftime("'%Y-%m%'")
            with DatabaseManager() as db:
                # select_expense = f"select rowid, * from Transactions where type = 'expense' and date like {query_date}"
                select_expense = f"select rowid, * from Transactions where type = 'expense'"
                self.expense_transactions = pd.read_sql(select_expense, db.connection, index_col='rowid')
                select_income = f"select rowid, * from Transactions where type = 'income' and date like {query_date}"
                self.income_transactions = pd.read_sql(select_income, db.connection, index_col='rowid')
                self.transactions_dict = {'expense': self.expense_transactions,
                                          'income': self.income_transactions}

        def add(self, category: str, amount: float, date: str, note: str, type_: str):
            # sql table order category, amount, date, note, type
            insert_statement = f"insert into Transactions values('{category}', {amount}, '{date}', '{note}', '{type_}')"
            with DatabaseManager() as db:
                db.execute(insert_statement)
                db.connection.commit()
            with DatabaseManager() as db:
                db.execute('select rowid from Transactions order by rowid desc limit 1')
                rowid = db.fetchone()[0]
            self.transactions_dict[type_].loc[rowid] = [category, amount, date, note, type_]

        def edit(self, rowid, new_category, new_amount, new_date, new_note):
            # category, amount, date, note, type
            update_statement = ("update Transactions set\n"
                                f"category = '{new_category}',\n"
                                f"amount = {new_amount},\n"
                                f"date = '{new_date}',\n"
                                f"note = '{new_note}'\n"
                                f"where rowid = {rowid}")

            with DatabaseManager() as db:
                db.execute(update_statement)
                db.connection.commit()

            self.refresh()

            # print(update_statement)

        def delete(self, rowid):
            with DatabaseManager() as db:
                db.execute(f"delete from Transactions where rowid = {rowid}")
                db.connection.commit()
            self.refresh()

        def balance(self):
            return self.income_transactions['amount'].sum() - self.expense_transactions['amount'].sum()

        def __str__(self):
            return (f"{self.income_transactions}\n"
                    "----------------------------------------\n"
                    f"{self.expense_transactions}\n\n"
                    f"total income = {self.income_transactions['amount'].sum()}\n"
                    f"total expense = {self.expense_transactions['amount'].sum()}\n"
                    f"balance = {self.balance()}")

    instance = None

    def __new__(cls):
        if Transactions.instance is None:
            Transactions.instance = Transactions.__Transactions()

        return Transactions.instance


if __name__ == '__main__':
    transaction = Transactions()
    print(transaction)
