from typing import Callable

import pytest

from restaurant.models import Restaurant, MenuEntry


@pytest.fixture(scope="session")
def restaurant_factory() -> Callable[..., Restaurant]:
    def _factory(**kwargs) -> Restaurant:
        return Restaurant.objects.create(**kwargs)

    _factory.model = Restaurant
    return _factory


@pytest.fixture
def pizzeria(db, restaurant_factory):
    return restaurant_factory(name="Pizzeria Empty")


@pytest.fixture
def menuentry_factory(pizzeria, pizza_tonno) -> Callable[..., MenuEntry]:
    defaults = {"restaurant": pizzeria, "pizza": pizza_tonno, "price": 4}

    def _factory(**kwargs):
        return MenuEntry(**(defaults | kwargs))

    return _factory
