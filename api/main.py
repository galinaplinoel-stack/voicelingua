"""VoiceLingua REST API server."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional

import sys
sys.path.insert(0, "..")
from voicelingua import Translator, VoiceSynthesizer, __version__

app = FastAPI(
    title="VoiceLingua API",
    description="AI Voice Translator API",
    version=__version__,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

translator = Translator()
voice = VoiceSynthesizer()


class TranslateRequest(BaseModel):
    text: str = Field(..., min_length=1)
    source: str = Field(default="en")
    target: str = Field(default="id")


@app.get("/")
def root():
    return {"name": "VoiceLingua API", "version": __version__, "status": "running"}


@app.post("/translate")
def translate(req: TranslateRequest):
    try:
        result = translator.translate(req.text, req.source, req.target)
        return result.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/languages")
def list_languages():
    return {"languages": translator.languages.list_all()}


@app.get("/voices")
def list_voices():
    return {"voices": voice.list_voices()}


@app.get("/history")
def get_history():
    return {"history": translator.history.get_all()}


@app.post("/detect")
def detect_language(text: str):
    detected = translator.detect_language(text)
    return {"language": detected, "text": text}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
