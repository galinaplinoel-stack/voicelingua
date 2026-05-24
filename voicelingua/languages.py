"""Language definitions and management for VoiceLingua."""


class Language:
    """Represents a supported language."""

    def __init__(
        self,
        code: str,
        name: str,
        native_name: str,
        flag: str,
        rtl: bool = False,
    ):
        self.code = code
        self.name = name
        self.native_name = native_name
        self.flag = flag
        self.rtl = rtl

    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "name": self.name,
            "native_name": self.native_name,
            "flag": self.flag,
            "rtl": self.rtl,
        }


class LanguageManager:
    """Manages all supported languages."""

    LANGUAGES = {
        "en": Language("en", "English", "English", "🇬🇧"),
        "id": Language("id", "Indonesian", "Bahasa Indonesia", "🇮🇩"),
        "ja": Language("ja", "Japanese", "日本語", "🇯🇵"),
        "ko": Language("ko", "Korean", "한국어", "🇰🇷"),
        "zh": Language("zh", "Chinese", "中文", "🇨🇳"),
        "es": Language("es", "Spanish", "Español", "🇪🇸"),
        "fr": Language("fr", "French", "Français", "🇫🇷"),
        "de": Language("de", "German", "Deutsch", "🇩🇪"),
        "ar": Language("ar", "Arabic", "العربية", "🇸🇦", rtl=True),
        "pt": Language("pt", "Portuguese", "Português", "🇧🇷"),
        "ru": Language("ru", "Russian", "Русский", "🇷🇺"),
        "hi": Language("hi", "Hindi", "हिन्दी", "🇮🇳"),
        "th": Language("th", "Thai", "ภาษาไทย", "🇹🇭"),
        "vi": Language("vi", "Vietnamese", "Tiếng Việt", "🇻🇳"),
    }

    def get(self, code: str) -> Language:
        """Get language by code."""
        if code not in self.LANGUAGES:
            raise KeyError(f"Unknown language code: {code}")
        return self.LANGUAGES[code]

    def is_supported(self, code: str) -> bool:
        """Check if a language code is supported."""
        return code in self.LANGUAGES

    def list_codes(self) -> list[str]:
        """List all supported language codes."""
        return list(self.LANGUAGES.keys())

    def list_all(self) -> list[dict]:
        """List all languages with metadata."""
        return [lang.to_dict() for lang in self.LANGUAGES.values()]

    def search(self, query: str) -> list[Language]:
        """Search languages by name or native name."""
        query = query.lower()
        return [
            lang for lang in self.LANGUAGES.values()
            if query in lang.name.lower() or query in lang.native_name.lower()
        ]
