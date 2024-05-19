from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import os
import json

acknowledges_dir = 'papers/acknowledgements'
ner_dir = 'papers/ner'

os.makedirs(ner_dir, exist_ok=True)

model_name = "dbmdz/bert-large-cased-finetuned-conll03-english"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(model_name)

results = []

nlp_ner = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")


for filename in os.listdir(acknowledges_dir):
    with open(os.path.join(acknowledges_dir, filename)) as f:
        with open(os.path.join(ner_dir, filename), 'w') as f2:
            entities = nlp_ner(f.read())
            filter_entities = []
            for entity in entities:
                if entity["entity_group"] == 'MISC' or entity['entity_group'] == 'ORG' or entity['entity_group'] == 'PER':
                    if entity['score'] > 0.85 and len(entity['word'])>1:
                        filter_entities.append(entity["word"])
            f2.write(str(filter_entities))