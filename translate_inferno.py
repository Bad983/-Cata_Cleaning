from transformers import pipeline

model_checkpoint = "Helsinki-NLP/opus-mt-en-it"
translator = pipeline("translation", model=model_checkpoint)

trad = translator("How are you?")
print(trad[0]['translation_text'])
