from pydantic import BaseModel, Field


class UserInfoSchema(BaseModel):
    userId: str = Field(alias='id')
    country: str
    display_name: str
    email: str
