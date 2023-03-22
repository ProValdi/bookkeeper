"""
Здесь содержатся тесты для виджета бюджета
"""
import pytest
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit

from bookkeeper.view.budget_widget import BudgetWidget


@pytest.fixture
def budget_widget(qtbot):
    widget = BudgetWidget()
    qtbot.addWidget(widget)
    return widget


def test_budget_widget_initial_state(budget_widget):
    assert budget_widget.month_budget_label.text() == "0.00"
    assert budget_widget.week_budget_label.text() == "0.00"
    assert budget_widget.day_budget_label.text() == "0.00"
    assert budget_widget.day_budget_edit.placeholderText() == "0.00"
    assert budget_widget.week_budget_edit.placeholderText() == "0.00"
    assert budget_widget.month_budget_edit.placeholderText() == "0.00"
    assert budget_widget.day_expenses_label.text() == "Расходы за день: 0.00"
    assert budget_widget.week_expenses_label.text() == "Расходы за неделю: 0.00"
    assert budget_widget.month_expenses_label.text() == "Расходы за месяц: 0.00"


def test_budget_widget_set_month_budget(budget_widget):
    budget_widget.set_month_budget(5000.0)
    assert budget_widget.month_budget_label.text() == "5000.00"


def test_budget_widget_set_month(budget_widget):
    budget_widget.set_month(2023, 3)
    assert budget_widget.month_label.text() == "Бюджет за марта 2023"


def test_budget_widget_update_day_budget(qtbot, budget_widget):
    budget_widget.day_budget_edit.setText("500.00")
    budget_widget.day_budget_edit.editingFinished.emit()
    qtbot.wait(500)
    assert budget_widget.day_budget_label.text() == "500.00"


def test_budget_widget_update_week_budget(qtbot, budget_widget):
    budget_widget.week_budget_edit.setText("2000.00")
    budget_widget.week_budget_edit.editingFinished.emit()
    qtbot.wait(500)
    assert budget_widget.week_budget_label.text() == "2000.00"


def test_budget_widget_update_month_budget(qtbot, budget_widget):
    budget_widget.month_budget_edit.setText("10000.00")
    budget_widget.month_budget_edit.editingFinished.emit()
    qtbot.wait(500)
    assert budget_widget.month_budget_label.text() == "10000.00"


def test_budget_widget_update_expenses_labels(budget_widget):
    budget_widget.expenses_updated.emit(100.0, 500.0, 2000.0)
    assert budget_widget.day_expenses_label.text() == "Расходы за день: 100.00"
    assert budget_widget.week_expenses_label.text() == "Расходы за неделю: 500.00"
    assert budget_widget.month_expenses_label.text() == "Расходы за месяц: 2000.00"
