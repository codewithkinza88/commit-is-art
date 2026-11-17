"""Plain-script tests for the in-app updater (app/updater.py).

Run:  python3 tests/test_updater.py

The updater must never crash the app: the release check returns
None on ANY failure (offline, timeout, bad JSON, missing asset),
and only a real download failure raises — the UI shows the
friendly message for that. No test below touches the real network:
the release fetch and the download both take a fake opener.
"""

import json
import os
import sys
import tempfile
import urllib.error

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.updater import (  # noqa: E402
    LATEST_RELEASE_URL, default_apk_path, download_apk,
    fetch_latest_release, is_newer,
)

PASSED = 0


def check(name, condition):
    global PASSED
    assert condition, f"FAILED: {name}"
    PASSED += 1
    print(f"PASS {name}")


class FakeResponse:
    """A minimal urllib response: read() in chunks, then b''."""

    def __init__(self, data, headers=None):
        self._data = data
        self._pos = 0
        self.headers = headers if headers is not None else {}
        self.closed = False

    def read(self, size=-1):
        if size is None or size < 0:
            chunk, self._pos = self._data[self._pos:], len(self._data)
            return chunk
        chunk = self._data[self._pos:self._pos + size]
        self._pos += len(chunk)
        return chunk

    def close(self):
        self.closed = True


def _release_json(tag="v1.7.0", assets=None):
    if assets is None:
        assets = [
            {"name": "notes.txt",
             "browser_download_url": "https://example.com/notes.txt"},
            {"name": "habit-garden.apk",
             "browser_download_url": "https://example.com/habit-garden.apk"},
        ]
    return json.dumps({"tag_name": tag, "assets": assets}).encode("utf-8")


def test_is_newer():
    check("a newer patch version is newer",
          is_newer("1.7.0", "1.6.0"))
    check("the same version is not newer",
          not is_newer("1.6.0", "1.6.0"))
    check("an older version is not newer",
          not is_newer("1.5.0", "1.6.0"))
    check("a 'v' prefix is tolerated",
          is_newer("v1.7.0", "1.6.0"))
    check("1.10 beats 1.9 (numeric, not alphabetical)",
          is_newer("1.10.0", "1.9.0"))
    check("a major bump is newer",
          is_newer("2.0", "1.9.9"))
    check("a malformed latest version is never newer",
          not is_newer("banana", "1.6.0"))
    check("a malformed current version is never newer",
          not is_newer("1.7.0", "banana"))
    check("an empty latest version is never newer",
          not is_newer("", "1.6.0"))
    check("a non-numeric part is never newer",
          not is_newer("1.7.x", "1.6.0"))


def test_fetch_latest_release():
    def opener_ok(url):
        assert url == LATEST_RELEASE_URL
        return FakeResponse(_release_json())

    result = fetch_latest_release(opener=opener_ok)
    check("a good release parses to version + apk url + tag",
          result == {"version": "1.7.0",
                     "apk_url": "https://example.com/habit-garden.apk",
                     "tag": "v1.7.0"})
    check("the .apk asset is picked, other assets ignored",
          result["apk_url"].endswith("habit-garden.apk"))

    def opener_no_apk(url):
        return FakeResponse(_release_json(assets=[
            {"name": "notes.txt",
             "browser_download_url": "https://example.com/notes.txt"}]))

    check("a release with no .apk asset returns None",
          fetch_latest_release(opener=opener_no_apk) is None)

    def opener_no_tag(url):
        return FakeResponse(_release_json(tag=""))

    check("a release with no tag returns None",
          fetch_latest_release(opener=opener_no_tag) is None)

    def opener_bad_json(url):
        return FakeResponse(b"not json{{{")

    check("bad JSON returns None instead of raising",
          fetch_latest_release(opener=opener_bad_json) is None)

    def opener_offline(url):
        raise urllib.error.URLError("no network")

    check("a network error returns None instead of raising",
          fetch_latest_release(opener=opener_offline) is None)


def test_download_apk():
    data = b"fake-apk-bytes" * 5000  # 70_000 bytes, several chunks

    def opener(url):
        return FakeResponse(data, headers={
            "Content-Length": str(len(data))})

    seen = []

    def progress(done, total):
        seen.append((done, total))

    with tempfile.TemporaryDirectory() as folder:
        dest = os.path.join(folder, "habit-garden.apk")
        result = download_apk("https://example.com/habit-garden.apk",
                              dest, progress_cb=progress, opener=opener)
        check("download_apk returns the destination path",
              result == dest)
        with open(dest, "rb") as f:
            check("the downloaded file holds every byte",
                  f.read() == data)
        check("progress is reported as it downloads",
              len(seen) >= 2)
        check("the last progress call reports the full size",
              seen[-1] == (len(data), len(data)))
        check("progress never exceeds the total",
              all(done <= total for done, total in seen))

    def opener_no_length(url):
        return FakeResponse(data, headers={})

    seen_no_length = []
    with tempfile.TemporaryDirectory() as folder:
        dest = os.path.join(folder, "habit-garden.apk")
        download_apk("https://example.com/habit-garden.apk", dest,
                     progress_cb=lambda d, t: seen_no_length.append((d, t)),
                     opener=opener_no_length)
        check("a download without Content-Length still works",
              os.path.getsize(dest) == len(data))
        check("total is None when the server sends no length",
              all(total is None for _done, total in seen_no_length))

    def opener_fails(url):
        raise urllib.error.URLError("no network")

    with tempfile.TemporaryDirectory() as folder:
        dest = os.path.join(folder, "habit-garden.apk")
        try:
            download_apk("https://example.com/habit-garden.apk",
                         dest, opener=opener_fails)
            raised = False
        except urllib.error.URLError:
            raised = True
        check("a failed download raises for the caller to handle",
              raised)


def test_default_apk_path():
    check("the default APK path ends with habit-garden.apk",
          default_apk_path().endswith("habit-garden.apk"))
    check("the default APK path is absolute",
          os.path.isabs(default_apk_path()))


if __name__ == "__main__":
    test_is_newer()
    test_fetch_latest_release()
    test_download_apk()
    test_default_apk_path()
    print(f"{PASSED} tests passed")
