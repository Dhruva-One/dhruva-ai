import httpx

from app.config import settings


class PlatformClient:
    """Reads school data through the platform API with the caller's own token.

    The AI service never reads the platform database, so every permission and
    feature switch applies to Dhruva exactly as it does to the person asking.
    """

    def __init__(self, user_token: str, base_url: str | None = None):
        self._client = httpx.Client(
            base_url=base_url or settings.platform_api_url,
            headers={"Authorization": f"Bearer {user_token}"},
            timeout=5.0,
        )

    def get(self, path: str) -> dict | list:
        resp = self._client.get(path)
        resp.raise_for_status()
        return resp.json()
