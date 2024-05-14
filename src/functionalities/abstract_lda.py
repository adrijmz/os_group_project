import os
from gensim.models import LdaModel
from gensim.corpora import Dictionary
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def process_documents(directory):
    documents = []
    for file_name in os.listdir(directory):
        if file_name.endswith(".txt"):
            with open(os.path.join(directory, file_name), 'r', encoding='utf-8') as file:
                document = file.read()
                documents.append(preprocess(document))
    return documents

def preprocess(text):
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text.lower())
    tokens = [token for token in tokens if token.isalpha()] 
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    tokens = [token for token in tokens if token not in stop_words]  
    return tokens

# Function to train the LDA model
def train_lda(documents, num_topics=10, passes=15):
    dictionary = Dictionary(documents)
    corpus = [dictionary.doc2bow(doc) for doc in documents]
    lda_model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=passes)
    return lda_model, dictionary, corpus

def get_lda_topics(num_words, lda_model):
    topics = []
    for topic_id in range(lda_model.num_topics):
        topic_words = lda_model.show_topic(topic_id, topn=num_words)
        words = [word for word, prob in topic_words]
        topics.append(words)
    return topics

def write_topics(topics, output_directory):
    with open(f"{output_directory}/topics.txt", 'w', encoding='utf-8') as file:
        for idx, topic_words in enumerate(topics):
            file.write(f"Topic {idx}: ")
            file.write(', '.join(topic_words) + '\n\n')

def get_topic_probability(lda_model, dictionary, document):
    bow = dictionary.doc2bow(preprocess(document))
    topic_probability = lda_model[bow]
    if topic_probability:
        max_prob_topic = max(topic_probability, key=lambda item: item[1])
        return max_prob_topic
    else:
        return None

def write_results(directory, abstract, topic, probability):
    with open(os.path.join(directory, f"{abstract}.txt"), 'w', encoding='utf-8') as file:
        file.write(f"Topic: {topic}, Probability: {probability:.4f}\n")

def process_abstracts(directory, lda_model, dictionary, output_directory, topics):
    for abstract in os.listdir(directory):
        if abstract.endswith(".txt"):
            with open(os.path.join(directory, abstract), 'r', encoding='utf-8') as file:
                document = file.read()
                max_topic_probability = get_topic_probability(lda_model, dictionary, document)
                if max_topic_probability is not None:
                    topic, prob = max_topic_probability
                    write_results(output_directory, os.path.splitext(abstract)[0], topics[topic], prob)
                else:
                    print(f"Error analyzing abstract {abstract} or zero probability")

def main():
    directory = "../../papers/abstract"
    output_directory = "../../papers/probabilities"
    topic_directory = "../../papers/topics"
    num_words = 10

    os.makedirs(output_directory, exist_ok=True)
    os.makedirs(topic_directory, exist_ok=True)

    documents = process_documents(directory)
    lda_model, dictionary, corpus = train_lda(documents)
    topics = get_lda_topics(num_words, lda_model)
    write_topics(topics, topic_directory)
    process_abstracts(directory, lda_model, dictionary, output_directory, topics)

if __name__=="__main__":
    main()
