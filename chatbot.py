import re
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

import string

def preprocess_query(query):
    """Preprocess a single user-query string to match the preprocessing of sentences.
    Args:
        query : str : Query text
    Returns:
        list : List of preprocessed words
    """
    words = word_tokenize(query)
    words = [word.lower() for word in words if word.lower() not in stopwords.words('english') and word not in string.punctuation]
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    return words

def preprocess(text_data):
    """Preprocess the text data by converting to lowercase, removing non-alphabetic characters, 
    tokenizing into sentences, lemmatizing, and removing stopwords.
    
    Args:
        text_data : str : Text data to be preprocessed   
    Returns:
        processed_sentences : list : List of preprocessed sentences
    """
    sentences = sent_tokenize(text_data)
    
    # preprocess each sentence
    def process_sentence(sentence):
        words = word_tokenize(sentence)
        words = [word.lower() for word in words if word.lower() not in stopwords.words('english') and word not in string.punctuation]
        lemmatizer = WordNetLemmatizer()
        words = [lemmatizer.lemmatize(word) for word in words]
        return words

    # Preprocess each sentence in the text
    corpus = [process_sentence(sentence) for sentence in sentences]
    return corpus

def get_most_relevant_sentence(query, sentences):
    """Get the most relevant sentence based on cosine similarity between the query and the sentences.
    
    Args:
        query : str/ list : Query text
        sentences : list : List of sentences to compare the query against
    Returns:
        str : Most relevant sentence
    """
    # Convert query to a set of words
    if isinstance(query, str):
        query_set = set(preprocess_query(query)) # Preprocess the query first
    
    elif isinstance(query, list):
        query_set = set(query)  # Assume it's already split into words
    else:
        raise ValueError("Query must be a string or a list of words.")

    max_similarity = 0
    most_relevant_sentence = ""

    for sentence in sentences:
        # Ensure sentence is a string, then split into words
        if isinstance(sentence, str):
            sentence_set = set(sentence.split())
        elif isinstance(sentence, list):
            sentence_set = set(sentence)  # Assume it's already split into words
        else:
            raise ValueError("Each sentence must be a string or a list of words.")

        # Calculate similarity using set operations
        similarity = len(query_set.intersection(sentence_set)) / float(len(query_set.union(sentence_set)))

        # Keep track of the most similar sentence
        if similarity > max_similarity:
            max_similarity = similarity
            most_relevant_sentence = sentence

    return most_relevant_sentence

def chatbot(query, sentences):
    """ Chatbot function that takes a query and a list of preprocessed sentences and returns the most relevant sentence.
    
    Args:
        query : str : Query text
        sentences : list : List of preprocessed sentences
    Returns:
        str : Response from the chatbot.
    """
    most_relevant_sentence = get_most_relevant_sentence(query, sentences)
    # Return the answer
    return most_relevant_sentence

def chatbot(query, sentences):
    """ Chatbot function that takes a query and a list of preprocessed sentences and returns a conversational response.
    
    Args:
        query : str : Query text
        sentences : list : List of preprocessed sentences
    Returns:
        str : Response from the chatbot.
    """

    most_relevant_sentence = get_most_relevant_sentence(query, sentences)
    if most_relevant_sentence:
        if isinstance(most_relevant_sentence, list):
            most_relevant_sentence = " ".join(most_relevant_sentence)
        # Add a conversational wrapper to the response
        return f"Here’s what I found: '{most_relevant_sentence}'. Let me know if you'd like more details!"
    else:
        return None