"""Utility helpers extracted from the original app."""
from urllib.parse import quote as urlencode, unquote
import hashlib
import re
from typing import Optional
from argon2 import PasswordHasher

ph = PasswordHasher()
forbidden_pattern = re.compile(r"%p(.*?%s)*.*?%")


def get_md5(s: Optional[str]) -> str:
    if not s:
        return ''
    return hashlib.md5(s.encode()).hexdigest()


def is_forbidden(s: Optional[str]) -> bool:
    if s is None:
        return False
    return bool(forbidden_pattern.search(s))


def encode(s: Optional[str]) -> str:
    return urlencode(s) if s is not None else ''


def decode(s: Optional[str]) -> str:
    return unquote(s) if s is not None else ''
