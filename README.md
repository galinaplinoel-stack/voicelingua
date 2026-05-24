# VoiceLingua — AI Voice Translator

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue" alt="version">
  <img src="https://img.shields.io/badge/python-3.10+-blue" alt="python">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="license">
</p>

> 🌐 AI-powered translator with natural voice synthesis. Translate text, speak it aloud, or use your voice to translate in real-time.

## ✨ Features

- 🎤 **Voice Input** — Speak naturally in any language, AI recognizes speech
- 🔊 **Natural Voice Output** — Hear translations with human-like voices
- ⚡ **Real-Time Translation** — Instant translations as you type
- 🌍 **14+ Languages** — English, Indonesian, Japanese, Korean, Chinese, Spanish, French, German, Arabic, Portuguese, Russian, Hindi, Thai, Vietnamese
- 📝 **Context Aware** — Understands idioms, slang, and context
- 💾 **Save & Export** — Download audio, save history, export conversations

## 📁 Project Structure

```
voicelingua/
├── voicelingua/              # Core Python package
│   ├── __init__.py           # Package init + version
│   ├── translator.py         # Translation engine
│   ├── voice.py              # Voice synthesis & recognition
│   ├── languages.py          # Language definitions & mappings
│   └── history.py            # Translation history manager
├── api/                      # REST API server
│   ├── __init__.py
│   └── main.py               # FastAPI application
├── web/                      # Frontend
│   └── index.html            # Interactive web UI
├── data/                     # Data files
│   └── dictionary.json       # Offline translation dictionary
├── tests/                    # Test suite
│   ├── __init__.py
│   └── test_translator.py    # Translator tests
├── config.example.yaml       # Configuration template
├── requirements.txt          # Python dependencies
├── setup.py                  # Package setup
├── vercel.json               # Vercel deployment config
├── .gitignore
├── LICENSE
└── README.md
```

## 🚀 Quick Start

### Install
```bash
pip install -r requirements.txt
```

### Run API Server
```bash
cd api
uvicorn main:app --reload --port 8001
```

### Run Web Interface
```bash
cd web
python -m http.server 3001
# Open http://localhost:3001
```

### Use as Python Library
```python
from voicelingua import Translator, VoiceSynthesizer

# Text translation
translator = Translator()
result = translator.translate(
    text="Hello, how are you?",
    source="en",
    target="id"
)
print(result)  # "Halo, apa kabar?"

# Voice synthesis
voice = VoiceSynthesizer()
voice.speak(result, language="id")
```

## 🔧 Configuration

Copy `config.example.yaml` to `config.yaml`:

```yaml
api:
  host: "0.0.0.0"
  port: 8001

translator:
  default_source: "en"
  default_target: "id"
  engine: "local"           # local or api
  cache_enabled: true

voice:
  engine: "browser"         # browser, google, or azure
  default_rate: 0.9
  auto_detect_language: true
```

## 🧪 Testing

```bash
python -m pytest tests/ -v
```

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

Breaking language barriers with AI ❤️
