# Heavily inspired by https://github.com/voicevox-client/python
# Documents available at <base_url>/docs, e.g. http://localhost:50021/docs
import httpx

# core_version in the methods below is voicevox core version, check for new ones here: https://github.com/VOICEVOX/voicevox_core/releases
# Just leave it as None for the latest possible
class Client:
    def __init__(self, base_url="http://localhost:50021", timeout=None):
        """
        Args:
            base_url (string): Voicevox engine base url
            timeout (integer | None): request timeout, useful to prevent hanging in CPU mode
        """
        self.http_client = httpx.Client(base_url=base_url, timeout=timeout)

    def fetch_speakers(self, core_version=None):
        """
        Fetch speakers list
        """
        params = {}
        if core_version is not None:
            params["core_version"] = core_version
        return self.__request("GET", "/speakers", params=params)

    def fetch_speaker_info(self, speaker_uuid, core_version=None):
        """
        Fetch speaker's info by speaker_uuid

        Args:
            speaker_uuid (string)
            core_version (string | None)
        """
        params = {
            "speaker_uuid": speaker_uuid
        }
        if core_version is not None:
            params["core_version"] = core_version
        return self.__request("GET", "/speaker_info", params=params)

    def initialize_speaker(self, speaker_id, skip_reinit=False, core_version=None):
        """
        Initialize the speaker with the specified speaker_id
        Not required but this will speed up the first execution of some APIs related to the speaker

        Args:
            speaker_id (integer)
            skip_reinit (boolean): Flag for whether to skip reinitialization of a speaker that's already initialized
            core_version (string | None)
        """
        params = {
            "speaker": speaker_id,
            "skip_reinit": skip_reinit
        }
        if core_version is not None:
            params["core_version"] = core_version
        self.__request("POST", "/initialize_speaker", params=params)

    def text_to_speech(self, text, speaker_id, enable_interrogative_upspeak=True, core_version=None):
        """
        Returns a wav file with speaker_id speaking text

        Args:
            text (string)
            speaker_id (integer)
            core_version (string | None)
        """

        audio_query = self.create_audio_query(text, speaker_id, core_version=core_version)
        return self.synthesis(audio_query, speaker_id, enable_interrogative_upspeak=enable_interrogative_upspeak, core_version=core_version)

    def create_audio_query(self, text, speaker_id, core_version=None):
        """
        Create audio query for voice synthesis. Must do this first before each voice synthesis

        Args:
            text (string)
            speaker_id (integer)
            core_version (string | None)
        """
        params = {
            "text": text,
            "speaker": speaker_id
        }
        if core_version is not None:
            params["core_version"] = core_version
        return self.__request("POST", "/audio_query", params=params)

    def synthesis(self, audio_query, speaker_id, enable_interrogative_upspeak=True, core_version=None):
        """
        Synthesize voice

        Args:
            audio_query: result of create_audio_query
            speaker_id (integer)
            enable_interrogative_upspeak (boolean): Adjust word ending for questions (e.g. higher pitch for the end of a question)
            core_version (string | None)
        """
        params = {
            "speaker": speaker_id,
            "enable_interrogative_upspeak": enable_interrogative_upspeak
        }
        if core_version is not None:
            params["core_version"] = core_version
        return self.__request("POST", "/synthesis", params=params, json=audio_query)

    def close(self):
        """
        Close http_client, must be called at the end
        """
        self.http_client.close()

    def __enter__(self):
        print("Voicevox Client ENTER")
        return self

    def __exit__(self, *args):
        print("Voicevox Client EXIT")
        self.close()

    def __request(self, method, path, **kwargs):
        response = self.http_client.request(method, path, **kwargs)

        if response.status_code == 200 or response.status_code == 204:
            if response.headers.get("content-type") == "application/json":
                return response.json()
            else:
                return response.content
        else:
            raise self.HttpException(response.json())


    class HttpException(Exception):
        pass
