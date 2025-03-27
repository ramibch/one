"""

class SquareTests(ParametrizedTestCase):
    @parametrize(
        "x,expected",
        [
            (1, 1),
            (2, 4),
        ],
    )
    def test_square(self, x: int, expected: int) -> None:
        self.assertEqual(x**2, expected)

"""

from django import test
from unittest_parametrize import ParametrizedTestCase


class SimpleTestCase(ParametrizedTestCase, test.SimpleTestCase):
    pass


class TestCase(SimpleTestCase, test.TestCase):
    pass


class TransactionTestCase(SimpleTestCase, test.TransactionTestCase):
    pass


class LiveServerTestCase(SimpleTestCase, test.LiveServerTestCase):
    pass
