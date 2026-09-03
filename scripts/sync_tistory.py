#!/usr/bin/env python3
"""Import public Tistory RSS entries as Jekyll posts."""

from __future__ import annotations

import argparse
import email.utils
import hashlib
import html
import json
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path


USER_AGENT = "p1ki-tistory-sync/1.0 (+https://p1ki-lab.github.io)"


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


@dataclass(frozen=True)
class Entry:
    title: str
    url: str
    published: datetime
    body: str
    category: str
    entry_id: str


def child_text(element: ET.Element, *names: str) -> str:
    for name in names:
        child = element.find(name)
        if child is not None and child.text:
            return child.text.strip()
    return ""


def parse_date(value: str) -> datetime:
    parsed = email.utils.parsedate_to_datetime(value)
    if parsed is None:
        raise ValueError(f"발행일을 해석할 수 없습니다: {value!r}")
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def stable_id(url: str, guid: str) -> str:
    source = guid or url
    path = urllib.parse.urlparse(url).path.rstrip("/")
    last_part = urllib.parse.unquote(path.rsplit("/", 1)[-1]) if path else ""
    if last_part.isdigit():
        return last_part
    return hashlib.sha256(source.encode("utf-8")).hexdigest()[:12]


def parse_feed(xml_bytes: bytes) -> list[Entry]:
    root = ET.fromstring(xml_bytes)
    items = root.findall("./channel/item")
    if not items:
        items = root.findall("{http://www.w3.org/2005/Atom}entry")

    entries: list[Entry] = []
    for item in items:
        title = child_text(item, "title", "{http://www.w3.org/2005/Atom}title")
        url = child_text(item, "link")
        if not url:
            atom_link = item.find("{http://www.w3.org/2005/Atom}link")
            if atom_link is not None:
                url = atom_link.attrib.get("href", "").strip()
        body = child_text(
            item,
            "{http://purl.org/rss/1.0/modules/content/}encoded",
            "description",
            "{http://www.w3.org/2005/Atom}content",
            "{http://www.w3.org/2005/Atom}summary",
        )
        date_text = child_text(
            item,
            "pubDate",
            "{http://www.w3.org/2005/Atom}published",
            "{http://www.w3.org/2005/Atom}updated",
        )
        guid = child_text(item, "guid", "{http://www.w3.org/2005/Atom}id")
        category = child_text(item, "category")

        if not (title and url and date_text):
            print("필수 값이 없는 RSS 항목을 건너뜁니다.", file=sys.stderr)
            continue
        entries.append(
            Entry(
                title=html.unescape(title),
                url=url,
                published=parse_date(date_text),
                body=body,
                category=html.unescape(category),
                entry_id=stable_id(url, guid),
            )
        )
    return entries


def plain_description(body: str, limit: int = 180) -> str:
    extractor = TextExtractor()
    extractor.feed(body)
    text = html.unescape(" ".join(extractor.parts))
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def clean_body(body: str) -> str:
    body = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)
    body = re.sub(r"<script\b[^>]*>.*?</script\s*>", "", body, flags=re.DOTALL | re.IGNORECASE)
    return body.strip()


def yaml_value(value: object) -> str:
    return json.dumps(value, ensure_ascii=False)


def render_post(entry: Entry, category_prefix: str) -> str:
    categories = [category_prefix]
    if entry.category and entry.category != category_prefix:
        categories.append(entry.category)
    published = entry.published.isoformat()
    notice_url = html.escape(entry.url, quote=True)
    body = clean_body(entry.body)
    return "\n".join(
        [
            "---",
            "layout: post",
            f"title: {yaml_value(entry.title)}",
            f"description: {yaml_value(plain_description(body))}",
            f"date: {yaml_value(published)}",
            f"categories: {yaml_value(categories)}",
            "tags: []",
            f"canonical_url: {yaml_value(entry.url)}",
            f"tistory_url: {yaml_value(entry.url)}",
            f"tistory_post_id: {yaml_value(entry.entry_id)}",
            "tistory_synced: true",
            "---",
            "",
            f'<p class="tistory-source">이 글은 <a href="{notice_url}">티스토리 원문</a>에서 자동으로 가져왔습니다.</p>',
            "",
            "{% raw %}",
            body,
            "{% endraw %}",
            "",
        ]
    )


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def load_config(path: Path) -> dict[str, object]:
    with path.open(encoding="utf-8") as handle:
        config = json.load(handle)
    url = str(config.get("rss_url", "")).strip()
    if not url.startswith(("https://", "http://")):
        raise ValueError(".tistory-sync.json의 rss_url에 티스토리 RSS 주소를 입력해 주세요.")
    return config


def sync(config_path: Path, posts_dir: Path) -> tuple[int, int]:
    config = load_config(config_path)
    rss_url = str(config["rss_url"])
    category_prefix = str(config.get("category_prefix", "티스토리"))
    entries = parse_feed(fetch(rss_url))
    if not entries:
        print("RSS에 공개된 글이 아직 없습니다.")
        return 0, 0

    posts_dir.mkdir(parents=True, exist_ok=True)
    created = 0
    updated = 0
    for entry in entries:
        filename = f"{entry.published:%Y-%m-%d}-tistory-{entry.entry_id}.html"
        destination = posts_dir / filename
        rendered = render_post(entry, category_prefix)
        previous = destination.read_text(encoding="utf-8") if destination.exists() else None
        if previous == rendered:
            continue
        destination.write_text(rendered, encoding="utf-8", newline="\n")
        if previous is None:
            created += 1
        else:
            updated += 1
    return created, updated


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=Path(".tistory-sync.json"))
    parser.add_argument("--posts-dir", type=Path, default=Path("_posts"))
    args = parser.parse_args()
    try:
        created, updated = sync(args.config, args.posts_dir)
    except Exception as exc:
        print(f"티스토리 동기화 실패: {exc}", file=sys.stderr)
        return 1
    print(f"티스토리 동기화 완료: 새 글 {created}개, 수정 글 {updated}개")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
