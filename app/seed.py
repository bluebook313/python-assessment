"""
Seed script for populating the database with sample data.
Run with: python -m app.seed
"""

from datetime import datetime, timedelta
from utils.database.connection import Base, engine, orm_session
from schemas.config import OrderStatus

# مهم: مدل‌ها باید import بشن تا Base.metadata اون‌ها رو بشناسه
from models import Product, Customer, Order, OrderItem


def init_db():
    """Create all tables if they don't exist."""
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created (if not existed).")


def seed_products(db):
    """Create 3 sample products (as required by the task)."""
    products = [
        Product(name="Laptop", price=1500.00, count=10),
        Product(name="Smartphone", price=800.00, count=25),
        Product(name="Headphones", price=120.00, count=50),
    ]
    db.add_all(products)
    db.commit()
    for p in products:
        db.refresh(p)
    print(f"✅ Seeded {len(products)} products.")
    return products


def seed_customers(db):
    """Create sample customers."""
    customers = [
        Customer(name="Ali Rezaei", email="ali@example.com"),
        Customer(name="Sara Ahmadi", email="sara@example.com"),
        Customer(name="Mohammad Karimi", email="mohammad@example.com"),
    ]
    db.add_all(customers)
    db.commit()
    for c in customers:
        db.refresh(c)
    print(f"✅ Seeded {len(customers)} customers.")
    return customers


def seed_orders(db, customers, products):
    """Create sample orders with items in different statuses."""
    now = datetime.utcnow()

    # --- Order 1: PENDING ---
    order1 = Order(
        customer_id=customers[0].id,
        status=OrderStatus.PENDING.value,
        created_at=now,
        total_price=0.0,
    )
    db.add(order1)
    db.commit()
    db.refresh(order1)

    items1 = [
        OrderItem(
            order_id=order1.id,
            product_id=products[0].id,   # Laptop
            quantity=1,
            total_order_price=products[0].price * 1,
        ),
        OrderItem(
            order_id=order1.id,
            product_id=products[2].id,   # Headphones
            quantity=2,
            total_order_price=products[2].price * 2,
        ),
    ]
    db.add_all(items1)
    order1.total_price = sum(i.total_order_price for i in items1)
    db.commit()

    # --- Order 2: PAID ---
    order2 = Order(
        customer_id=customers[1].id,
        status=OrderStatus.PAID.value,
        created_at=now - timedelta(hours=2),
        total_price=0.0,
    )
    db.add(order2)
    db.commit()
    db.refresh(order2)

    items2 = [
        OrderItem(
            order_id=order2.id,
            product_id=products[1].id,   # Smartphone
            quantity=1,
            total_order_price=products[1].price * 1,
        ),
    ]
    db.add_all(items2)
    order2.total_price = sum(i.total_order_price for i in items2)
    db.commit()

    # --- Order 3: COMPLETED ---
    order3 = Order(
        customer_id=customers[2].id,
        status=OrderStatus.COMPLETED.value,
        created_at=now - timedelta(days=1),
        total_price=0.0,
    )
    db.add(order3)
    db.commit()
    db.refresh(order3)

    items3 = [
        OrderItem(
            order_id=order3.id,
            product_id=products[0].id,
            quantity=2,
            total_order_price=products[0].price * 2,
        ),
    ]
    db.add_all(items3)
    order3.total_price = sum(i.total_order_price for i in items3)
    db.commit()
    
    # --- Order 3: COMPLETED ---
    order3 = Order(
        customer_id=customers[2].id,
        status=OrderStatus.COMPLETED.value,
        created_at=now - timedelta(days=1),
        total_price=0.0,
    )
    db.add(order3)
    db.commit()
    db.refresh(order3)

    items3 = [
        OrderItem(
            order_id=order3.id,
            product_id=products[0].id,
            quantity=2,
            total_order_price=products[0].price * 2,
        ),
    ]
    db.add_all(items3)
    order3.total_price = sum(i.total_order_price for i in items3)
    db.commit()

    print("✅ Seeded 3 orders with items (PENDING / PAID / COMPLETED).")


def run_seed():
    """Main entry point."""
    init_db()
    db = orm_session()
    try:
        # اگه دیتابیس از قبل داده داشت، دوباره seed نکن
        if db.query(Product).count() > 0:
            print("⚠️  Database already has data. Skipping seed.")
            return

        products = seed_products(db)
        customers = seed_customers(db)
        seed_orders(db, customers, products)

        print("Seeding completed successfully!")
        print("📋 Sample data ready:")
        print("   - 3 Products (Laptop, Smartphone, Headphones)")
        print("   - 3 Customers (Ali, Sara, Mohammad)")
        print("   - 3 Orders (PENDING, PAID, COMPLETED)")
    except Exception as e:
        db.rollback()
        print(f"❌ Seeding failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()