from typing import TypedDict, Dict,  List

Inventory_Dist = Dict[str, int]
Input_Warehouse = TypedDict("Warehouse_Dict_List",
                            {"name": str, "inventory": Inventory_Dist})
Input_Warehouse_List = List[Input_Warehouse]
Warehouse_Shipment = Dict[str, Inventory_Dist]
Shipment = List[Warehouse_Shipment]
