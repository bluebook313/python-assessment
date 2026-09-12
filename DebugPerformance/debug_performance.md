# Code Review: Debug, Performance & Complexity

## First Code: `get_customer_orders`

```python
def get_customer_orders(customers, orders):
    result = []

    for customer in customers:
        customer_orders = []

        for order in orders:
            if order.customer_id == customer.id:
                customer_orders.append(order)

        result.append({
            "customer": customer,
            "orders": customer_orders
        })

    return result
```

### 🐛 Problems

- **Problem:** For every customer, all orders are checked again.
- **Result:** As data grows, the number of checks becomes very large.
- **Solution:** Group orders once by `customer_id` in a dict, then look them up directly.

---

## ✅ Simpler Solution

Check orders only **once** and group them by `customer_id`.

```python
def get_customer_orders(customers, orders):
    orders_by_customer = {}

    for order in orders:
        orders_by_customer.setdefault(order.customer_id, []).append(order)

    result = []

    for customer in customers:
        result.append({
            "customer": customer,
            "orders": orders_by_customer.get(customer.id, [])
        })

    return result
```

---

## 🎯 Complexity in Simple Terms

### Current Approach

For **each customer**, all orders are checked.

So as customers and orders grow, checks grow very fast.

```text
10 customers × 100 orders = 1,000 checks
1000 customers × 10000 orders = 10,000,000 checks
```

### Optimized Approach

1. Orders are checked only **once**.
2. Customers are checked only **once**.
3. A dictionary is used to find each customer's orders directly.