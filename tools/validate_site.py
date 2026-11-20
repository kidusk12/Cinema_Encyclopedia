#!/usr/bin/env python3
"""Validates the Cinema Archive: strict HTML5 parse, link/anchor/image checks, no CSS/JS."""
import os, re, sys
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
try:
    import html5lib
except ImportError:
    html5lib = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pages = sorted(os.path.join(d, f) for d, _, fs in os.walk(ROOT) for f in fs if f.endswith(".html"))
errors, ids, refs, stats = [], {}, [], dict(links=0, images=0)
BAD_TAGS = {"style", "script", "iframe", "object", "embed"}

class P(HTMLParser):
    def __init__(s, path): super().__init__(); s.path = path; s.ids = set(); s.text = []; s.h1 = 0; s.stack = []
    def handle_starttag(s, tag, attrs):
        a = dict(attrs); rel = os.path.relpath(s.path, ROOT)
        if tag in BAD_TAGS: errors.append(f"{rel}: forbidden <{tag}>")
        if tag == "link" and "stylesheet" in (a.get("rel") or ""): errors.append(f"{rel}: stylesheet link")
        if tag == "h1": s.h1 += 1
        for k, v in attrs:
            if k == "style": errors.append(f"{rel}: inline style attribute")
            if k.startswith("on"): errors.append(f"{rel}: event handler {k}")
            if k == "id": 
                if v in s.ids: errors.append(f"{rel}: duplicate id {v}")
                s.ids.add(v)
        if tag == "a" and a.get("href"): refs.append((s.path, a["href"], "link"))
        if tag in ("img", "source", "audio", "video") and a.get("src"): refs.append((s.path, a["src"], "img"))
        if tag == "form" and a.get("action"): refs.append((s.path, a["action"], "link"))
    def handle_data(s, d): s.text.append(d)

for path in pages:
    src = open(path, encoding="utf-8").read(); rel = os.path.relpath(path, ROOT)
    if html5lib:
        try: html5lib.HTMLParser(strict=True).parse(src)
        except Exception as e: errors.append(f"{rel}: HTML5 parse error: {e}")
    if "javascript:" in src.lower(): errors.append(f"{rel}: javascript: URL")
    if "lorem ipsum" in src.lower(): errors.append(f"{rel}: lorem ipsum")
    if not src.lstrip().lower().startswith("<!doctype html>"): errors.append(f"{rel}: missing doctype")
    p = P(path); p.feed(src); ids[path] = p.ids
    if p.h1 != 1: errors.append(f"{rel}: expected exactly one h1, found {p.h1}")
    if len("".join(p.text).split()) < 60: errors.append(f"{rel}: suspiciously little content")

for path, ref, kind in refs:
    rel = os.path.relpath(path, ROOT); u = urlparse(ref)
    if u.scheme or ref.startswith("//"): errors.append(f"{rel}: external reference {ref}"); continue
    stats["images" if kind == "img" else "links"] += 1
    target = path if not u.path else os.path.normpath(os.path.join(os.path.dirname(path), unquote(u.path)))
    if not os.path.exists(target): errors.append(f"{rel}: broken {kind} -> {ref}"); continue
    if u.fragment and target.endswith(".html") and u.fragment not in ids.get(target, set()):
        errors.append(f"{rel}: missing anchor #{u.fragment} in {os.path.relpath(target, ROOT)}")

for f in ("SOURCES.md", "README.md"):
    if not os.path.exists(os.path.join(ROOT, f)): errors.append(f"missing {f}")
movies = [p for p in pages if os.sep + "movies" + os.sep in p]
print(f"HTML files: {len(pages)} (movie pages: {len(movies)}); local links checked: {stats['links']}; image refs: {stats['images']}; strict HTML5 parser: {'yes' if html5lib else 'NO (html5lib missing)'}")
print("\n".join(errors) if errors else "ALL CHECKS PASSED")
sys.exit(1 if errors else 0)
