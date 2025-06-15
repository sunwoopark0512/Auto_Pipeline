from transformers import AlbertTokenizer, AlbertForMaskedLM

# ALBERT 모델 로딩
tokenizer = AlbertTokenizer.from_pretrained('albert-base-v2')
model = AlbertForMaskedLM.from_pretrained('albert-base-v2')

def predict_masked_text(text: str) -> str:
    inputs = tokenizer(text, return_tensors='pt')
    outputs = model(**inputs)
    return tokenizer.decode(outputs.logits.argmax(dim=-1), skip_special_tokens=True)
