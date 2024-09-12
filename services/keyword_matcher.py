import nltk
from utils.nltk_utils import cosine_similarity, initialize_nltk, load_glove_embeddings
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import numpy as np
from nltk.corpus import wordnet as wn

initialize_nltk()

embeddings_index = load_glove_embeddings()


def match_descriptors_nltk(
    listing_keywords,
    category_labels,
    top_n=5,
    embeddings_index=embeddings_index,
    dim=50,
):
    if embeddings_index is None:
        raise ValueError("Embeddings index is not loaded.")

    text = str(listing_keywords)
    text_vector = get_avg_word_vector(text, embeddings_index, dim)
    label_scores = {}

    # Calculate similarity scores
    for label in category_labels:
        label_vector = get_avg_word_vector(label, embeddings_index, dim)
        similarity = cosine_similarity(text_vector, label_vector)
        label_scores[label] = similarity

    # Apply dynamic weighting to give less common descriptors a higher chance of being selected
    weighted_scores = {}
    for label, score in label_scores.items():
        frequency = category_labels.count(label)
        weighted_scores[label] = score / (frequency + 1)

    # Sort and select top labels
    sorted_labels = sorted(weighted_scores, key=weighted_scores.get, reverse=True)

    # Introduce randomness by shuffling and selecting from top labels
    top_labels = sorted_labels[:top_n]

    return str(top_labels)



# Calculate the average word vectors for a given text
def get_avg_word_vector(text, embeddings_index, dim=50):
    tokens = word_tokenize(str(text).lower())
    stop_words = set(stopwords.words("english"))
    filtered_tokens = [
        token for token in tokens if token.isalnum() and token not in stop_words
    ]
    word_vectors = [
        embeddings_index[token]
        for token in filtered_tokens
        if token in embeddings_index
    ]

    if not word_vectors:
        return np.zeros(dim)

    avg_vector = np.mean(word_vectors, axis=0)
    return avg_vector


