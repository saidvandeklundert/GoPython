from pydantic import BaseModel
from typing import List


class Standard(BaseModel):
    log: bool


class Py2GoArgs(BaseModel):
    hosts: List[str]
    standard: Standard


m = Py2GoArgs(hosts=["1.1.1.1", "2.2.2.2"], standard={"log": "False"})

# returns a dictionary:
print(m.dict())