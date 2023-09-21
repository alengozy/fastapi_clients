from fastapi import HTTPException


class BaseHttpException(HTTPException):
    status_code: int = None
    detail: str = None
    headers: dict[str, any] = None
    
    def __init__(self):
        super().__init__(status_code=self.status_code, detail = self.detail, headers=self.headers)

class CustomerNotFound(BaseHttpException):
    status_code = 400
    detail = 'Customer Not Found'

class EmployeeNotFound(BaseHttpException):
    status_code = 400
    detail = 'Employee Not Found'

class CustomerNotInSalePoint(BaseHttpException):
    status_code = 400
    detail = 'Customer not bound to Sale Point'

class EmployeeNotInSalePoint(BaseHttpException):
    status_code = 400
    detail = 'Employee not bound to Sale Point'

class SalePointDoesNotHaveCustomer(BaseHttpException):
    status_code = 400
    detail = 'Sale Point not appointed to Customer'
    
class DuplicateValue(BaseHttpException):
    status_code = 400
    
    def __init__(self, detail: str):
        self.detail = detail


