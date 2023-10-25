from typing import Any, Dict, Optional

import httpx


async def get(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
    timeout: Optional[int] = 30,
    **kwargs,
) -> httpx.Response:
    async with httpx.AsyncClient(follow_redirects=True) as client:
        return await client.get(
            url, headers=headers, params=params, timeout=timeout, **kwargs
        )
