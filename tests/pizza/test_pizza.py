import pytest

from pizza.models import Topping

pytestmark = pytest.mark.django_db


class TestToppingModel:
    def test_topping_query(self, topping_factory):
        topping_factory(name="Mozzarella")
        topping_factory(name="Salami")
        assert set(Topping.objects.values_list("name", flat=True)) == {
            "Mozzarella",
            "Salami",
        }


class TestPizzaModel:
    def test_pizza_toppings(self, pizza_factory):
        pizza = pizza_factory(name="Margherita", toppings=["Tomato", "Mozzarella"])
        assert set(pizza.toppings.values_list("name", flat=True)) == {
            "Tomato",
            "Mozzarella",
        }
