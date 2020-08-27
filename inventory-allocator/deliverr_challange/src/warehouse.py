from .typing import Inventory_Dist, Warehouse_Shipment
from copy import deepcopy


class Warehouse(object):
    """
    A warehouse to store inventory, process shipments and ship them.

    Attributes:
        __name (str): Name of the warehouse.
        __inventory (Inventory_Dist): Inventory available in warehouse.
        __to_be_shipped (Inventory_Dist): Inventory processed to be shipped.

    """

    def __init__(self, name: str, inventory: Inventory_Dist):
        """
        The constructor for Warehouse class.

        Parameters:
           name (str): The name given to warehouse.
           inventory (int): The inventory given to warehouse.

        """
        self.__name = name
        self.__inventory = inventory
        self.__to_be_shipped = {}

    def __is_item_in_stock(self, item: str) -> bool:
        """Return True if item is in inventory, False otherwise"""
        return item in self.__inventory and self.__inventory[item] > 0

    def get_quantity(self, item: str) -> int:
        """Returns an int which is quantity of item in inventory currently"""
        if not self.__is_item_in_stock(item):
            return 0
        return self.__inventory[item]

    def process_item_shipment(self, item: str, quantity: int):
        """
        Create a shipment for an item using warehouse inventory

        Parameters:
            item (str): Item to be ordered.
            quantity (int): Amount of item to be ordered.

        """
        if quantity > 0 and self.__is_item_in_stock(item):
            self.__to_be_shipped[item] = min(self.get_quantity(item), quantity)
            self.__inventory[item] -= self.__to_be_shipped[item]

    def ship_order(self) -> Warehouse_Shipment:
        """Return created warhouse shipment, from inventory to be shipped"""
        if not self.__to_be_shipped:
            return {}
        else:
            return {self.__name: self.__to_be_shipped}
