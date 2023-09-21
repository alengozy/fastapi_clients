from sqlalchemy.orm import Session, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_, select
from . import models, schemas


async def get_sale_point(db: AsyncSession, sp_id: int):
    query = select(models.SalePoint).where(models.SalePoint.id == sp_id).limit(1)
    return await db.execute(query)

async def get_sale_point_by_title(db: AsyncSession, sp_title: str):
    query = select(models.SalePoint).where(models.SalePoint.title == sp_title).limit(1)
    return await db.execute(query)

async def get_order(db: AsyncSession, order_id: int):
    result = await db.query(models.Order).filter(models.Order.id == order_id).first()
    return result

async def get_orders(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.query(models.Order).offset(skip).limit(limit).all()
    return result

async def get_employee(db: AsyncSession, employee_id: int):
    result = await db.query(models.Employee).filter(models.Employee.id == employee_id).first()  
    return result

async def get_employee_by_phone(db: AsyncSession, phone: str):
    result = await db.query(models.Employee).filter(models.Employee.phone == phone).first()
    return result

async def get_customer(db: AsyncSession, customer_id: int):
    result = await db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    return result

async def get_customer_by_phone(db: AsyncSession, phone: str):
    result = await db.query(models.Customer).filter(models.Customer.phone == phone).first()
    return result

async def get_customer_by_name(db: AsyncSession, name: str):
    result = await db.query(models.Customer).filter(models.Customer.name == name).first()
    return result


async def get_sale_points_by_num(db: AsyncSession, phone: str):
    sps = await db.query(models.SalePoint).join(models.Customer).join(models.Employee).filter(or_ (models.Employee.phone == phone, models.Customer.phone == phone)) \
    .options(
        joinedload(models.SalePoint.customers)
        ,joinedload(models.SalePoint.employees)
    )
    return sps

async def create_sale_point(db: AsyncSession, sp: schemas.SalePointCreate):
    db_sale_point = models.SalePoint(title=sp.title)
    db.add(db_sale_point)
    await db.commit()
    await db.refresh(db_sale_point)
    return db_sale_point

async def create_customer(db: AsyncSession, customer: schemas.CustomerCreate):
    db_customer = models.Customer(name = customer.name, phone = customer.phone, sale_point_id = customer.sale_point_id)
    db.add(db_customer)
    await db.commit()
    await db.refresh(db_customer)
    return db_customer

async def create_employee(db: AsyncSession, employee: schemas.EmployeeCreate):
    db_employee = models.Employee(name = employee.name, phone = employee.phone, sale_point_id = employee.sale_point_id)
    db.add(db_employee)
    await db.commit()
    await db.refresh(db_employee)
    return db_employee

