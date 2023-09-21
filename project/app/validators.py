from . import schemas, models, crud
from sqlalchemy.ext.asyncio import AsyncSession
from .exceptions import *

async def validate_human(customer: models.Customer, employee: models.Employee):
    if not customer:
        raise CustomerNotFound()
    if not employee:
        raise EmployeeNotFound()
    
async def validate_order(db: AsyncSession, order: schemas.OrderCreate):
    db_customer = await crud.get_customer(db = db, customer_id = order.customer_id)
    db_employee = await crud.get_employee(db = db, employee_id = order.employee_id)

    await validate_human(db_customer, db_employee)

    db_sale_points = [u.__dict__ for u in await crud.get_sale_points_by_num(db = db, phone = db_customer.phone).all()]
    for el in db_sale_points:
        sale_point_customers = [u.__dict__ for u in el['customers']]
        sale_point_employees = [u.__dict__ for u in el['employees']]
    if not any(sale_point['id'] == order.sale_point_id for sale_point in db_sale_points):
        raise SalePointDoesNotHaveCustomer()
    if not any(employee['id'] == order.employee_id for employee in sale_point_employees):
        raise EmployeeNotInSalePoint()
    if not any(customer['id'] == order.customer_id for customer in sale_point_customers):
        raise CustomerNotInSalePoint()
    
async def validate_duplicate_sp(db: AsyncSession, sp_title: str):
    db_sale_point = await crud.get_sale_point_by_title(db = db, sp_title = sp_title)
    if db_sale_point:
        raise DuplicateValue(detail='Sale Point with that title already exists')
    
async def validate_duplicate_customer(db: AsyncSession, customer: schemas.CustomerCreate):
    db_customer_by_name = await crud.get_customer_by_name(db = db, name = customer.name)
    db_customer_by_phone = await crud.get_customer_by_phone(db = db, phone = customer.phone)
    if db_customer_by_name or db_customer_by_phone:
        raise DuplicateValue(detail = 'Duplicate customer name' if db_customer_by_name else 'Duplicate customer phone')
    