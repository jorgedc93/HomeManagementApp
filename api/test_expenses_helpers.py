import random
import unittest
from unittest.mock import patch

from api import expenses_helpers
from api.config import app
from api.test_utils import generate_random_expenses


@patch("api.expenses_helpers.mongo")
class TestExpensesHelpers(unittest.TestCase):

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_get_expenses_list(self, mock_mongo):
        """ Test that getting a list of expenses works as expected """
        random_expenses = generate_random_expenses(random.randint(1, 10))

        mock_mongo.db.expenses.find.return_value = random_expenses

        response_expenses = expenses_helpers.get_expense_list()

        # We assert that it returns the expected number of expenses
        self.assertEqual(len(random_expenses), len(response_expenses))

        # And we assert that the users are the same
        for expense in response_expenses:
            self.assertIn(expense, random_expenses)


if __name__ == '__main__':
    unittest.main()
