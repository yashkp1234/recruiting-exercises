import unittest
from ..src.warehouse import Warehouse


class TestWarehouse(unittest.TestCase):

    def test_exact_number_items(self):
        apple_warehouse = Warehouse(name="Farmers", inventory={"apple": 1})
        apple_warehouse.process_item_shipment("apple", 1)
        self.assertEqual(apple_warehouse.ship_order(),
                         {"Farmers": {"apple": 1}})

    def test_non_existant_item(self):
        apple_warehouse = Warehouse(name="Farmers", inventory={"apple": 1})
        apple_warehouse.process_item_shipment("pear", 1)
        self.assertEqual(apple_warehouse.ship_order(), {})

    def test_ran_out_of_item(self):
        apple_warehouse = Warehouse(name="Farmers", inventory={"apple": 0})
        apple_warehouse.process_item_shipment("apple", 1)
        self.assertEqual(apple_warehouse.ship_order(), {})

    def test_more_than_available(self):
        apple_warehouse = Warehouse(name="Farmers", inventory={"apple": 5})
        apple_warehouse.process_item_shipment("apple", 6)
        self.assertEqual(apple_warehouse.ship_order(),
                         {"Farmers": {"apple": 5}})

    def test_less_than_available(self):
        apple_warehouse = Warehouse(name="Farmers", inventory={"apple": 5})
        apple_warehouse.process_item_shipment("apple", 3)
        self.assertEqual(apple_warehouse.ship_order(),
                         {"Farmers": {"apple": 3}})

    def ship_nothing(self):
        apple_warehouse = Warehouse(name="Farmers", inventory={"apple": 5})
        apple_warehouse.process_item_shipment("apple", 0)
        self.assertEqual(apple_warehouse.ship_order(), {})


if __name__ == "__main__":
    unittest.main()
