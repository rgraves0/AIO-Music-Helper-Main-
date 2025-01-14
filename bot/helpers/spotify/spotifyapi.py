import json
import requests

from librespot.core import Session
from librespot.audio.decoders import AudioQuality

from bot.helpers.translations import lang
from bot.logger import LOGGER

class SpotifyAPI:
    def __init__(self):
        self.session = None
        self.token = None
        self.quality = AudioQuality.HIGH
        # If using mp3 - Set re-encode to True
        self.music_format = "ogg"
        self.reencode = False
        self.premiuim = False

    async def login(self, user_name, password):
        """if os.path.isfile("credentials.json"):
            self.session = Session.Builder().stored_file().create()
            return"""
        self.session = Session.Builder().user_pass(user_name, password).create()

    async def get_song_info(self, song_id):
        try:
            info = json.loads(
                requests.get(
                    "https://api.spotify.com/v1/tracks?ids="
                    + song_id
                    + "&market=from_token",
                    headers={"Authorization": "Bearer %s" % self.token},
                ).text
            )
            is_playable = info["tracks"][0]["is_playable"]
            if not is_playable:
                return None, lang.ERR_SPOT_NOT_AVAIL
            return info['tracks'][0], None
        except:
            LOGGER.debug('SPOTIFY : Error getting Track Details')
            pass

    async def get_album_name(self, album_id):
        headers = {"Authorization": f"Bearer {self.token}"}
        resp = requests.get(
            f"https://api.spotify.com/v1/albums/{album_id}", headers=headers
        ).json()
        return resp
    
    def handle_quality(self, data=None):
        'Sets quality if input given else returns cuurent quality'
        if data == 160: self.quality = AudioQuality.HIGH
        elif data == 320: self.quality = AudioQuality.VERY_HIGH
        else:
            if spotify.quality == AudioQuality.HIGH:
                return 160
            else: return 320

spotify = SpotifyAPI() 