import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def preprocess(text):
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text.lower())
    tokens = [token for token in tokens if token.isalpha()] 
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    tokens = [token for token in tokens if token not in stop_words]  
    return ' '.join(tokens)

def compare_abstracts(abstract1, abstract2):
    processed_abstract1 = preprocess(abstract1)
    processed_abstract2 = preprocess(abstract2)
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([processed_abstract1, processed_abstract2])
    
    similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return similarity_score[0][0]

def read_abstract(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def main():
    abstract_dir = "papers/abstract"
    similarities_dir = "papers/similarities"
    abstarct_to_show = 10

    os.makedirs(similarities_dir, exist_ok=True)
    
    print("Calculating similarities between abstracts...\n")
    similarities = []
    abstract_files = os.listdir(abstract_dir)
    total_comparisons = sum(range(len(abstract_files)))
    progress = 0
    for i, abstract_file1 in enumerate(abstract_files):
        for abstract_file2 in abstract_files[i+1:]:
            abstract1 = read_abstract(os.path.join(abstract_dir, abstract_file1))
            abstract2 = read_abstract(os.path.join(abstract_dir, abstract_file2))
            similarity = compare_abstracts(abstract1, abstract2)
            similarities.append([abstract_file1, abstract_file2, similarity])
            progress += 1
            percentage = (progress / total_comparisons) * 100
            bar_length = 20
            num_hashes = int(percentage / (100 / bar_length))
            num_spaces = bar_length - num_hashes
            progress_bar = "[" + "#" * num_hashes + " " * num_spaces + "]"
            print(f"\rProgress: {progress_bar} {percentage:.2f}%", end="", flush=True)
    print("\n")

    similarities.sort(key=lambda x: x[2], reverse=True)
    with open(os.path.join(similarities_dir, "similarities.txt"), 'w', encoding='utf-8') as file:
        for i in range(min(abstarct_to_show, len(similarities))):
            abstract_file1, abstract_file2, similarity = similarities[i]
            print(f"Abstract {abstract_file1} and Abstract {abstract_file2} have a similarity of {similarity:.4f}")
            file.write(f"{abstract_file1};{abstract_file2};{similarity:.4f}\n")


if __name__ == "__main__":
    main()
