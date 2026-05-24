"""Voice synthesis and recognition module.

Handles text-to-speech output and speech-to-text input
for the VoiceLingua translator.
"""

from typing import Optional


class VoiceProfile:
    """Represents a voice profile for synthesis."""

    def __init__(
        self,
        name: str,
        language: str,
        gender: str = "neutral",
        rate: float = 1.0,
        pitch: float = 1.0,
    ):
        self.name = name
        self.language = language
        self.gender = gender
        self.rate = rate
        self.pitch = pitch

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "language": self.language,
            "gender": self.gender,
            "rate": self.rate,
            "pitch": self.pitch,
        }


class VoiceSynthesizer:
    """Text-to-speech engine with multi-language support."""

    DEFAULT_VOICES = {
        "en": VoiceProfile("en-US-Standard", "en", "neutral", 0.9),
        "id": VoiceProfile("id-ID-Standard", "id", "neutral", 0.9),
        "ja": VoiceProfile("ja-JP-Standard", "ja", "neutral", 0.85),
        "ko": VoiceProfile("ko-KR-Standard", "ko", "neutral", 0.85),
        "zh": VoiceProfile("cmn-CN-Standard", "zh", "neutral", 0.9),
        "es": VoiceProfile("es-ES-Standard", "es", "neutral", 0.95),
        "fr": VoiceProfile("fr-FR-Standard", "fr", "neutral", 0.9),
        "de": VoiceProfile("de-DE-Standard", "de", "neutral", 0.9),
        "ar": VoiceProfile("ar-SA-Standard", "ar", "neutral", 0.85),
        "pt": VoiceProfile("pt-BR-Standard", "pt", "neutral", 0.95),
        "ru": VoiceProfile("ru-RU-Standard", "ru", "neutral", 0.85),
        "hi": VoiceProfile("hi-IN-Standard", "hi", "neutral", 0.9),
        "th": VoiceProfile("th-TH-Standard", "th", "neutral", 0.85),
        "vi": VoiceProfile("vi-VN-Standard", "vi", "neutral", 0.9),
    }

    def __init__(self, engine: str = "browser"):
        self.engine = engine
        self.voices = dict(self.DEFAULT_VOICES)

    def get_voice(self, language: str) -> Optional[VoiceProfile]:
        """Get voice profile for a language."""
        return self.voices.get(language)

    def set_voice(self, language: str, profile: VoiceProfile):
        """Set custom voice profile for a language."""
        self.voices[language] = profile

    def get_synthesis_config(self, language: str) -> dict:
        """Get synthesis configuration for browser TTS API."""
        voice = self.get_voice(language)
        if not voice:
            return {"lang": language, "rate": 0.9, "pitch": 1.0}
        return {
            "lang": f"{language}",
            "rate": voice.rate,
            "pitch": voice.pitch,
            "voiceName": voice.name,
        }

    def list_voices(self) -> list[dict]:
        """List all available voice profiles."""
        return [v.to_dict() for v in self.voices.values()]

    def update_rate(self, language: str, rate: float):
        """Update speaking rate for a language voice."""
        if language in self.voices:
            self.voices[language].rate = max(0.1, min(2.0, rate))

    def update_pitch(self, language: str, pitch: float):
        """Update pitch for a language voice."""
        if language in self.voices:
            self.voices[language].pitch = max(0.0, min(2.0, pitch))


class SpeechRecognizer:
    """Speech-to-text engine for voice input."""

    def __init__(self):
        self._supported_langs = [
            "en", "id", "ja", "ko", "zh", "es", "fr",
            "de", "ar", "pt", "ru", "hi", "th", "vi",
        ]

    def is_supported(self, language: str) -> bool:
        """Check if language is supported for speech recognition."""
        return language in self._supported_langs

    def get_recognition_config(self, language: str) -> dict:
        """Get speech recognition configuration for browser API."""
        lang_map = {
            "en": "en-US", "id": "id-ID", "ja": "ja-JP",
            "ko": "ko-KR", "zh": "zh-CN", "es": "es-ES",
            "fr": "fr-FR", "de": "de-DE", "ar": "ar-SA",
            "pt": "pt-BR", "ru": "ru-RU", "hi": "hi-IN",
            "th": "th-TH", "vi": "vi-VN",
        }
        return {
            "lang": lang_map.get(language, language),
            "continuous": False,
            "interimResults": False,
        }

    def list_supported(self) -> list[str]:
        """List all supported recognition languages."""
        return self._supported_langs.copy()
