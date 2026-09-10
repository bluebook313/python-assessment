# ============================================================
# Models
# ============================================================
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship
from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    create_engine,
    select,
)
class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="product"
    )


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)

    orders: Mapped[list["Order"]] = relationship(
        back_populates="customer"
    )


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(30),
        default=OrderStatus.PENDING.value,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    customer: Mapped[Customer] = relationship(
        back_populates="orders"
    )

    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
    )

    def add_item(
        self,
        product: Product,
        quantity: int,
    ) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

        if self.status in (
            OrderStatus.COMPLETED.value,
            OrderStatus.CANCELLED.value,
        ):
            raise ValueError("Completed or cancelled order cannot be changed")

        if product.stock < quantity:
            raise ValueError("Not enough product stock")

        for item in self.items:
            if item.product_id == product.id:
                item.quantity += quantity
                return

        item = OrderItem(
            product=product,
            quantity=quantity,
            price=product.price,
        )

        self.items.append(item)

    def remove_item(self, product_id: int) -> None:
        if self.status in (
            OrderStatus.COMPLETED.value,
            OrderStatus.CANCELLED.value,
        ):
            raise ValueError("Completed or cancelled order cannot be changed")

        self.items = [
            item for item in self.items
            if item.product_id != product_id
        ]

    def calculate_total(self) -> float:
        return sum(
            item.price * item.quantity
            for item in self.items
        )

    def pay(self) -> None:
        if self.status != OrderStatus.PENDING.value:
            raise ValueError(
                "Only pending orders can be paid"
            )

        if not self.items:
            raise ValueError(
                "Cannot pay an empty order"
            )

        self.status = OrderStatus.PAID.value

    def cancel(self) -> None:
        if self.status in (
            OrderStatus.COMPLETED.value,
            OrderStatus.CANCELLED.value,
        ):
            raise ValueError(
                "Order cannot be cancelled"
            )

        if self.status == OrderStatus.PROCESSING.value:
            raise ValueError(
                "Processing order cannot be cancelled"
            )

        self.status = OrderStatus.CANCELLED.value

    def complete(self) -> None:
        if self.status != OrderStatus.PROCESSING.value:
            raise ValueError(
                "Only processing orders can be completed"
            )

        self.status = OrderStatus.COMPLETED.value


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"),
        nullable=False,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    # Snapshot of product price at order time
    price: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    order: Mapped[Order] = relationship(
        back_populates="items"
    )

    product: Mapped[Product] = relationship(
        back_populates="order_items"
    )
