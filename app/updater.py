"""In-app updater for Habit Garden (pure logic, no Flet).

How it works: the app asks GitHub for the latest public release
(https://api.github.com/repos/codewithkinza88/commit-is-art/releases/
latest). The release asset is a public download, so no login is
needed — unlike a GitHub Actions artifact, which needs a GitHub
sign-in and the app could never fetch it. The build workflow
publishes the built APK to a rolling "latest" release, so the app
can always find the newest version there.

The check never raises: offline, a timeout, bad JSON or a missing
asset just means "no update known" — the app simply shows no
banner. The final install step is Android's own installer popup:
one tap, inside the app flow, no browser.
"""

import json
import os
import urllib.error
import urllib.request

LATEST_RELEASE_URL = ("https://api.github.com/repos/codewithkinza88/"
                      "commit-is-art/releases/latest")
API_TIMEOUT_SECONDS = 8
DOWNLOAD_TIMEOUT_SECONDS = 30


def _parse_version(text):
    """'v1.7.0' -> (1, 7, 0); malformed text -> None."""
    if not isinstance(text, str):
        return None
    text = text.strip().lstrip("vV")
    if not text:
        return None
    numbers = []
    for part in text.split("."):
        part = part.strip()
        if not part.isdigit():
            return None
        numbers.append(int(part))
    return tuple(numbers)


def is_newer(latest_version, current_version):
    """True when latest_version is newer than current_version.

    Tolerant of a "v" prefix; malformed strings are never newer.
    """
    latest = _parse_version(latest_version)
    current = _parse_version(current_version)
    if latest is None or current is None:
        return False
    return latest > current


def _read_response(response):
    """Read a response body as text, closing it afterwards."""
    try:
        return response.read().decode("utf-8")
    finally:
        close = getattr(response, "close", None)
        if callable(close):
            close()


def fetch_latest_release(opener=None):
    """Fetch the latest public release from GitHub.

    Returns {"version", "apk_url", "tag"} or None on ANY failure
    (offline, timeout, bad JSON, no .apk asset) — never raises.
    `opener` is a test seam: a callable taking a URL (or Request)
    and returning a response object with .read(); when None, urllib
    is used.
    """
    try:
        if opener is not None:
            response = opener(LATEST_RELEASE_URL)
            body = _read_response(response)
        else:
            request = urllib.request.Request(
                LATEST_RELEASE_URL,
                headers={"Accept": "application/vnd.github+json",
                         "User-Agent": "Habit-Garden-Updater"})
            response = urllib.request.urlopen(
                request, timeout=API_TIMEOUT_SECONDS)
            body = _read_response(response)
        payload = json.loads(body) or {}
        tag = payload.get("tag_name") or ""
        version = tag.lstrip("vV")
        apk_url = None
        for asset in payload.get("assets") or []:
            name = asset.get("name") or ""
            if name.lower().endswith(".apk"):
                apk_url = asset.get("browser_download_url")
                break
        if not version or not apk_url:
            return None
        return {"version": version, "apk_url": apk_url, "tag": tag}
    except Exception:
        return None


def default_apk_path():
    """Where to save the downloaded APK: the Downloads folder when
    it exists (Android), otherwise the working directory."""
    downloads = os.path.join(os.path.expanduser("~"), "Download")
    folder = downloads if os.path.isdir(downloads) else os.getcwd()
    return os.path.join(folder, "habit-garden.apk")


def download_apk(apk_url, dest_path, progress_cb=None, opener=None):
    """Stream-download the APK to dest_path.

    progress_cb(downloaded_bytes, total_bytes_or_None) is called as
    chunks arrive. Returns dest_path. Raises on real failure — the
    caller shows the friendly message.
    """
    request = urllib.request.Request(
        apk_url, headers={"User-Agent": "Habit-Garden-Updater"})
    if opener is not None:
        response = opener(request)
    else:
        response = urllib.request.urlopen(
            request, timeout=DOWNLOAD_TIMEOUT_SECONDS)
    total = None
    try:
        headers = getattr(response, "headers", None)
        if headers is not None:
            try:
                length = headers.get("Content-Length")
            except Exception:
                length = None
            if length:
                try:
                    total = int(length)
                except (TypeError, ValueError):
                    total = None
        downloaded = 0
        with open(dest_path, "wb") as out:
            while True:
                chunk = response.read(65536)
                if not chunk:
                    break
                out.write(chunk)
                downloaded += len(chunk)
                if progress_cb is not None:
                    progress_cb(downloaded, total)
    finally:
        close = getattr(response, "close", None)
        if callable(close):
            close()
    return dest_path
