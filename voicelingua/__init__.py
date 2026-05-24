"""VoiceLingua — AI Voice Translator

Translate text across 14+ languages with natural voice synthesis.
"""

__version__ = "1.0.0"
__author__ = "VoiceLingua Team"

from .translator import Translator
from .voice import VoiceSynthesizer
from .languages import LanguageManager
from .history import HistoryManager

__all__ = ["Translator", "VoiceSynthesizer", "LanguageManager", "HistoryManager"]
