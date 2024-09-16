import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE
from sklearn.preprocessing import LabelEncoder
from textblob import TextBlob

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
from heapq import nlargest

class TextAnalysisService:
    def __init__(self, visualization_folder):
        self.visualization_folder = visualization_folder


    def summarize(self, text, num_sentences=3):
        try:
            nltk.download('punkt')
            nltk.download('stopwords')
            nltk.download('punkt_tab')

            # Tokenize the text into sentences and words
            sentences = sent_tokenize(text)
            words = word_tokenize(text.lower())

            # Remove stopwords
            stop_words = set(stopwords.words('english'))
            words = [word for word in words if word not in stop_words and word.isalnum()]

            # Calculate word frequencies
            freq = FreqDist(words)

            # Score sentences based on word frequencies
            sentence_scores = {}
            for sentence in sentences:
                for word in word_tokenize(sentence.lower()):
                    if word in freq:
                        if sentence not in sentence_scores:
                            sentence_scores[sentence] = freq[word]
                        else:
                            sentence_scores[sentence] += freq[word]

            # Get the top N sentences with highest scores
            summary_sentences = nlargest(num_sentences, sentence_scores, key=sentence_scores.get)

            # Join the summary sentences
            summary = ' '.join(summary_sentences)

            return summary
        except Exception as e:
            return f"Error: {str(e)}"

    def extract_keywords(self, text):
        vectorizer = TfidfVectorizer(stop_words='english')
        X = vectorizer.fit_transform([text])
        feature_names = vectorizer.get_feature_names_out()
        scores = np.asarray(X.sum(axis=0)).flatten()
        keywords = sorted(zip(feature_names, scores), key=lambda x: -x[1])
        return [keyword for keyword, score in keywords[:10]]

    def analyze_sentiment(self, text):
        analysis = TextBlob(text)
        sentiment = analysis.sentiment.polarity
        if sentiment > 0:
            return "positive"
        elif sentiment < 0:
            return "negative"
        else:
            return "neutral"

    def visualize_tsne(self, text):
        try:
            # Convert the text into a matrix of TF-IDF features
            vectorizer = TfidfVectorizer(stop_words='english')
            X = vectorizer.fit_transform([text])
            words = vectorizer.get_feature_names_out()  # Get the feature names (words)
            X_array = X.toarray()  # Convert sparse matrix to dense array

            # Check if we have enough data for t-SNE
            n_samples, n_features = X_array.shape
            if n_samples < 2 or n_features < 2:
                return {'error': 'Not enough data for t-SNE visualization. Please provide more text.'}

            # Determine the appropriate perplexity
            perplexity = min(30, max(2, n_samples - 1))  # Ensure perplexity is at least 2

            # Apply t-SNE (reduce dimensionality to 2D)
            tsne = TSNE(n_components=2, perplexity=perplexity, random_state=42)
            X_tsne = tsne.fit_transform(X_array)

            # Plot the t-SNE visualization
            plt.figure(figsize=(10, 7))
            plt.scatter(X_tsne[:, 0], X_tsne[:, 1])

            # Annotate points with the words
            for i, word in enumerate(words):
                plt.annotate(word, (X_tsne[i, 0], X_tsne[i, 1]))

            # Save the visualization
            visualization_filename = 'tsne_plot.png'
            visualization_path = os.path.join(self.visualization_folder, visualization_filename)
            plt.savefig(visualization_path)
            plt.close()

            return {'visualization_url': f'/static/visualizations/{visualization_filename}'}
        except Exception as e:
            return {'error': str(e)}



    def process_text(self, text, search_query=None, category=None, custom_query=None):
        results = {}
        
        if search_query:
            results['search_results'] = [word for word in text.split() if search_query.lower() in word.lower()]
        
        if category:
            # Placeholder: Implement category-based text processing
            results['category_results'] = f"Categorized under {category}"
        
        if custom_query:
            # Placeholder: Implement custom query processing
            results['custom_query_results'] = f"Results for {custom_query}"
        
        return results
