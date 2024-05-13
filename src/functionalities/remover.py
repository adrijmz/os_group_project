import os
from nltk.tokenize import word_tokenize

def delete_all_but_letters_and_spaces(text):
    return ''.join(e for e in text if e.isalnum() or e.isspace())

def tokenize_text(read_dir, write_dir):
    for filename in os.listdir(read_dir):       
        if filename.endswith(".txt"):
            abstract_path = os.path.join(read_dir, filename)
            with open(abstract_path, "r") as abstract_file:
                text = abstract_file.read()
                text = delete_all_but_letters_and_spaces(text)
                tokens = word_tokenize(text)
                text_tokenized_file = os.path.join(write_dir, filename)
                with open(text_tokenized_file, "w") as text_tokenized:
                    for token in tokens:
                        text_tokenized.write(token + " ")

if __name__ == "__main__":
    abstract_directory = '../../papers/abstract/'
    acknowledgements_directory = '../../papers/acknowledgements/'
    tokenized_abstract_directory = '../../papers/token/abstract/'
    tokenized_acknowledgements_directory = '../../papers/token/acknowledgements/'

    os.makedirs(tokenized_abstract_directory, exist_ok=True)
    os.makedirs(tokenized_acknowledgements_directory, exist_ok=True)

    tokenize_text(abstract_directory, tokenized_abstract_directory)
    tokenize_text(acknowledgements_directory, tokenized_acknowledgements_directory)
    