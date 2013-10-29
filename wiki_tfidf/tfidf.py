from sklearn.feature_extraction.text import TfidfVectorizer
import lxml

def pairwiseSimilarity(documents):

        tfidf = TfidfVectorizer(min_df=1).fit_transform(documents)
        pairwise_similarity = tfidf * tfidf.T
        return pairwise_similarity

