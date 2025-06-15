from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "google/flan-t5-small"
_model = None
_tokenizer = None


def _load():
    global _model, _tokenizer
    if _model is None or _tokenizer is None:
        _model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    return _model, _tokenizer


def compress_context(context: str) -> str:
    """Return compressed context focusing on essential facts."""
    model, tokenizer = _load()
    prompt = f"Compress this context to essential facts:\n{context}"
    inputs = tokenizer(prompt, return_tensors="pt", max_length=2048, truncation=True)
    output = model.generate(**inputs, max_new_tokens=512)
    return tokenizer.decode(output[0], skip_special_tokens=True)
