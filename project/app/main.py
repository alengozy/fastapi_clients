from fastapi import Depends, FastAPI, HTTPException

from . import crud, validators, schemas
from .database import SessionAsync, init_db


app = FastAPI()


# Dependency
async def get_db():
    async with SessionAsync() as session:
        yield session


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/salepoints/{phone}", response_model=list[schemas.SalePoint])
async def get_sale_points(phone: str, db: SessionAsync = Depends(get_db)):
    sps = await crud.get_sale_points_by_num(db, phone)
    return sps


@app.post("/orders/", response_model=schemas.Order)
async def create_order(order: schemas.OrderCreate, db: SessionAsync = Depends(get_db)):
    await validators.validate_order(db=db, order=order)
    return await crud.create_order(db=db, order=order)


@app.post("/visits/", response_model=schemas.Visit)
async def create_visit(visit: schemas.VisitCreate, db: SessionAsync = Depends(get_db)):
    db_order = await crud.get_order(db=db, order_id=visit.order_id)
    if db_order.fulfilled_at:
        raise HTTPException(status_code=400, detail="Order already closed")


@app.post("/employee/", response_model=schemas.Employee)
async def create_employee(employee: schemas.EmployeeCreate, db: SessionAsync = Depends(get_db)):
    return await crud.create_employee(employee=employee, db=db)


@app.post("/customer/", response_model=schemas.Customer)
async def create_employee(customer: schemas.CustomerCreate, db: SessionAsync = Depends(get_db)):
    await validators.validate_duplicate_customer(db = db, customer=customer)
    return await crud.create_customer(customer=customer, db=db)


@app.post("/salepoint/")
async def create_sale_point(sp: schemas.SalePointCreate, db: SessionAsync = Depends(get_db)):
    await validators.validate_duplicate_sp(db=db, sp_title=sp.title)
    return await crud.create_sale_point(sp=sp, db=db)
