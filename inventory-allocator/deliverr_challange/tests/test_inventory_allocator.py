import unittest
from ..src.inventory_allocator import InventoryAllocator


class TestInventoryAllocator(unittest.TestCase):

    ################# Test cases where allocation is possible #################
    def test_exact_match_with_single_warehouse(self):
        order = {"apple": 1}
        warehouses = [{"name": "owd", "inventory": {"apple": 1}}]

        allocation = InventoryAllocator(order, warehouses).allocate_inventory()
        expected_result = [{"owd": {"apple": 1}}]
        self.assertEqual(allocation, expected_result)

    def test_exact_match__of_multiple_items_at_single_warehouse(self):
        order = {"apple": 1, "beans": 7, "pineapple": 8}
        warehouses = [
            {"name": "owd", "inventory": {"apple": 1, "beans": 7, "pineapple": 8}}
        ]

        allocation = InventoryAllocator(order, warehouses).allocate_inventory()
        expected_result = [{"owd": {"apple": 1, "beans": 7, "pineapple": 8}}]
        self.assertEqual(allocation, expected_result)

    def test_more_inventory_than_order_at_single_warehouse(self):
        order = {"apple": 5, "orange": 1}
        warehouses = [{"name": "owd", "inventory": {"apple": 10, "orange": 2}}]

        allocator = InventoryAllocator(order, warehouses)
        expected_result = [{"owd": {"apple": 5, "orange": 1}}]
        self.assertEqual(allocator.allocate_inventory(), expected_result)

    def test_warhouse_storing_inventory_correctly_after_shipment(self):
        order = {"apple": 5, "orange": 1}
        warehouses = [
            {"name": "owd", "inventory": {"apple": 10, "orange": 2}}]

        allocator = InventoryAllocator(order, warehouses)
        expected_result = [{"owd": {"apple": 5, "orange": 1}}]
        self.assertEqual(allocator.allocate_inventory(), expected_result)
        allocator.set_order(order)
        self.assertEqual(allocator.allocate_inventory(), expected_result)

    def test_exact_match_in_various_warehouses(self):
        order = {"apple": 1, "beans": 7, "pineapple": 8}
        warehouses = [
            {"name": "owd", "inventory": {"apple": 1}},
            {"name": "johns", "inventory": {"beans": 7}},
            {"name": "bobs", "inventory": {"pineapple": 8}},
        ]

        allocation = InventoryAllocator(order, warehouses).allocate_inventory()
        expected_result = [
            {"owd": {"apple": 1}},
            {"johns": {"beans": 7}},
            {"bobs": {"pineapple": 8}},
        ]
        self.assertEqual(allocation, expected_result)

    def test_optimal_allocation_of_single_item_exact_match(self):
        order = {"apple": 5}
        warehouses = [
            {"name": "owd", "inventory": {"apple": 5}},
            {"name": "johns", "inventory": {"apples": 10}},
            {"name": "bobs", "inventory": {"apples": 8}},
        ]

        allocation = InventoryAllocator(order, warehouses).allocate_inventory()
        expected_result = [
            {"owd": {"apple": 5}},
        ]
        self.assertEqual(allocation, expected_result)

    def test_optimal_allocation_multiple_items_exact_match(self):
        order = {"apple": 7, "beans": 7,
                 "pineapple": 8, "cheese": 10, "pasta": 9}
        warehouses = [
            {"name": "owd", "inventory": {"apple": 7, "cheese": 10}},
            {"name": "johns", "inventory": {"beans": 7, "pasta": 9, "cheese": 10}},
            {"name": "bobs", "inventory": {"apple": 7, "beans": 7,
                                           "cheese": 10, "pineapple": 8, "pasta": 9}},
        ]

        allocation = InventoryAllocator(order, warehouses).allocate_inventory()
        expected_result = [
            {"owd": {"apple": 7, "cheese": 10}},
            {"johns": {"beans": 7, "pasta": 9}},
            {"bobs": {"pineapple": 8}}
        ]
        self.assertEqual(allocation, expected_result)

    def test_optimal_allocation_over_warehouses_no_exact_match(self):
        order = {"apple": 9, "cheese": 60, "pasta": 18}
        warehouses = [
            {"name": "owd", "inventory": {"apple": 7,
                                          "beans": 2, "cheese": 10, "pineapple": 8}},
            {"name": "johns", "inventory": {"beans": 7, "pasta": 9, "cheese": 10}},
            {"name": "bobs", "inventory": {"apple": 2, "beans": 7,
                                           "cheese": 40, "pineapple": 8, "pasta": 9}},
        ]

        allocation = InventoryAllocator(order, warehouses).allocate_inventory()
        expected_result = [
            {"owd": {"apple": 7, "cheese": 10}},
            {"johns": {"pasta": 9, "cheese": 10}},
            {"bobs": {"apple": 2, "cheese": 40, "pasta": 9}},
        ]
        self.assertEqual(allocation, expected_result)

    def test_optimal_allocation_of_an_exact_match_over_partial(self):
        order = {"cheese": 30}
        warehouses = [
            {"name": "owd", "inventory": {"apple": 7, "cheese": 10}},
            {"name": "johns", "inventory": {"beans": 7, "pasta": 9, "cheese": 10}},
            {"name": "bobs", "inventory": {"apple": 7, "beans": 7,
                                           "cheese": 30, "pineapple": 8, "pasta": 9}},
        ]

        allocation = InventoryAllocator(order, warehouses).allocate_inventory()
        expected_result = [{"bobs": {"cheese": 30}}]
        self.assertEqual(allocation, expected_result)

    def test_optimal_allocation_of_partial_match_and_exact_match_in_same_order(self):
        order = {"apple": 9, "beans": 13,
                 "pineapple": 8, "cheese": 30, "pasta": 18}
        warehouses = [
            {"name": "owd", "inventory": {"apple": 7, "cheese": 10, "pineapple": 8}},
            {"name": "johns", "inventory": {"beans": 7, "pasta": 9, "cheese": 10}},
            {"name": "bobs", "inventory": {"apple": 7, "beans": 7,
                                           "cheese": 40, "pineapple": 8, "pasta": 9}},
        ]

        allocation = InventoryAllocator(order, warehouses).allocate_inventory()
        expected_result = [
            {"owd": {"apple": 7, "pineapple": 8}},
            {"johns": {"beans": 7, "pasta": 9}},
            {"bobs": {"apple": 2, "beans": 6, "cheese": 30, "pasta": 9}},
        ]
        self.assertEqual(allocation, expected_result)

    def test_optimal_allocation_full_inventory_usage(self):
        order = {"apple": 9, "beans": 16,
                 "pineapple": 16, "cheese": 60, "pasta": 18}
        warehouses = [
            {"name": "owd", "inventory": {"apple": 7,
                                          "beans": 2, "cheese": 10, "pineapple": 8}},
            {"name": "johns", "inventory": {"beans": 7, "pasta": 9, "cheese": 10}},
            {"name": "bobs", "inventory": {"apple": 2, "beans": 7,
                                           "cheese": 40, "pineapple": 8, "pasta": 9}},
        ]

        allocation = InventoryAllocator(order, warehouses).allocate_inventory()
        expected_result = [
            {"owd": {"apple": 7, "beans": 2, "cheese": 10, "pineapple": 8}},
            {"johns": {"beans": 7, "pasta": 9, "cheese": 10}},
            {"bobs": {"apple": 2, "beans": 7,
                      "cheese": 40, "pineapple": 8, "pasta": 9}},
        ]
        self.assertEqual(allocation, expected_result)

    ################# Test cases where allocation is not possible #################
    def test_item_missing(self):
        order = {"apple": 1, "chaps": 1}
        warehouses = [{"name": "owd", "inventory": {"apple": 1}}]

        allocation = InventoryAllocator(order, warehouses).allocate_inventory()
        self.assertEqual(allocation, [])

    def test_item_missing_multiple_warehouses(self):
        order = {"apple": 1, "pineapple": 6, "cheese": 2}
        warehouses = [
            {"name": "owd", "inventory": {"apple": 5}},
            {"name": "beep", "inventory": {"pineapple": 6}}]

        allocation = InventoryAllocator(order, warehouses).allocate_inventory()
        self.assertEqual(allocation, [])

    def test_first_item_missing_multiple_warehouses(self):
        order = {"apples": 1, "bapple": 6, "pineapple": 2}
        warehouses = [
            {"name": "owd", "inventory": {"bapple": 5}},
            {"name": "beep", "inventory": {"pineapple": 6}}]

        allocation = InventoryAllocator(order, warehouses).allocate_inventory()
        self.assertEqual(allocation, [])

    def test_warehouses_not_changed_on_missing_item(self):
        order = {"apple": 3, "pineapple": 6, "cheese": 2, "pizza": 12}
        warehouses = [
            {"name": "owd", "inventory": {"apple": 5, "pizza": 6}},
            {"name": "beep", "inventory": {"pineapple": 6, "pizza": 10}}
        ]

        allocator = InventoryAllocator(order, warehouses)
        self.assertEqual(allocator.allocate_inventory(), [])
        order = {"apple": 3, "pineapple": 6, "pizza": 12}
        allocator.set_order(order)
        self.assertEqual(allocator.allocate_inventory(), [
                         {"owd": {"apple": 3, "pizza": 6}},
                         {"beep": {"pineapple": 6, "pizza": 6}}
                         ])

    def test_no_inventory_at_warehouse(self):
        order = {"apple": 1}
        warehouses = [{"name": "owd", "inventory": {"apple": 0}},
                      {"name": "owds", "inventory": {"apple": 0}},
                      {"name": "owdzz", "inventory": {"apple": 0}}]

        allocation = InventoryAllocator(order, warehouses).allocate_inventory()
        self.assertEqual(allocation, [])

    def test_not_enough_inventory_one_warehouse(self):
        order = {"apple": 5, "burito": 5}
        warehouses = [{"name": "owd", "inventory": {"apple": 6, "burito": 4}}]

        allocation = InventoryAllocator(order, warehouses).allocate_inventory()
        self.assertEqual(allocation, [])

    def test_not_enough_inventory_multiple_warehouse(self):
        order = {"apple": 10, "burito": 50, "carrot": 10}
        warehouses = [
            {"name": "owd", "inventory": {"apple": 1, "burito": 4, "carrot": 1}},
            {"name": "zeep", "inventory": {"apple": 2, "burito": 4, "carrot": 5}},
            {"name": "zeepa", "inventory": {"apple": 2, "burito": 4}},
            {"name": "zeepv", "inventory": {"apple": 2, "burito": 20}},
            {"name": "zeepc", "inventory": {"apple": 2, "burito": 10, "carrot": 1}}
        ]

        allocation = InventoryAllocator(order, warehouses).allocate_inventory()
        self.assertEqual(allocation, [])

    def test_not_enough_inventory_random_item_multiple_warehouse(self):
        order = {"apple": 10, "burito": 50, "carrot": 10}
        warehouses = [
            {"name": "owd", "inventory": {"apple": 1, "burito": 4, "carrot": 1}},
            {"name": "zeep", "inventory": {"apple": 2, "burito": 4, "carrot": 5}},
            {"name": "zeepa", "inventory": {"apple": 5, "burito": 4}},
            {"name": "zeepv", "inventory": {"apple": 2, "burito": 20}},
            {"name": "zeepc", "inventory": {"apple": 2, "burito": 10, "carrot": 6}}
        ]

        allocation = InventoryAllocator(order, warehouses).allocate_inventory()
        self.assertEqual(allocation, [])

    def test_order_nothing(self):
        order = {"apple": 0, "burito": 0, "carrot": 0}
        warehouses = [
            {"name": "owd", "inventory": {"apple": 1, "burito": 4, "carrot": 1}},
            {"name": "zeep", "inventory": {"apple": 2, "burito": 4, "carrot": 5}},
            {"name": "zeepa", "inventory": {"apple": 2, "burito": 4}},
            {"name": "zeepv", "inventory": {"apple": 2, "burito": 20}},
            {"name": "zeepc", "inventory": {"apple": 2, "burito": 10, "carrot": 1}}
        ]

        allocation = InventoryAllocator(order, warehouses).allocate_inventory()
        self.assertEqual(allocation, [])


if __name__ == "__main__":
    unittest.main()
