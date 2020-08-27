# Deliverr Challange

## Testing

The tests must be run from the deliverr_challange folder.
To get there from root directory do the following

```sh
$ cd inventory-allocator/deliverr_challange
```

To run the unit tests run the following, with expected results below

```python
$ python -m unittests
.......................
----------------------------------------------------------------------
Ran 26 tests in 0.001s

OK
```

For custom test cases you may wish to add, just simply add them into test\test_inventory_allocator.py file.<br/>
Format the test case similar to the one below.

```python
    def test_exact_match_with_single_warehouse(self):
        order = {"apple": 1}
        warehouses = [{"name": "owd", "inventory": {"apple": 1}}]

        allocation = InventoryAllocator(order, warehouses).allocate_inventory()
        expected_result = [{"owd": {"apple": 1}}]
        self.assertEqual(allocation, expected_result)
```

## Assumptions Made

- If an item from an order cannot be fufilled, then the rest of the order should still completed as much as possible
  - Example
    - Given an inventory of {apple: 2, pear: 1} and warehouse list of [{name: test, inventory: {pear: 1}}]
    - This should result in [{test: {pear: 1}}] not [], as although the apple shipment cannot be fufilled, the pears can
  - Reasoning
    - In an email sent to technical recruiter, she clarified that this was the case
- It is always cheaper to allocate the shipment of an item to the n cheapest warehouses than it is to allocate to m warehouses who have higher costs, where m < n
  - Example
    - Consider warehouses with costs of [1, 2, 3, 4, 5, 6, 7], the index of the warehouse is its name and cost, and we have an order of 5 apples
    - Warehouses 1 to 5 combined have 5 apples and would cost 1 + 2 + 3 + 4 + 5 = 15 to ship from
    - Warehouses 6 to 7 also have 5 apples combined and would cost of 6 + 7 = 13 to ship from which is cheaper
    - Thus without this assumption we would have to consider cases like these
  - Reasoning:
    - Without knowing the actual costs of using each warehouse it would be impossible to be able to optimally allocate without making an assumption similar to this

## Implementation

Let W represent the number of warehouses, let I represent the number of items in an order

1. Create list of Warehouse objects given the second input which is a list of dictionaries with names and inventory distributions representing warehouses
   - Time: O(W)
2. Loop through order and for each item call process_shipment_for_item
   - process_shipment_for_item loops through the warehouses once to see if one warehouse and cover the item order and creates it, if it cannot and it is possible to create a distributed shipment across warehouses then it loops through warehouses again to create the distributed shipment
     - Time: O(2W)
   - Total Time: O(I) \* O(2W) = O(2IW)
3. Loop through all warehouses, output any shipments they have processed and append them to a list representing final shipment of the order
   - Time: O(W)

Total Time = O(W) + O(2WI) + O(W) = O(2WI + 2W) = O(WI)<br/>
**Thus, the overall implementation time is O(WI)**