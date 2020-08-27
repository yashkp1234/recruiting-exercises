from copy import deepcopy
from .typing import Inventory_Dist, Warehouse_Shipment


class Warehouse(object):
    """A warehouse to store inventory, process shipments and ship them.

    Attributes:
        __name (str): Name of the warehouse.
        __inventory (Inventory_Dist): Inventory available in warehouse.
        __to_be_shipped (Inventory_Dist): Inventory processed to be shipped.

    """

    def __init__(self, name: str, inventory: Inventory_Dist):
        """The constructor for Warehouse class.

        Parameters:
           name (str): The name given to warehouse.
           inventory (int): The inventory given to warehouse.

        """
        self.__name = name
        self.__inventory = deepcopy(inventory)
        self.__to_be_shipped = {}

    def __clear_temp_orders(self):
        """Remove all processed orders"""
        self.__to_be_shipped = {}

    def __is_item_in_stock(self, item: str) -> bool:
        """ Return True if item is in inventory, False otherwise"""
        return item in self.__inventory and self.__inventory[item] > 0

    def get_quantity(self, item: str) -> int:
        """Returns an int which is quantity of item in inventory currently"""
        if not self.__is_item_in_stock(item):
            return 0
        return self.__inventory[item]

    def process_item_shipment(self, item: str, quantity: int):
        """Create a shipment for an item using warehouse inventory

        Parameters:
            item (str): Item to be ordered.
            quantity (int): Amount of item to be ordered.

        """
        if quantity > 0 and self.__is_item_in_stock(item):
            self.__to_be_shipped[item] = min(self.get_quantity(item),
                                             quantity)
            self.__inventory[item] -= self.__to_be_shipped[item]

    def cancel_processed_shipments(self):
        """Cancel all processed shipments and restore items in inventory"""
        for item in self.__to_be_shipped:
            self.__inventory[item] += self.__to_be_shipped[item]
        self.__clear_temp_orders()

    def ship_order(self) -> Warehouse_Shipment:
        """Return created warhouse shipment, from inventory to be shipped"""
        order = self.__to_be_shipped
        self.__clear_temp_orders()

        if not order:
            return {}
        else:
            return {self.__name: order}
