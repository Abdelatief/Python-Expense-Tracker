from UtilitiesMod import directory_files


class Categories:
    class __Categories:
        def __init__(self):
            self.expense_categories = []
            self.income_categories = []
            self.category_list = {'expense': self.expense_categories,
                                  'income': self.income_categories}
            self.refresh()

        def category_exists(self, category_type: str, category: str):
            category = category.strip()
            return category.lower() not in (old_category.lower() for old_category in self.category_list[category_type])

        def save_category(self, category_type: str, category: str):
            category = category.strip()
            if self.category_exists(category_type, category):
                file = category_type + '.txt'
                with open(file, 'a') as writer:
                    writer.write(category + '\n')
                self.category_list[category_type].append(category)
                return True
            else:
                print(f'{category} already exists')
                return False

        def edit(self, category_type: str, old_category: str, new_category: str):
            # we want to edit the category in the list
            new_category = new_category.strip()
            if self.category_exists(category_type, new_category):
                self.category_list[category_type][self.category_list[category_type].index(old_category)] = new_category
                # write the list to the category file
                self._write_list(category_type)
                return True
            else:
                print('New category name already exists!')
                return False

        def delete(self, category_type: str, category: str):
            self.category_list[category_type].remove(category)
            self._write_list(category_type)

        def _write_list(self, category_type: str):
            file = category_type + '.txt'
            with open(file, 'w') as writer:
                for each_category in self.category_list[category_type]:
                    writer.write(each_category + '\n')

        def refresh(self):
            if 'expense.txt' in directory_files():
                self.expense_categories.clear()
                with open('expense.txt', 'r') as expenses:
                    self.expense_categories.extend(expenses.read().split())
            else:
                self.expense_categories.extend([])

            if 'income.txt' in directory_files():
                self.income_categories.clear()
                with open('income.txt', 'r') as income:
                    self.income_categories.extend(income.read().split())
            else:
                self.income_categories.extend([])

        def __str__(self):
            return f'{self!r} {self.category_list}'

    instance = None

    def __new__(cls):
        if Categories.instance is None:
            Categories.instance = Categories.__Categories()

        return Categories.instance
