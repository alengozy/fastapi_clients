from sqlalchemy import Column, ForeignKey, Integer, String, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum as E


from .database import Base

class StatusEnum(str,E):
    STARTED = "started"
    ENDED = "ended"
    IN_PROCESS = "in_process"
    AWAITING = "awaiting"
    CANCELED = "canceled"

class Employee(Base):
    __tablename__ = "temployees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String, unique=True, index=True)

    sale_point_id = Column(Integer, ForeignKey("tsalepoint.id"), nullable = False)
    sale_point = relationship("SalePoint", back_populates="employees")
    orders = relationship("Order", back_populates="employee")
    visits = relationship("Visit", back_populates="employee")


class SalePoint(Base):
    __tablename__ = "tsalepoint"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)

    employees = relationship("Employee", back_populates="sale_point")
    customers = relationship("Customer", back_populates="sale_point")
    orders = relationship("Order", back_populates="sale_point")
    visits = relationship("Visit", back_populates="sale_point")

class Customer(Base):
    __tablename__ = "tcustomers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone = Column(String, unique=True, index=True)
    sale_point_id = Column(Integer, ForeignKey("tsalepoint.id"), nullable=False)

    sale_point = relationship("SalePoint", back_populates="customers")
    orders = relationship("Order", back_populates="customer")
    visits = relationship("Visit", back_populates="customer")

class Order(Base):
    __tablename__ = "torders"

    id = Column(Integer, primary_key = True, index = True)
    created_at = Column(DateTime(timezone = True), server_default=func.now())
    fulfilled_at = Column(DateTime(timezone = True), server_default=func.now())
    sale_point_id = Column(Integer, ForeignKey("tsalepoint.id"))
    customer_id = Column(Integer, ForeignKey("tcustomers.id"))
    employee_id = Column(Integer, ForeignKey("temployees.id"))
    status = Column(Enum(StatusEnum), default = StatusEnum.STARTED)

    sale_point = relationship("SalePoint", back_populates="orders")
    visit = relationship("Visit", back_populates="order")
    employee = relationship("Employee", back_populates="orders")
    customer = relationship("Customer", back_populates="orders")

    #@hybrid_property
    #def is_active(self) -> bool:
    #   return self.fulfilled_at is None
class Visit(Base):
    __tablename__ = "tvisits"

    id = Column(Integer, primary_key=True, index=True)
    visited_at = Column(DateTime(timezone = True), server_default=func.now())
    employee_id = Column(Integer, ForeignKey("temployees.id"))
    order_id = Column(Integer, ForeignKey("torders.id"), unique = True)
    customer_id = Column(Integer, ForeignKey("tcustomers.id"))
    sale_point_id = Column(Integer, ForeignKey("tsalepoint.id"))

    order = relationship("Order", back_populates="visit")
    employee = relationship("Employee", back_populates="visits")
    customer = relationship("Customer", back_populates="visits")
    sale_point = relationship("SalePoint", back_populates="visits")




