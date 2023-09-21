from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional

class StatusEnum(str,Enum):
    STARTED = "started"
    ENDED = "ended"
    IN_PROCESS = "in_process"
    AWAITING = "awaiting"
    CANCELED = "canceled"

class HumanBase(BaseModel):
    name: str
    phone: str

class VisitBase(BaseModel):
    pass

class VisitCreate(VisitBase):
    visited_at: datetime = Field(default_factory=datetime.now)
    sale_point_id: int
    customer_id: int
    employee_id: int
    order_id: int

class Visit(VisitBase):
    id: int
    

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    created_at: datetime = Field(default_factory=datetime.now)
class OrderCreate(OrderBase):
    sale_point_id: int
    employee_id: int
    customer_id: int 

class Order(OrderBase):
    id: int
    fulfilled_at: Optional[datetime] = None
    status: StatusEnum = StatusEnum.STARTED

    class Config:
        from_attributes = True
        use_enum_values = True

class EmployeeCreate(HumanBase):
    sale_point_id: int

class CustomerCreate(HumanBase):
    sale_point_id: int

class Employee(HumanBase):
    id: int

    orders: list[Order] = []
    visits: list[Visit] = []
    class Config:
        from_attributes = True

class Customer(HumanBase):
    id: int
    orders: list[Order] = []
    visits: list[Visit] = []

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    created_at: str
    fulfilled_at: str  = None


class SalePointBase(BaseModel):
    pass

class SalePointCreate(SalePointBase):
    title: str

class SalePoint(SalePointBase):
    id: int
    employees: list[Employee] = []
    orders: list[Order] = []
    customers: list[Customer] = []
    visits: list[Visit] = []

    class Config:
        from_attributes = True