import spotipy
from SyncUs.Schemas.auth import TokenSchema
from SyncUs.Schemas.user import UserInfoSchema

class SpotifyWrapper:
    auth_manager = spotipy.oauth2.SpotifyOAuth(
        scope='user-read-currently-playing user-read-email user-read-recently-played user-modify-playback-state',
        show_dialog=True,
        redirect_uri="http://localhost:3000/oauth/callback"
    )

    def getOauthUrl(self) -> str:
        return self.auth_manager.get_authorize_url()

    def getToken(self, code: str) -> TokenSchema:
        return TokenSchema.parse_obj(self.auth_manager.get_access_token(code, check_cache=False))

    def getUserFromToken(self, access_token: str) -> UserInfoSchema:
        user = UserInfoSchema.parse_obj(
            spotipy.Spotify(auth=access_token).current_user()
        )
        return user

    def searchMusic(self, string: str):
        resp = spotipy.Spotify(client_credentials_manager = spotipy.SpotifyClientCredentials()).search(string,limit=1, type="track")
        matched = resp["tracks"]['items']
        if len(matched) != 0:
            return matched[0]["uri"], matched[0]["name"]
        return None, None

spotifyWrapper = SpotifyWrapper()
