import os
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Tokenization and preprocessing
nltk.download('punkt')
nltk.download('stopwords')

def read_files(file_paths):
    documents = []
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            content = file.read()
            documents.append(content)
    return documents

def preprocess(document):
    stop_words = set(stopwords.words('english'))
    ps = PorterStemmer()

    tokens = nltk.word_tokenize(document)
    tokens = [ps.stem(token.lower()) for token in tokens if token.isalnum()]
    tokens = [token for token in tokens if token not in stop_words]

    return ' '.join(tokens)

def inverted_index(query):
    processed_documents = [preprocess(doc) for doc in documents]

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(processed_documents)
    # Preprocess Query
    processed_query = preprocess(query)
    # Vectorize Query
    query_vector = vectorizer.transform([processed_query])

     # Inverted Index
    inverted_index = {}
    for doc_id, processed_doc in enumerate(processed_documents):
        terms = processed_doc.split()
        for term in terms:
            if term not in inverted_index:
                inverted_index[term] = [doc_id]
            else:
                inverted_index[term].append(doc_id)
    # Display Inverted Index
    print("\nInverted Index:")
    for term, doc_ids in inverted_index.items():
        print(f"{term}: {doc_ids}")

    evaluation(tfidf_matrix, query_vector)

   
def evaluation(tfidf_matrix, query_vector):
    # Calculate Cosine Similarity
    cosine_similarities = cosine_similarity(tfidf_matrix, query_vector).flatten()
    # Rank documents based on similarity
    document_ranking = sorted(enumerate(cosine_similarities), key=lambda x: x[1], reverse=True)
    # Display Results
    for index, score in document_ranking:
        print(f"Document {index + 1}: Similarity Score = {score:.4f}")
        print(documents[index])
        print("=" * 50)


file_paths = ["D:\\Users\\inesa\\OneDrive\\Desktop\\test.txt", "D:\\Users\\inesa\\OneDrive\\Desktop\\test2.txt"]
documents = read_files(file_paths)
query = "test"
inverted_index(query)