from transformers import DistilGPT2LMHeadModel, DistilGPT2Tokenizer

# DistilGPT 모델을 다운받고 초기화
tokenizer = DistilGPT2Tokenizer.from_pretrained('distilgpt2')
model = DistilGPT2LMHeadModel.from_pretrained('distilgpt2')

def generate_text(prompt: str) -> str:
    inputs = tokenizer(prompt, return_tensors='pt')
    outputs = model.generate(inputs['input_ids'], max_length=200)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
