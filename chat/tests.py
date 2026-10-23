from decimal import Decimal

from django.test import TestCase

from .models import Item
from .tools import adjust_price_by_percentage


class InventoryPriceAdjustmentTests(TestCase):
    def test_increase_price_by_percentage(self):
        item = Item.objects.create(name='Chocolate Bar', quantity=10, price=Decimal('10.00'))

        result = adjust_price_by_percentage('Chocolate Bar', 50)

        self.assertEqual(result['name'], 'Chocolate Bar')
        item.refresh_from_db()
        self.assertEqual(item.price, Decimal('15.00'))
        self.assertEqual(result['price'], '15.00')
