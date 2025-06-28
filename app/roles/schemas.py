from pydantic import BaseModel

class RoleSchema(BaseModel):
    name: str

    class Config:
        orm_mode = True