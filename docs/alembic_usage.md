```python
Base.metadata.create_all(engine)
```

Alembic should replace that for **database schema management**.

## 1. Install Alembic

```powershell
python -m pip install alembic
```

Or add it to `requirements.txt`:

```text
alembic
```

---

## 2. Initialize Alembic

From your project root:

```powershell
alembic init alembic
```

You'll get:

```text
project/
├── alembic/
│   ├── versions/
│   ├── env.py
│   ├── script.py.mako
│   └── README
│
├── alembic.ini
├── app/
├── tests/
└── requirements.txt
```

---

## 3. Configure database URL

You probably already have:

```python
DATABASE_URL = ...
```

in your config.

In `alembic.ini` you'll see:

```ini
sqlalchemy.url = driver://user:pass@localhost/dbname
```

You can leave it empty:

```ini
sqlalchemy.url =
```

because I recommend getting the URL from your Python config.

---

# 4. Modify `alembic/env.py`

This is the important part.

You need Alembic to know about your models.

At the top:

```python
from models import Base
```

But **your Base is actually here**:

```python
from utils.database.connection import Base
```

So use:

```python
from utils.database.connection import Base
```

And import your models:

```python
from models import Product, Customer, Order, OrderItem
```

Then find:

```python
target_metadata = None
```

and change it to:

```python
target_metadata = Base.metadata
```

So the relevant part becomes:

```python
from utils.database.connection import Base
from models import Product, Customer, Order, OrderItem


target_metadata = Base.metadata
```

The imports of the models are important because otherwise SQLAlchemy may not know about those tables when Alembic examines the metadata.

---

# 5. Better: use your `DATABASE_URL`

If your config contains something like:

```python
DATABASE_URL = "sqlite:///./database.db"
```

you can put this in `env.py`:

```python
from schemas.config import DATABASE_URL
```

Then:

```python
config.set_main_option(
    "sqlalchemy.url",
    DATABASE_URL
)
```

So you don't have to maintain the database URL twice.

For example:

```python
from schemas.config import DATABASE_URL

config.set_main_option(
    "sqlalchemy.url",
    DATABASE_URL
)
```

---

# 6. Create your first migration

Now run:

```powershell
alembic revision --autogenerate -m "create initial tables"
```

Alembic will compare:

```text
Your SQLAlchemy Models
        ↓
Base.metadata
        ↓
Current Database
```

and generate a migration inside:

```text
alembic/versions/
```

Something like:

```text
alembic/
└── versions/
    └── 8f123abc_create_initial_tables.py
```

---

# 7. Apply the migration

Run:

```powershell
alembic upgrade head
```

Now your tables should be created:

```text
customers
products
orders
order_items
```

---

# 8. Remove `create_all`

This part of your model file:

```python
Base.metadata.create_all(engine)
```

should be removed.

Don't put database creation inside your model module.

So your models should end with:

```python
class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(ForeignKey("orders.id"), nullable=False)
    product_id = Column(ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_order_price = Column(Float, nullable=False)

    __table_args__ = (
        UniqueConstraint("order_id", "product_id"),
    )
```

No:

```python
Base.metadata.create_all(engine)
```

---

# 9. Normal workflow from now on

Suppose you change:

```python
class Product(Base):
    ...

    price = Column(Float, nullable=False)
    count = Column(Integer, nullable=False)
```

and later add:

```python
description = Column(String(500))
```

You don't manually modify the database.

Run:

```powershell
alembic revision --autogenerate -m "add product description"
```

Then:

```powershell
alembic upgrade head
```

That's the basic workflow:

```text
Change Model
     ↓
alembic revision --autogenerate
     ↓
Review migration
     ↓
alembic upgrade head
     ↓
Database updated
```

### Useful commands

Check current migration:

```powershell
alembic current
```

See migration history:

```powershell
alembic history
```

Upgrade:

```powershell
alembic upgrade head
```

Go back one migration:

```powershell
alembic downgrade -1
```
