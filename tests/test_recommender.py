import pandas as pd

from master_program_chatbot.recommender import recommend_courses


def test_recommend_courses():
    user_background = "I have a background in machine learning and deep learning."

    data = {
        "course_name": [
            "Introduction to AI",
            "Machine Learning",
            "Deep Learning",
            "AI Product Management",
            "Data-driven Decision Making",
            "UX for AI",
        ],
        "course_type": [
            "mandatory",
            "mandatory",
            "elective",
            "mandatory",
            "mandatory",
            "elective",
        ],
        "credits": [3, 4, 4, 3, 4, 4],
    }
    courses = pd.DataFrame(data)

    recommendations = recommend_courses(user_background, courses)

    assert isinstance(recommendations, pd.DataFrame)
    assert not recommendations.empty

    assert "similarity" in recommendations.columns

    assert recommendations.iloc[0]["course_name"] == "Machine Learning"
    assert recommendations.iloc[1]["course_name"] == "Deep Learning"

    assert recommendations["similarity"].between(0, 1).all()
