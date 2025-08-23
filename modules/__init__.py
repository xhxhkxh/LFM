"""Modules package for the application.

This package exposes the major submodules so callers can import like
from modules import db, auth, forum
"""
# This file intentionally left minimal to mark the package.
__all__ = ["config", "utils", "db", "models", "auth", "forum", "errors"]
