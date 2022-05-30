import pytest

pytestmark = pytest.mark.django_db


class TestMenu:
    def test_menuentry(self, menuentry_factory):
        menuentry = menuentry_factory()
        assert menuentry.pizza.name == "Tonno"
        assert menuentry.restaurant.name == "Pizzeria Empty"
