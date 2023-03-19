"""
Модуль содержит класс главного окна приложения Bookkeeper
"""
from PyQt5.QtWidgets import QMainWindow, QTabWidget


class MainWindow(QMainWindow):
    """
    Виджет для отображения главного окна.
    """

    def __init__(self) -> None:
        super().__init__()

        # создаёт QTabWidget для хранения различных виджетов
        tab_widget = QTabWidget()

        # виджет вкладок в качестве центрального виджета главного окна
        self.setCentralWidget(tab_widget)
        self.presenter = None
