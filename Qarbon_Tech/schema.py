from pydantic import BaseModel,Field
from datetime import datetime
from typing import Union
from enum import Enum

class Items(BaseModel):
    item_id : str
    issue_date : datetime

class User(str,Enum):
    buyer = "buyer"
    seller = "seller"

class Request_Body(BaseModel):
    name : str or None = Field(None,min_length=3) 
    email : str = Field(min_length=10,default="abc@gmail.com",pattern=r"^[a-z0-9+_\.]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+$")
    contact : str = Field(pattern="^[0-9]{10}$")
    source : User = Field(default="buyer")
    item_name : list[Items]

class Resp(Request_Body):
    ID : str

# Employee

class Deduct(BaseModel):
    tax : Union[float,None] = None
    health_insurance : float
class Earn(BaseModel):
    basic_salary : Union[float,None] = None
    overtime_pay : Union[float,None] = None

class Sal_details(BaseModel):
    salary_id : str
    earnings : Earn 
    deductions : Union[Deduct,None] = None
    net_salary : Union[float,None] = None

class Emp(BaseModel):
    full_name : Union[str,None] = None, Field(default="employeeName")
    years_of_service : Union[int,None] = None, Field(default=5)
    contact_number : Union[int,None] = None,Field(max_digits=10,min_length=10)
    is_present : bool = True
    salary_detail : Sal_details

