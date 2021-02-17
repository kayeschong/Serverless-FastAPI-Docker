# coding: utf8
from fastapi import FastAPI
from pydantic import BaseModel
import spacy
from spacy.matcher import Matcher
from typing import List, Dict


app = FastAPI()

MODELS = {"en_core_web_sm": spacy.load("en_core_web_sm")}


class MatchData(BaseModel):
    text: str
    # Pattern format changed for spacy v3
    pattern: List[
        List[Dict[str, str]]
    ]


def get_model_desc(nlp, model_name):
    """Get human-readable model name, language name and version."""
    lang_cls = spacy.util.get_lang_class(nlp.lang)
    lang_name = lang_cls.__name__
    model_version = nlp.meta["version"]
    return "{} - {} (v{})".format(lang_name, model_name, model_version)


@app.get("/models")
def models():
    return {name: get_model_desc(nlp, name) for name, nlp in MODELS.items()}


@app.post("/match")
def match(model: str, data: MatchData):
    nlp = MODELS[model]

    matcher = Matcher(nlp.vocab)
    matcher.add("PATTERN", data.pattern) # pattern args changed for v3
    
    doc = nlp(data.text)
    tokens = []
    matches = []
    match_tokens = set()

    for _, start, end in matcher(doc):
        if start >= end:  # filter out null matches or results of weird bug
            continue
        span = doc[start:end]
        if span[0].i in match_tokens:  # filter out overlaps
            continue
        match_tokens.update([t.i for t in span])
        matches.append(
            {"start": span.start_char, "end": span.end_char, "label": "MATCH"}
        )

    for t in doc:
        start = t.idx
        end = t.idx + len(t.text)
        label = "MATCH" if t.i in match_tokens else "TOKEN"
        tokens.append({"start": start, "end": end, "label": label})
    return {"matches": matches, "tokens": tokens}
