# Heavily inspired by https://github.com/voicevox-client/python
from httpx import AsyncClient

# core_version in the methods below is voicevox core version, check for new ones here: https://github.com/VOICEVOX/voicevox_core/releases
# Just leave it as None for the latest possible
class Client:
    def __init__(self, base_url="http://localhost:50021", timeout=None):
        """
        Args:
            base_url (string): Voicevox engine base url
            timeout (integer | None): request timeout, useful to prevent hanging in CPU mode
        """
        self.http_client = AsyncClient(base_url=base_url, timeout=timeout)

    async def fetch_speakers(self, core_version=None):
        """
        Fetch speakers list
        """
        params = {}
        if core_version is not None:
            params["core_version"] = core_version
        return await self.__request("GET", "/speakers", params=params)

    async def fetch_speaker_info(self, speaker_uuid, core_version=None):
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
        return await self.__request("GET", "/speaker_info", params=params)

    async def close(self):
        """
        Close http_client, must be called at the end
        """
        await self.http_client.aclose()

    async def __aenter__(self):
        print("Voicevox Client ENTER")
        return self

    async def __aexit__(self, *args):
        print("Voicevox Client EXIT")
        await self.close()

    async def __request(self, method, path, **kwargs):
        response = await self.http_client.request(method, path, **kwargs)

        if response.status_code == 200 or response.status_code == 204:
            if response.headers.get("content-type") == "application/json":
                return response.json()
            else:
                return response.content
        else:
            raise self.HttpException(response.json())


    class HttpException(Exception):
        pass