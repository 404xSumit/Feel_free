from flask import Flask, request, jsonify, render_template
from my_api import API_KEY, genai
import nltk
from nltk.stem import PorterStemmer

# nltk.download('punkt')# only needed once

stemmer = PorterStemmer()
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
app = Flask(__name__)
mental_health_keywords = [
    "anxiety", "depression", "stress", "therapy", "mental health", "counseling","panic", "sleep", "sad", "unmotivated", "lonely", "anger","wellbeing","self-esteem", "motivation", "overwhelmed", "confidence", "burnout","self care", "mood", "trauma", "grief", "personal health", "feel", "emotions","support", "talk", "mental", "how to cope", "frustrated", "cry", "depressed", "anxious", "lonely", "alone", "unmotivated", "burnout", "suicide", "loser","embarrasing", "scold", "fight", "relative", "passed","kill", "die",'fuck','god','evil','yeah','please','solve'
]
stemmed_keywords = [stemmer.stem(word.lower()) for word in mental_health_keywords]
exit_commands = ["bye", "thank you", "ok", "thanks"]
first_response_flag = {"first": True}
@app.route('/')
def index():
    return render_template('chatbox.html')

@app.route('/chat', methods=["POST"])
def chat():
    user_input = request.json.get('message', '').strip().lower()
    if user_input in exit_commands:
        return jsonify({'response': "Goodbye! Take care of yourself."})
    if is_mental_health_related(user_input):
        response = empathetic_response(user_input, first_response_flag["first"])
        first_response_flag["first"] = False
        return jsonify({'response': response})
    else:
        return jsonify({'response': "Sorry, I am here to have conversations related to your personal wellbeing only."})

def is_mental_health_related(text):
    text = text.lower()
    words = nltk.word_tokenize(text)
    stemmed_input = [stemmer.stem(word) for word in words]
    return any(word in stemmed_keywords for word in stemmed_input)

def empathetic_response(text, is_first_response):
    if "sad" in text:
        return "I'm so sorry you're feeling sad. It must be really tough right now..." if is_first_response else "I'm here for you. I understand that feeling sad can be overwhelming..."
    elif "anxious" in text:
        return "It sounds like you're feeling really anxious..." if is_first_response else "I can imagine how overwhelming anxiety can be..."
    elif "depressed" in text:
        return "I'm really sorry you're feeling this way..." if is_first_response else "Depression can be really tough, but you're not alone..."
    elif "lonely" in text:
        return "I'm so sorry you're feeling lonely right now..." if is_first_response else "Loneliness can be so hard, but you're not truly alone..."
    elif "burnout" in text:
        return "Burnout can leave you feeling drained and overwhelmed..." if is_first_response else "I understand that burnout can be overwhelming..."
    else:
        return model.generate_content(text).text
if __name__ == '__main__':
    app.run(debug=True)
