from .typing import Inventory_Dist, Input_Warehouse_List, Shipment
from .warehouse import Warehouse


class InventoryAllocator(object):
    """
    Optimally create shipments of inventory to complete orders

    Attributes:
        __warhouse_list (List[Warhouse]): List of all Warehouse objects.

    """

    def __init__(self):
        self.__warehouse_list = []

    def __create_warehouse_list(self, warehouse_dict_list: Input_Warehouse_List):
        """
        Creates a Warehouse object for each Warhouse_Dict in the list

        Parameters:
           warhouse_dict_list: A list of dicts mapping warehouse names to inventories

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
            a shipment for item from that warehouse and returns False

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

    def __process_item_shipments_across_warehouses(self, item: str,
                                                   order_quantity: int):
        """
        Process item shipments across warehouses for order_quantity amount

        Parameters:
            item: Item to be shipped.
            order_quantity: Amount of item to be shipped.

        """
        quantity_left = order_quantity

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
            warhouse_dicts: A list of dicts mapping warehouse names and to inventories

        """
        self.__create_warehouse_list(warehouse_dicts)

        # Process all items in order into warehouse shipments
        for item, quantity in order.items():
            if quantity == 0:
                # Skip orders of 0
                continue
            if self.__are_multiple_warehouses_required(item, quantity):
                # No warehouse can fully complete shipment and distributed shipment is possible
                self.__process_item_shipments_across_warehouses(item, quantity)

        # Combine warehouse shipments to fufill order
        shipment = []
        for warehouse in self.__warehouse_list:
            warehouse_shipment = warehouse.ship_processed_shipments()
            if warehouse_shipment:
                shipment.append(warehouse_shipment)
        return shipment
