from pydantic import BaseModel, validator

from SyncUs.Schemas.user import UserInfoSchema
from SyncUs.utils.dataops import inMemDataBase


class BroadcastSchema(BaseModel):
    msg: str
    sent_id: str
    sent_from: UserInfoSchema = None

    @validator('sent_from', pre=True, always=True)
    def set_sent_from(cls, val, values):
        if val is None:
            return inMemDataBase.getUserFromSid(values['sent_id'])
