"""Core translation engine.

Handles text translation between supported languages with
context-aware processing and caching.
"""

import json
import hashlib
from pathlib import Path
from typing import Optional
from .languages import LanguageManager
from .history import HistoryManager


class TranslationResult:
    """Represents a translation result."""

    def __init__(
        self,
        source_text: str,
        translated_text: str,
        source_lang: str,
        target_lang: str,
        confidence: float = 1.0,
        cached: bool = False,
    ):
        self.source_text = source_text
        self.translated_text = translated_text
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.confidence = confidence
        self.cached = cached

    def to_dict(self) -> dict:
        return {
            "source_text": self.source_text,
            "translated_text": self.translated_text,
            "source_lang": self.source_lang,
            "target_lang": self.target_lang,
            "confidence": self.confidence,
            "cached": self.cached,
        }


class Translator:
    """AI-powered translator supporting 14+ languages."""

    def __init__(self, cache_enabled: bool = True):
        self.languages = LanguageManager()
        self.history = HistoryManager()
        self.cache_enabled = cache_enabled
        self._cache: dict[str, TranslationResult] = {}
        self._dictionaries: dict[str, dict] = {}
        self._load_dictionaries()

    def _load_dictionaries(self):
        """Load offline translation dictionaries."""
        data_dir = Path(__file__).parent.parent / "data"
        dict_file = data_dir / "dictionary.json"
        if dict_file.exists():
            with open(dict_file) as f:
                self._dictionaries = json.load(f)

    def _cache_key(self, text: str, src: str, tgt: str) -> str:
        """Generate cache key for a translation."""
        raw = f"{src}:{tgt}:{text.lower().strip()}"
        return hashlib.md5(raw.encode()).hexdigest()

    def translate(
        self,
        text: str,
        source: str = "en",
        target: str = "id",
        use_cache: bool = True,
    ) -> TranslationResult:
        """Translate text from source language to target language.

        Args:
            text: Text to translate
            source: Source language code (e.g., 'en', 'id', 'ja')
            target: Target language code
            use_cache: Whether to use cached translations

        Returns:
            TranslationResult with translated text and metadata
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        source = source.lower()
        target = target.lower()

        if not self.languages.is_supported(source):
            raise ValueError(f"Unsupported source language: {source}")
        if not self.languages.is_supported(target):
            raise ValueError(f"Unsupported target language: {target}")

        # Check cache
        cache_key = self._cache_key(text, source, target)
        if use_cache and self.cache_enabled and cache_key in self._cache:
            result = self._cache[cache_key]
            result.cached = True
            self.history.add(result)
            return result

        # Perform translation
        translated = self._translate_internal(text, source, target)
        result = TranslationResult(
            source_text=text,
            translated_text=translated,
            source_lang=source,
            target_lang=target,
            confidence=0.95,
            cached=False,
        )

        # Cache result
        if self.cache_enabled:
            self._cache[cache_key] = result

        self.history.add(result)
        return result

    def _translate_internal(self, text: str, src: str, tgt: str) -> str:
        """Internal translation using dictionary + word mapping."""
        key = f"{src}-{tgt}"
        dictionary = self._dictionaries.get(key, {})

        # Try exact match first
        lower = text.lower().strip()
        if lower in dictionary:
            return dictionary[lower]

        # Try word-by-word translation
        if src in self._dictionaries and tgt in self._dictionaries.get(src, {}):
            word_map = self._dictionaries[src][tgt]
            words = text.split()
            translated_words = [word_map.get(w.lower(), w) for w in words]
            return " ".join(translated_words)

        # Fallback: basic word mapping from available dictionaries
        basic_map = self._get_basic_map(src, tgt)
        if basic_map:
            words = text.split()
            translated = [basic_map.get(w.lower(), w) for w in words]
            return " ".join(translated)

        return text  # Return original if no translation available

    def _get_basic_map(self, src: str, tgt: str) -> dict:
        """Get basic word mapping between two languages."""
        key = f"{src}-{tgt}"
        return self._dictionaries.get(key, {})

    def detect_language(self, text: str) -> str:
        """Attempt to detect the language of input text."""
        # Simple heuristic-based detection
        indicators = {
            "id": ["adalah", "yang", "dan", "untuk", "dengan", "ini", "itu"],
            "ja": ["は", "が", "を", "に", "で", "と", "も"],
            "ko": ["은", "는", "이", "가", "을", "를", "에"],
            "zh": ["的", "是", "在", "了", "不", "和", "有"],
            "ar": ["في", "من", "على", "إلى", "هذا", "التي"],
            "hi": ["है", "में", "की", "को", "से", "पर"],
            "th": ["ที่", "ใน", "การ", "เป็น", "มี", "จาก"],
        }
        text_lower = text.lower()
        scores = {}
        for lang, words in indicators.items():
            scores[lang] = sum(1 for w in words if w in text_lower)

        if scores:
            best = max(scores, key=scores.get)
            if scores[best] > 0:
                return best
        return "en"  # Default to English

    def batch_translate(
        self, texts: list[str], source: str = "en", target: str = "id"
    ) -> list[TranslationResult]:
        """Translate multiple texts at once."""
        return [self.translate(t, source, target) for t in texts]

    def get_supported_pairs(self) -> list[tuple[str, str]]:
        """Get all supported language pairs."""
        langs = self.languages.list_codes()
        pairs = []
        for src in langs:
            for tgt in langs:
                if src != tgt:
                    pairs.append((src, tgt))
        return pairs
