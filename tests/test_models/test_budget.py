from datetime import datetime
from bookkeeper.models.budget import Budget
from bookkeeper.repository.memory_repository import MemoryRepository

import pytest


@pytest.fixture
def repo():
    return MemoryRepository()


class TestBudget:

    def test_create_for_current_month_new_budget(self, repo):
        budget = Budget.create_for_current_month(1000, repo)
        assert self._compare_datetime(budget.term, datetime.now()).__eq__(True)
        assert budget.amount == 1000
        assert budget.pk != 0
        assert budget.comment == ''
        assert repo.get(budget.pk) == budget

    def test_create_for_current_month_existing_budget(self, repo):
        existing_budget = Budget(datetime.now(), 1000)
        repo.add(existing_budget)
        budget = Budget.create_for_current_month(1000, repo)
        budget.term = budget.term.replace(microsecond=1)
        budget.added_date = budget.added_date.replace(microsecond=1)
        existing_budget.term = existing_budget.term.replace(microsecond=1)
        existing_budget.added_date = existing_budget.added_date.replace(microsecond=1)
        budget.pk = 1
        existing_budget.pk = 1
        assert budget == existing_budget

    def test_create_for_current_month_with_comment(self, repo):
        budget = Budget.create_for_current_month(1000, repo, comment='test')

        assert self._compare_datetime(budget.term, datetime.now()).__eq__(True)

        assert budget.amount == 1000
        assert budget.pk != 0
        assert budget.comment == 'test'
        assert repo.get(budget.pk) == budget

    @staticmethod
    def _compare_datetime(datetime_1: datetime, datetime_2: datetime) -> bool:
        return datetime_1.year == datetime_2.year and \
               datetime_1.month == datetime_2.month and \
               datetime_1.day == datetime_2.day and \
               datetime_1.fold == datetime_2.fold and \
               datetime_1.hour == datetime_2.hour and \
               datetime_1.minute == datetime_2.minute
