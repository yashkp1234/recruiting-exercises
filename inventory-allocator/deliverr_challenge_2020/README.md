# Deliverr Challenge

## Testing

The tests must be run from the deliverr_challenge folder.
To get there from root directory (/recruiting-exercises) do the following

```sh
$ cd inventory-allocator/deliverr_challenge
```

To run the unit tests run the following, with expected results below

```python
$ python -m unittests
.......................
----------------------------------------------------------------------
Ran 27 tests in 0.001s

OK
```

For custom test cases you may wish to add, put them into test\test_inventory_allocator.py file.<br/>
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

- If an item from an order cannot be fulfilled, then I assume that the rest of the order should still completed as much as possible
  - Example
    - Given an inventory of {apple: 2, pear: 1} and warehouse list of [{name: test, inventory: {pear: 1}}]
    - This should result in [{test: {pear: 1}}] not [], as although the apple shipment cannot be fulfilled, the pears can
  - Reasoning
    - In an email sent to technical recruiter, she clarified that this was the case
- Let n, m, k be integers where n > k > m. Consider a list of n warehouses, where there are k cheapest warehouses and m more expensive warehouses. I assume that it is always cheaper to allocate a shipment of an item to the k cheapest warehouses rather than the m expensive warehouses if more than one warehouse is needed for the shipment
  - Example
    - Consider warehouses with costs of [1, 2, 3, 4, 5, 6, 7], the index of the warehouse is its name and cost, and we have an order of 5 apples
    - Warehouses 1 to 5 combined have 5 apples and would cost 1 + 2 + 3 + 4 + 5 = 15 to ship from
    - Warehouses 6 to 7 also have 5 apples combined and would cost of 6 + 7 = 13 to ship from, which means using the m expensive warehouses would be cheaper
    - However, if we change our groupings where we have Warehouses 1 to 4 (cost is 10) and Warehouses 5 to 6 (cost is 11) then optimal shipment would use the k cheaper warehouses
    - Thus, we need to know the cost of using an individual warehouse to optimally allocate a shipment across warehouses
  - Reasoning:
    - Since we do not know the actual costs of using each warehouse it is impossible to optimally allocate inventory without making an assumption similar to this

## Implementation

Let W represent the number of warehouses, let I represent the number of items in an order

1. Create list of Warehouse objects given the second input which is a list of dictionaries with names and inventory distributions representing warehouses
   - Time: O(W)
2. Loop through order and for each item and quantity ...
   - Loop through warehouses once to check if the item requires multiple warehouses to complete a shipment.<br/> If needed then loop through warehouses again to create the shipments across warehouses for the item, otherwise we either already processed a shipment using only one warehouse or it is not possible to ship the item.
     - Time: O(2W)
   - Total Time: O(I) \* O(2W) = O(2IW)
3. Loop through all warehouses, output any shipments they have processed and append them to a list representing final shipment of the order
   - Time: O(W)

Total Time = O(W) + O(2WI) + O(W) = O(2WI + 2W) = O(WI)<br/>
**Thus, the overall implementation time is O(WI)**

## Design Decisions

- Why use a warehouse class and create warehouse objects when it takes an extra O(W) time to do so?
  - I interpreted this challenge as more of a design challenge than optimization. In reality there’s a lot of short cuts I could have taken such as writing the inventory allocation as one class, or using the warehouse list as given to avoid the extra O(W) of creating warehouses. However, I didn't because I took the perspective that this is a real-world problem and the way I solve this problem should be correct and efficient, but also well designed for scalability and to allow for future improvements and additions while being easily maintainable.
  - In order to achieve this I tried to follow OOP principles by creating the Warehouse class, and making “private” variables and methods (nothing is really private in python but \_\_ is convention for it). I believe the Warehouse class helps modularize my code making it easier to find errors, have better readability, and helps it be scalable. Specifically, adding new features such as being able to use the same warehouse list to complete multiple orders could easily be implemented currently the way my project is structured. In fact, it was implemented when I first commited, before I decided to just do what was asked in the challenge.
