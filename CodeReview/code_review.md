# Code Review: `process_order`

## 📌 Code Under Review

```python
def process_order(order):
    try:
        if order.status == "paid":
            send_email(order.customer.email)
            charge_account(order.customer.id, order.total)
            update_shipping(order)
            order.status = "completed"
            save(order)
    except Exception:
        pass
```

---

## 🐛 Issues

### 🔴 Issue 1: Swallowing Errors (`except: pass`)

No logs are recorded; debugging becomes impossible.

---

### 🔴 Issue 2: Lack of Transaction / Rollback

The operation is multi-step, and if an error occurs midway, the system is left in an inconsistent state. For example, if `charge_account` succeeds but `save` fails → money is deducted but the order is not recorded!

---

### 🔴 Issue 3: Improper Order of Operations

`send_email` is executed before `charge_account`; if the charge fails, an incorrect email has already been sent.

---

### 🔴 Issue 4: Using a Generic `except Exception`

Programming errors (such as `AttributeError`) are also hidden, making bugs harder to detect.

---

### 🔴 Issue 5: Lack of Separation of Responsibilities (SRP)

A single function sends emails, charges accounts, and updates shipping all at once. This makes the code hard to test, maintain, and reuse.

---

### 🔴 Issue 6: Lack of Input Validation

`order.total` may be negative or zero, leading to invalid charges.