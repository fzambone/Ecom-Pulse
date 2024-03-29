from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from utils.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    deleted_at = Column(DateTime)

    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)
    description = Column(String)
    quantity = Column(Integer)
    category_id = Column(Integer, ForeignKey("categories.id"))
    deleted_at = Column(DateTime)

    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")

class Visitor(Base):
    __tablename__ = "visitors"

    id = Column(Integer, primary_key=True, index=True)
    approximate_location = Column(String(50))
    session_start_time = Column(DateTime)
    ip_address = Column(String)
    deleted_at = Column(DateTime)

    events = relationship("Event", back_populates="visitor")
    orders = relationship("Order", back_populates="visitor")

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime)
    visitor_id = Column(Integer, ForeignKey("visitors.id"))
    event_type = Column(String(50))
    page_url = Column(String(255))
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    referrer = Column(String(255))
    deleted_at = Column(DateTime)
    
    visitor = relationship("Visitor", back_populates="events")
    product = relationship("Product")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime)
    visitor_id = Column(Integer, ForeignKey("visitors.id"))
    total_amount = Column(Float)
    deleted_at = Column(DateTime)

    visitor = relationship("Visitor", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    deleted_at = Column(DateTime)

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")