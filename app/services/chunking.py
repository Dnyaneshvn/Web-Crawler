import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

logger = logging.getLogger(__name__)

def chunk_data(content: str):
    logger.info("Starting data chunking")
    sentences = content.split('. ')
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(sentences)

    true_k = int(len(sentences) ** 0.5)
    model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
    model.fit(X)

    clusters = {}
    for i, sentence in enumerate(sentences):
        label = model.labels_[i]
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(sentence)
    
    logger.info("Data chunking completed")
    return clusters