from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime


def get_cosine_sim(*strs):
    vectors = [t for t in get_vectors(*strs)]
    return cosine_similarity(vectors)


def get_vectors(*strs):
    text = [t for t in strs]
    vectorizer = CountVectorizer(text)
    vectorizer.fit(text)
    return vectorizer.transform(text).toarray()


def match(s, arrs):
    print('Matching')
    start_time = datetime.now()
    max_sim = 0
    max_indx = 0
    for i in range(len(arrs)):
        sim = get_cosine_sim(s, arrs[i])[0][1]
        if sim > max_sim:
            max_sim = sim
            max_indx = i
    print('Matching: {} seconds'.format(datetime.now() - start_time))
    return max_indx
