from pydantic import BaseModel

class CategorySchema(BaseModel):
    name: str

class NewCategorySchema(BaseModel):
    name: str