from .typing import Inventory_Dist, Input_Warehouse_List, Shipment
from .warehouse import Warehouse


class InventoryAllocator(object):
    """
    Optimally create shipments of inventory to complete orders

    Attributes:
        __warhouse_list (List[Warhouse]): List of all Warehouse objects.

    """

    def __init__(self):
        """The constructor for InventoryAllocator class."""
        self.__warehouse_list = []

    def __set_warehouse_list(self, warehouse_dict_list: Input_Warehouse_List):
        """
        Creates a Warehouse object for each Warhouse_Dict in the list

        Parameters:
           warhouse_dict_list: A list of warehouses and their inventories

        """
        for inp_warehouse in warehouse_dict_list:
            self.__warehouse_list.append(
                Warehouse(inp_warehouse["name"], inp_warehouse["inventory"])
            )

    def __are_multiple_warehouses_required(self, item: str,
                                           order_quantity: int) -> bool:
        """
        Return True if multiple warehouses are needed otherwise False

        Side Effects:
            If a single warehouse can ship all of the item then it processes
            a shipment for that warehouse

        Parameters:
            item: Item to be shipped.
            order_quantity: Amount of item to be shipped.

        """
        total_amount = 0

        for warehouse in self.__warehouse_list:
            quantity_in_warehouse = warehouse.get_quantity(item)
            if quantity_in_warehouse >= order_quantity:
                # Single warehouse can ship all of the item so return False
                warehouse.process_item_shipment(item, order_quantity)
                return False
            # Keep track of total item amount across warehouses
            total_amount += quantity_in_warehouse

        return total_amount >= order_quantity

    def __process_shipment_for_item(self, item: str, order_quantity: int):
        """
        Processes a shipment for order_quantity amount of an item

        Parameters:
            item: Item to be shipped.
            order_quantity: Amount of item to be shipped.

        """
        quantity_left = order_quantity
        total_amount = 0

        # Greedily take inventory from warehouses until shipment is complete
        for warehouse in self.__warehouse_list:
            quantity_in_warehouse = warehouse.get_quantity(item)
            if quantity_in_warehouse > 0:
                shipping_quantity = min(quantity_in_warehouse,
                                        quantity_left)
                quantity_left -= shipping_quantity
                warehouse.process_item_shipment(item, shipping_quantity)
            if quantity_left <= 0:
                break

    def allocate_inventory(self, order: Inventory_Dist,
                           warehouse_dicts: Input_Warehouse_List) -> Shipment:
        """
        Returns Shipment of optimally allocated inventory

        Parameters:
            order: The order to be completed.
            warhouse_dicts: A list of warehouses and their inventories

        """
        self.__set_warehouse_list(warehouse_dicts)

        # Process all items in order into warehouse shipments
        for item, quantity in order.items():
            if quantity == 0:
                # Skip orders of 0
                continue
            if self.__are_multiple_warehouses_required(item, quantity):
                self.__process_shipment_for_item(item, quantity)

        # Combine warehouse shipments to fufill order
        shipment = []
        for warehouse in self.__warehouse_list:
            warehouse_shipment = warehouse.ship_order()
            if warehouse_shipment:
                shipment.append(warehouse_shipment)
        return shipment
