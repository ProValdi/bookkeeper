"""
Модуль содержит класс виджета расходов
для отображения информации о расходах таблицей.
"""
from datetime import datetime
from typing import cast, List, Dict, Tuple, Union

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QWidget,
    QVBoxLayout,
    QPushButton, QComboBox, QInputDialog, QMessageBox,
)

FLAGS_EN_SEL_EDIT: Union[Qt.ItemFlags, Qt.ItemFlag] = Union[Qt.ItemFlag.ItemIsEnabled,
                                                            Qt.ItemFlag.ItemIsSelectable,
                                                            Qt.ItemFlag.ItemIsEditable]

FLAGS_EN_SEL: Union[Qt.ItemFlags, Qt.ItemFlag] = Union[Qt.ItemFlag.ItemIsEnabled, Qt.ItemFlag.ItemIsSelectable]


class ExpensesListWidget(QWidget):
    """
    Виджет для отображения таблицы расходов.
    """

    delete_button_clicked = pyqtSignal(int)
    category_cell_double_clicked = pyqtSignal(int, int, str)
    category_cell_changed = pyqtSignal(int, int, int)
    expense_cell_changed = pyqtSignal(int, int, str)

    def __init__(self) -> None:
        super().__init__()

        self.table = QTableWidget()
        self.init_table()
        self.update_table([])

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.table.cellDoubleClicked.connect(self._on_cell_double_clicked)

    def init_table(self) -> None:
        """
        Инициализирует таблицу, на которой будут
        отображаться данные о расходах.
        """
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Категория", "Сумма расхода", "Дата", "Комментарий", ""])
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents)

        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                if col == 0:
                    self.table.item(row, col).setFlags(FLAGS_EN_SEL)
                else:
                    self.table.item(row, col).setFlags(FLAGS_EN_SEL_EDIT)

    def update_table(self, expenses: List[Dict[str, str]]) -> None:
        """
        Обновляет содержимое ExpensesListWidget
        полученным списком
        """
        self.table.clearContents()
        self.table.setRowCount(len(expenses))
        for row, expense in enumerate(expenses):
            category_item = QTableWidgetItem(expense["category"])
            amount_item = QTableWidgetItem(str(expense["amount"]))
            date_item = QTableWidgetItem(expense["date"])
            description_item = QTableWidgetItem(expense["description"])
            delete_button = QPushButton("Удалить")
            delete_button.clicked.connect(self.delete_row)

            self.table.setItem(row, 0, category_item)
            self.table.setItem(row, 1, amount_item)
            self.table.setItem(row, 2, date_item)
            self.table.setItem(row, 3, description_item)
            self.table.setCellWidget(row, 4, delete_button)

    def _on_cell_double_clicked(self, row: int, column: int) -> None:
        """
        Двойным нажатием вызывает QInputDialog,
        где можно обновить значения объекта Expense
        """
        if column in (1, 3):
            item = self.table.item(row, column)
            new_value, ok_dialog = QInputDialog.getText(self,
                                                        "Изменение значения",
                                                        "Введите новое значение:",
                                                        text=item.text())
            if ok_dialog:
                self.expense_cell_changed.emit(row, column, new_value)

        elif column == 2:
            item = self.table.item(row, column)
            new_value, ok_dialog = QInputDialog.getText(self,
                                                        "Изменение значения",
                                                        "Введите новое значение:",
                                                        text=item.text())
            if ok_dialog:
                try:
                    datetime.strptime(new_value, "%Y-%m-%d")
                    self.expense_cell_changed.emit(row, column, new_value)
                except ValueError:
                    QMessageBox.warning(self, "Ошибка ввода даты",
                                        "Введите дату в формате YYYY-MM-DD")
                    self.table.setItem(row, column, QTableWidgetItem(item.text()))

        elif column == 0:
            item = self.table.item(row, column)
            self.category_cell_double_clicked.emit(row, column, item.text())

    def update_category_cell(self,
                             row: int,
                             column: int,
                             categories: List[Tuple[int, str]]) -> None:
        """
        Создаёт на месте ячейки QComboBox,
        и заполняет его категориями
        """

        combo_box = QComboBox()
        self.categories = categories
        combo_box.insertSeparator(0)

        categories_sorted = sorted(categories, key=lambda x: x[0])

        combo_box.addItems([name for _, name in categories_sorted])
        self.table.setCellWidget(row, column, combo_box)

        combo_box.currentIndexChanged.connect(
            lambda index, row=row, column=column, categories=categories_sorted:
            self.category_cell_changed.emit(row, column, categories[index - 1][0]))

        self.table.setCellWidget(row, column, combo_box)

    def delete_row(self) -> None:
        """
        Удаляет строку с выбранным расходом из списка расходов
        и обновляет содержимое таблицы.
        """
        delete_button: QPushButton = cast(QPushButton, self.sender())
        index: int = self.table.indexAt(delete_button.pos()).row()
        print(index)
        if index >= 0:
            self.delete_button_clicked.emit(index)


class EditableTableWidgetItem(QTableWidgetItem):
    """
    QTableWidgetItem, который допускает редактирование ячеек таблицы ExpenseListWidget
    """

    def __init__(self, text: str) -> None:
        super().__init__(text)

    def flags(self) -> Qt.ItemFlags:
        """
        Устанавливает флаги для ячеек таблицы
        """
        return super().flags() | Qt.ItemFlag.ItemIsEditable
