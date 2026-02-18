# core/__init__.py
"""Главная точка входа в функционал анализатора."""

from .analyzer import MTGCardAnalyzer

__all__ = ["MTGCardAnalyzer"]

# Удобный алиас для быстрого запуска
def analyze(count: int):
    """Quick start: проанализировать N карт."""
    return MTGCardAnalyzer().run(count)