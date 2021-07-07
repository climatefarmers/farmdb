from pydantic import BaseModel
from fastapi import FastAPI
from postal.parser import parse_address
from typing import Optional

class Address(BaseModel):
    raw: str
    road: Optional[str]
    near: Optional[str]
    house_number: Optional[int]
    city: Optional[str]
    postcode: Optional[str]
    state: Optional[str]
    country: Optional[str]


app = FastAPI()

@app.get("/parse/", response_model=Address)
async def address_parser(address: str) -> Address:
    elems = {e[1]: e[0] for e in parse_address(address)}
    elems['raw'] = address
    return elems