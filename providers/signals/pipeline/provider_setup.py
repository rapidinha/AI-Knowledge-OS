from __future__ import annotations

import os
from typing import Any


def _non_empty_str(val: Any) -> bool:
    return isinstance(val, str) and bool(val.strip())


def _has_google_creds(meta: dict[str, Any], token_env: str) -> bool:
    return bool(
        os.environ.get(token_env)
        or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        or meta.get("credentials_file")
    )


def check_provider_ready(name: str, meta: dict[str, Any]) -> tuple[bool, str]:
    if not meta.get("enabled"):
        return True, ""
    if name == "product_hunt":
        if not os.environ.get("PRODUCTHUNT_TOKEN"):
            return False, (
                "Set env PRODUCTHUNT_TOKEN (Product Hunt developer token from "
                "https://api.producthunt.com/v2/oauth/applications). Never commit the token."
            )
        return True, ""
    if name == "rss":
        feeds = meta.get("feeds") or []
        if not feeds:
            return False, "Add providers.rss.feeds: [url, ...] in journals/radar/config.yaml"
        return True, ""
    if name == "youtube_api":
        if not os.environ.get("YOUTUBE_API_KEY"):
            return False, "Set env YOUTUBE_API_KEY (Google Cloud YouTube Data API key)."
        if not (meta.get("queries") or meta.get("channel_ids")):
            return False, "Set providers.youtube_api.queries or channel_ids in config.yaml"
        return True, ""
    if name == "ga4":
        if _non_empty_str(meta.get("export_path")):
            return True, ""
        if not _has_google_creds(meta, "GA4_ACCESS_TOKEN"):
            return False, (
                "Set providers.ga4.export_path to a local runReport JSON export, or set "
                "GA4_ACCESS_TOKEN, GOOGLE_APPLICATION_CREDENTIALS, or providers.ga4.credentials_file "
                "(lab only)."
            )
        if not meta.get("property_id"):
            return False, "Set providers.ga4.property_id in config.yaml"
        return True, ""
    if name == "search_console":
        if _non_empty_str(meta.get("export_path")):
            return True, ""
        if not _has_google_creds(meta, "GSC_ACCESS_TOKEN"):
            return False, (
                "Set providers.search_console.export_path to a local query export JSON, or set "
                "GSC_ACCESS_TOKEN, GOOGLE_APPLICATION_CREDENTIALS, or "
                "providers.search_console.credentials_file (lab only)."
            )
        if not meta.get("site_url"):
            return False, "Set providers.search_console.site_url (e.g. https://example.com/)"
        return True, ""
    return True, ""
