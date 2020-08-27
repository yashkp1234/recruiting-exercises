from .warehouse import Warehouse
from .typing import Inventory_Dist, Input_Warehouse_List, Shipment


class InventoryAllocator(object):
    """Optimally create shipments of inventory to complete orders

    Attributes:
        __order (Inventory_Dist): The order to be completed.
        __warhouse_list (List[Warhouse]): List of all warehouse objects.

    """

    def __init__(self, order: Inventory_Dist,
                 warehouse_dicts: Input_Warehouse_List):
        """The constructor for InventoryAllocator class.

        Parameters:
           order: The order to be completed.
           warhouse_dicts: A list of warehouses and their inventories 

        """
        self.__order = order
        self.__warehouse_list = []
        self.__set_warehouse_list(warehouse_dicts)

    def __set_warehouse_list(self, warehouse_dict_list: Input_Warehouse_List):
        """Creates a Warehouse object for each Warhouse_Dict in the list

        Parameters:
           warhouse_dict_list: A list of warehouses and their inventories

        """
        for inp_warehouse in warehouse_dict_list:
            self.__warehouse_list.append(
                Warehouse(inp_warehouse["name"], inp_warehouse["inventory"])
            )

    def __can_process_shipment_for_item(self, item: str,
                                        order_quantity: int) -> bool:
        """Return True if possible to process an shipment for item, False otherwise

        Side Effects:  
            If it is possible to process an shipment for an item, the order
            will be processed by all required Warehouses

        Parameters:
            item (str): Item to be shipped.
            order_quantity (int): Amount of item to be shipped.

        """
        running_shipments = []
        quantity_left = order_quantity

        for warehouse in self.__warehouse_list:
            quantity_in_warehouse = warehouse.get_quantity(item)

            if quantity_in_warehouse >= order_quantity:
                # Single warehouse can ship all of the item quantity
                warehouse.process_item_shipment(item, order_quantity)
                return True
            elif quantity_left > 0 and quantity_in_warehouse > 0:
                # Add partial shipments to running_shipments
                shipping_quantity = min(quantity_in_warehouse, quantity_left)
                quantity_left -= shipping_quantity
                running_shipments.append((warehouse, shipping_quantity))

        if quantity_left > 0:
            # Unable to complete the order
            return False
        for warehouse_shipment_for_item in running_shipments:
            warehouse, shipment_quantity = warehouse_shipment_for_item
            warehouse.process_item_shipment(item, shipment_quantity)
        return True

    def __cancel_all_processed_shipments(self):
        """Loop through each warehouses and cancel all processed shippments in it"""
        for warehouse in self.__warehouse_list:
            warehouse.cancel_processed_shipments()

    def set_order(self, input_order: Inventory_Dist):
        """Set order to the input_order"""
        self.__order = input_order

    def allocate_inventory(self) -> Shipment:
        """Returns Shipment of optimally allocated inventory if possible 

        Side Effects:
            If shipment is not possible then all processed shipments in each 
            warehouse in __warehouse_list is cancelled
            If shipment is possible then inventory is reduced in each 
            warehouse from which inventory was taken in __warehouse_list
            and processed shipments are cleared and shipped

        """
        # Try to process all items in order into warehouse shipments
        for item, quantity in self.__order.items():
            if quantity == 0:
                # Skip orders of 0
                continue
            elif not self.__can_process_shipment_for_item(item, quantity):
                self.__cancel_all_processed_shipments()
                return []

        # All items successfully processed so shipment can be sent
        shipment = []
        for warehouse in self.__warehouse_list:
            warehouse_shipment = warehouse.ship_order()
            if warehouse_shipment:
                shipment.append(warehouse_shipment)
        return shipment
