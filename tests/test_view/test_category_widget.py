"""
Здесь содержатся тесты для виджета со списком категорий
"""
import pytest
from PyQt5 import QtTest
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidgetItem
from bookkeeper.view.category_widget import CategoryWidget


@pytest.fixture(autouse=True)
def category_widget(qtbot):
    widget = CategoryWidget()
    qtbot.addWidget(widget)
    return widget


def test_add_existing_category(category_widget, qtbot):
    category_widget.name_edit.setText("Категория")
    item = QListWidgetItem("Категория")
    category_widget.list.addItem(item)

    with qtbot.assertNotEmitted(category_widget.add_category_signal):
        qtbot.mouseClick(category_widget.add_button, Qt.MouseButton.LeftButton)


def test_delete_category(category_widget, qtbot):
    item = QListWidgetItem("Категория")
    category_widget.list.addItem(item)
    category_widget.list.setCurrentItem(item)

    with qtbot.waitSignal(category_widget.delete_category_signal, timeout=1000):
        qtbot.mouseClick(category_widget.delete_button, Qt.MouseButton.LeftButton)

    items = [category_widget.list.item(i).text() for i in range(category_widget.list.count())]
    assert "Категория" not in items


def test_init_category_list(category_widget, qtbot):
    categories = ["Кушать 3", "Кушать 1", "Кушать 2"]
    category_widget.init_category_list(categories)

    items = [category_widget.list.item(i).text() for i in range(category_widget.list.count())]
    assert items == ["Кушать 1", "Кушать 2", "Кушать 3"]


def test_add_category(category_widget, qtbot):
    def test_add_category(category_widget, qtbot):
        # Enter category name
        category_widget.name_edit.setText("New Category")

        # Simulate user input to enable button
        category_widget.on_name_edit_changed("New Category")

        # Make add button visible
        category_widget.add_button.setVisible(True)

        print(f"add button enabled: {category_widget.add_button.isEnabled()}")
        print(f"add button visible: {category_widget.add_button.isVisible()}")

        with qtbot.waitSignal(category_widget.add_category_signal, timeout=1000) as blocker:
            # Click add button
            qtbot.mouseClick(category_widget.add_button, Qt.MouseButton.LeftButton)

            # Check if add_category_signal is emitted
            assert blocker.signal_triggered

        # Debug statement to check if category is added to list
        print(f"category added to list: {category_widget.list.item(0).text()}")

        # Wait for category to be added to list
        qtbot.waitUntil(lambda: category_widget.list.count() == 1, timeout=1000)
