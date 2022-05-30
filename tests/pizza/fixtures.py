from typing import Callable

import pytest

from pizza.models import Topping, Pizza


@pytest.fixture(scope="session")
def topping_factory() -> Callable[..., Topping]:
    def _factory(**kwargs):
        return Topping.objects.create(**kwargs)

    _factory.model = Topping
    return _factory


@pytest.fixture(scope="session")
def pizza_factory() -> Callable[..., Pizza]:
    def _factory(**kwargs):
        toppings = kwargs.pop("toppings", [])
        pizza = Pizza.objects.create(**kwargs)
        if toppings:
            for topping_name in toppings:
                topping, _ = Topping.objects.get_or_create(name=topping_name)
                pizza.toppings.add(topping)
        return pizza

    _factory.model = Pizza
    return _factory


@pytest.fixture
def pizza_margherita(db, pizza_factory):
    return pizza_factory(name="Margherita", toppings=["Tomato", "Mozzarella"])


@pytest.fixture
def pizza_margherita(db, pizza_factory):
    return pizza_factory(name="Margherita", toppings=["Tomato", "Mozzarella"])


@pytest.fixture
def pizza_tonno(db, pizza_factory):
    return pizza_factory(name="Tonno", toppings=["Tuna", "Onions", "Cheese"])
