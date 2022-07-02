import spotipy
from SyncUs.Schemas.user import UserInfoSchema

class SpotifyWrapper:
    def getUserFromToken(self, access_token: str):
        user = UserInfoSchema.parse_obj(
            spotipy.Spotify(auth=access_token).current_user()
        )
        return user

spotifyWrapper = SpotifyWrapper()