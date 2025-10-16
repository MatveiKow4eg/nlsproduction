from __future__ import annotations
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, Boolean, DateTime, Text, ForeignKey

# The db instance is provided by app.db via import in app.py
from app import db


class Product(db.Model):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    day_rate: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    description: Mapped[str | None] = mapped_column(Text)
    specs: Mapped[str | None] = mapped_column(Text)
    image_url: Mapped[str | None] = mapped_column(String(500))
    stock: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    package_items: Mapped[list[PackageItem]] = relationship(
        back_populates="product", cascade="all,delete-orphan"
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Product {self.id} {self.name!r}>"


class Package(db.Model):
    __tablename__ = "packages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    target: Mapped[str | None] = mapped_column(String(120))
    base_price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    description: Mapped[str | None] = mapped_column(Text)

    items: Mapped[list[PackageItem]] = relationship(
        back_populates="package", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Package {self.id} {self.title!r}>"


class PackageItem(db.Model):
    __tablename__ = "package_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    package_id: Mapped[int] = mapped_column(ForeignKey("packages.id"), nullable=False, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False, index=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    package: Mapped[Package] = relationship(back_populates="items")
    product: Mapped[Product] = relationship(back_populates="package_items")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<PackageItem pkg={self.package_id} product={self.product_id} x{self.quantity}>"


class Inquiry(db.Model):
    __tablename__ = "inquiries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_date: Mapped[str | None] = mapped_column(String(32))  # keep as string input for simplicity
    city: Mapped[str | None] = mapped_column(String(120))
    guests: Mapped[int | None] = mapped_column(Integer)
    service_type: Mapped[str | None] = mapped_column(String(120))
    delivery_required: Mapped[bool] = mapped_column(Boolean, default=False)

    contact_name: Mapped[str] = mapped_column(String(120), nullable=False)
    contact_email: Mapped[str | None] = mapped_column(String(255))
    contact_phone: Mapped[str | None] = mapped_column(String(64))
    notes: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Inquiry {self.id} {self.contact_name!r} at {self.created_at.isoformat()}>"


class Case(db.Model):
    __tablename__ = "cases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    type: Mapped[str | None] = mapped_column(String(64), index=True)
    location: Mapped[str | None] = mapped_column(String(200))
    date_label: Mapped[str | None] = mapped_column(String(64))
    short_text: Mapped[str | None] = mapped_column(Text)
    image_url: Mapped[str | None] = mapped_column(String(500))

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Case {self.id} {self.title!r}>"


class Post(db.Model):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(220), unique=True, index=True, nullable=False)
    content: Mapped[str | None] = mapped_column(Text)
    published: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime)

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Post {self.id} {self.slug!r} published={self.published}>"
