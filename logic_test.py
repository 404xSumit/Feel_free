# logic_test.py

questions = [
    {"q": "I often feel sad or hopeless.", "tag": "depression"},
    {"q": "I frequently feel anxious, worried, or tense.", "tag": "anxiety"},
    {"q": "I have trouble sleeping or concentrating.", "tag": "anxiety"},
    {"q": "I no longer enjoy things I used to.", "tag": "depression"},
    {"q": "I relive past traumatic experiences often.", "tag": "ptsd"},
    {"q": "I avoid social situations or feel isolated.", "tag": "social"},
    {"q": "Others often disappoint me when I expect something from them.", "tag": "anger issues"},
]

likert_score = {
    "Strongly Disagree": 0,
    "Disagree": 1,
    "Neutral": 2,
    "Agree": 3,
    "Strongly Agree": 4,
}


def analyze_responses(response_scores):
    tag_scores = {}

    for idx, score in enumerate(response_scores):
        tag = questions[idx]["tag"]
        tag_scores[tag] = tag_scores.get(tag, 0) + score
    flags = {tag: score for tag, score in tag_scores.items() if score >= 6}

    if not flags:
        return "Your responses do not indicate signs of a mental health disorder. Keep taking care of yourself!"
    else:
        msg = "Based on your responses, you may be experiencing:\n"
        for issue in flags:
            msg += f"- {issue.title()}\n"
        msg += "\nYour feel trial as a guest expires here, please login or create a new account to continue for better support."
        return msg
