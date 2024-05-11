import os
from gensim import corpora, models
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
    dictionary = corpora.Dictionary(documents)
    corpus = [dictionary.doc2bow(doc) for doc in documents]
    lda_model = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=passes)
    return lda_model, dictionary, corpus

def print_lda_topics(num_words, lda_model):
    print("LDA TOPICS")
    for topic_id in range(lda_model.num_topics):
        topic_words = lda_model.show_topic(topic_id, topn=num_words)
        print(f"Topic {topic_id}:")
        words = ', '.join([word for word, prob in topic_words])
        print(words)
    print("")

def get_topic_probability(lda_model, dictionary, document):
    bow = dictionary.doc2bow(preprocess(document))
    topic_probability = lda_model[bow]
    return topic_probability

def main():
    directory = "papers/abstract"
    documents = process_documents(directory)
    lda_model, dictionary, corpus = train_lda(documents)
    num_words = 10
    print_lda_topics(num_words, lda_model)
    for abstract in os.listdir(directory):
        if abstract.endswith(".txt"):
            with open(os.path.join(directory, abstract), 'r', encoding='utf-8') as file:
                document = file.read()
                topic_probability = get_topic_probability(lda_model, dictionary, document)
                print(f"Abstract {abstract}")
                for topic, prob in topic_probability:
                    print(f"Topic: {topic}, Probability: {prob:.4f}")

if __name__=="__main__":
    main()
