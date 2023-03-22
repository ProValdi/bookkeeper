"""
Здесь содержатся тесты для виджета со списком расходов
"""
import pytest

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QPoint

from bookkeeper.view.expenses_list_widget import ExpensesListWidget


@pytest.fixture(autouse=True)
def expenses_list_widget(qtbot):
    widget = ExpensesListWidget()
    qtbot.addWidget(widget)
    return widget


def test_table(expenses_list_widget):
    """
    Проверяет верно ли, инициализируется таблица
    """
    assert expenses_list_widget.table.rowCount() == 0
    assert expenses_list_widget.table.columnCount() == 5
    assert expenses_list_widget.table.horizontalHeaderItem(0).text() == "Категория"
    assert expenses_list_widget.table.horizontalHeaderItem(1).text() == "Сумма расхода"
    assert expenses_list_widget.table.horizontalHeaderItem(2).text() == "Дата"
    assert expenses_list_widget.table.horizontalHeaderItem(3).text() == "Комментарий"
    assert expenses_list_widget.table.horizontalHeaderItem(4).text() == ""


def test_update_table(expenses_list_widget):
    """
    Проверяет верно ли, обновляется таблица
    """
    expenses_list_widget.update_table([
        {"date": "2023-03-01", "description": "Продукты", "category": "Еда", "amount": "3000.00"},
        {"date": "2023-03-02", "description": "Питса", "category": "Еда", "amount": "700.00"},
    ])
    assert expenses_list_widget.table.rowCount() == 2
    assert expenses_list_widget.table.item(0, 0).text() == "Еда"
    assert expenses_list_widget.table.item(0, 1).text() == "3000.00"
    assert expenses_list_widget.table.item(0, 2).text() == "2023-03-01"
    assert expenses_list_widget.table.item(0, 3).text() == "Продукты"
    assert expenses_list_widget.table.cellWidget(0, 4) is not None


def test_add_row(expenses_list_widget):
    """
    Проверяет, что строка успешно добавляется
    """
    initial_row_count = expenses_list_widget.table.rowCount()
    expenses_list_widget.update_table([
        {"date": "2023-03-01", "description": "Продукты", "category": "Еда", "amount": "3000.00"},
        {"date": "2023-03-02", "description": "Питса", "category": "Еда", "amount": "700.00"},
    ])
    expenses_list_widget.update_table([
        {"date": "2023-03-01", "description": "Продукты", "category": "Еда", "amount": "2000.00"},
        {"date": "2023-03-04", "description": "Такси", "category": "Транспорт", "amount": "250.00"},
        {"date": "2023-03-03", "description": "Кино", "category": "Развлечения", "amount": "500.00"},
    ])
    assert expenses_list_widget.table.rowCount() == initial_row_count + 3
    assert expenses_list_widget.table.item(2, 0).text() == "Развлечения"
    assert expenses_list_widget.table.item(2, 1).text() == "500.00"
    assert expenses_list_widget.table.item(2, 2).text() == "2023-03-03"
    assert expenses_list_widget.table.item(2, 3).text() == "Кино"


def test_delete_row(expenses_list_widget, qtbot):
    expenses = [
        {"category": "Food", "amount": "10.00", "date": "2022-01-01", "description": ""},
        {"category": "Transportation", "amount": "5.00", "date": "2022-01-02", "description": ""},
    ]
    expenses_list_widget.update_table(expenses)

    assert expenses_list_widget.table.rowCount() == 2

    delete_button = expenses_list_widget.table.cellWidget(0, 4)
    delete_button_pos = delete_button.mapToGlobal(
        QPoint(int(delete_button.width() / 2), int(delete_button.height() / 2)))
    qtbot.mouseClick(delete_button, Qt.MouseButton.LeftButton, pos=delete_button_pos)

    expenses.pop(0)

    expenses_list_widget.update_table(expenses)

    assert expenses_list_widget.table.rowCount() == 1
