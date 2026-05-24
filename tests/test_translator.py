"""Tests for VoiceLingua translator."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from voicelingua import Translator, VoiceSynthesizer, LanguageManager


def test_translate_en_to_id():
    """Test English to Indonesian translation."""
    t = Translator()
    result = t.translate("hello", "en", "id")
    assert result.translated_text == "halo"


def test_translate_id_to_en():
    """Test Indonesian to English translation."""
    t = Translator()
    result = t.translate("terima kasih", "id", "en")
    assert result.translated_text == "thank you"


def test_translate_en_to_ja():
    """Test English to Japanese translation."""
    t = Translator()
    result = t.translate("hello", "en", "ja")
    assert "こんにちは" in result.translated_text


def test_translate_en_to_es():
    """Test English to Spanish translation."""
    t = Translator()
    result = t.translate("hello", "en", "es")
    assert "hola" in result.translated_text


def test_detect_language():
    """Test language detection."""
    t = Translator()
    assert t.detect_language("halo apa kabar") == "id"


def test_invalid_language():
    """Test invalid language raises error."""
    t = Translator()
    try:
        t.translate("hello", "xx", "en")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_empty_text():
    """Test empty text raises error."""
    t = Translator()
    try:
        t.translate("", "en", "id")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_language_manager():
    """Test language manager."""
    lm = LanguageManager()
    assert lm.is_supported("en")
    assert lm.is_supported("ja")
    assert not lm.is_supported("xx")
    assert len(lm.list_codes()) >= 14


def test_voice_synthesizer():
    """Test voice synthesizer."""
    vs = VoiceSynthesizer()
    voice = vs.get_voice("en")
    assert voice is not None
    assert voice.language == "en"


def test_history():
    """Test translation history."""
    t = Translator()
    t.translate("hello", "en", "id")
    t.translate("world", "en", "id")
    assert t.history.count >= 2


if __name__ == "__main__":
    tests = [
        test_translate_en_to_id,
        test_translate_id_to_en,
        test_translate_en_to_ja,
        test_translate_en_to_es,
        test_detect_language,
        test_invalid_language,
        test_empty_text,
        test_language_manager,
        test_voice_synthesizer,
        test_history,
    ]
    for t in tests:
        try:
            t()
            print(f"  ✅ {t.__name__}")
        except Exception as e:
            print(f"  ❌ {t.__name__}: {e}")
    print("\nAll tests complete!")
