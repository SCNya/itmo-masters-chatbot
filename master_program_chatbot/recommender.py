import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def recommend_courses(user_background: str, courses: pd.DataFrame) -> pd.DataFrame:
    """
    Рекомендует элективные курсы на основе бэкграунда пользователя.
    """
    vectorizer = TfidfVectorizer(stop_words="english")

    course_descriptions = courses["course_name"]

    tfidf_matrix = vectorizer.fit_transform(course_descriptions)

    user_vector = vectorizer.transform([user_background])

    cosine_similarities = cosine_similarity(user_vector, tfidf_matrix).flatten()

    courses["similarity"] = cosine_similarities

    return courses.sort_values(by="similarity", ascending=False)
