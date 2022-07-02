from SyncUs.Schemas.user import UserInfoSchema
from SyncUs.utils.spotify import spotifyWrapper

class InMemDataBase:
    def __init__(self) -> None:
        self.sidMap = {}

    def addSid(self, sid: str, token: str):
        user = spotifyWrapper.getUserFromToken(token)
        self.sidMap[sid] = user
        print(user)
    
    def getUserFromSid(self, sid: str) -> UserInfoSchema:
        print(self.sidMap,'-------------')
        return self.sidMap[sid]

    def removeSid(self, sid):
        del self.sidMap[sid]


inMemDataBase = InMemDataBase()
