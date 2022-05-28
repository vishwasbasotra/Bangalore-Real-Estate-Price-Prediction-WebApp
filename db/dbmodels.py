import imp
from pydantic import BaseModel
from typing import Optional

class SignIn(BaseModel):
    name: Optional[str] = ""
    email: str
    password: str

class HouseData(BaseModel):
    name: str
    phone: str
    area: int
    bhk: int
    bath: str
    location: str
    price: str