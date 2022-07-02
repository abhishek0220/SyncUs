from pydantic import BaseModel, Field


class UserInfoSchema(BaseModel):
    userId: str = Field(alias='id')
    display_name: str
    email: str
