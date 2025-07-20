from flask import Flask, render_template, request, jsonify
from my_api import API_KEY, genai
import nltk
from nltk.stem import PorterStemmer

# Download NLTK data (only needed once)
nltk.download('punkt')
app = Flask(__name__,template_folder = ".")

stemmer = PorterStemmer()
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
mental_health_keywords = [
    "anxiety", "depression", "stress", "therapy", "mental health", "counseling",
    "panic", "sleep", "sad", "unmotivated", "lonely", "anger", "wellbeing",
    "self-esteem", "motivation", "overwhelmed", "confidence", "burnout",
    "self care", "mood", "trauma", "grief", "personal health", "feel", "emotions",
    "support", "talk", "mental", "how to cope", "frustrated", "cry", "depressed", 
    "anxious", "lonely", "alone", "unmotivated", "burnout", "suicide", "loser", 
    "embarrasing", "scold", "fight", "feel", "relative", "passed", "die"
]

stemmed_keywords = [stemmer.stem(word.lower()) for word in mental_health_keywords]
exit_commands = ["bye", "thank you", "ok", "thanks"]

class ChatBot:
    def __init__(self):
        self.first_response = True

    def is_mental_health_related(self, text):
        text = text.lower()
        words = nltk.word_tokenize(text)
        stemmed_input = [stemmer.stem(word) for word in words]
        return any(stemmed_word in stemmed_input for stemmed_word in stemmed_keywords)

    def empathetic_response(self, text, is_first_response):
        text_lower = text.lower()
        if "sad" in text_lower:
            return (
                "I'm so sorry you're feeling sad. It must be really tough right now. "
                "It's okay to feel this way, and it's important to give yourself the time you need to process your emotions. "
                "Take care of yourself during this time."
            ) if is_first_response else (
                "I'm here for you. I understand that feeling sad can be overwhelming, but please remember that you're not alone."
            )
        elif "anxious" in text_lower:
            return (
                "It sounds like you're feeling really anxious, and I want you to know that your feelings are valid. "
                "It can be overwhelming when anxiety takes hold, but you're not alone in this. "
                "Remember, you're strong, and it's okay to take things one step at a time."
            ) if is_first_response else (
                "I can imagine how overwhelming anxiety can be. Take your time, and remember you're capable of managing it, step by step."
            )
        elif "depressed" in text_lower:
            return (
                "I'm really sorry you're feeling this way. Depression can feel isolating, but you're not alone. "
                "It's okay to take things one step at a time. Please be kind to yourself, and don't hesitate to reach out when you're ready."
            ) if is_first_response else (
                "Depression can be really tough, but you're not alone. Be gentle with yourself, and know that it's okay to feel this way."
            )
        elif "lonely" in text_lower:
            return (
                "I'm so sorry you're feeling lonely right now. Loneliness can be incredibly hard to bear, but it doesn't mean you're alone. "
                "I'm here with you, and I want to remind you that you are worthy of connection and care."
            ) if is_first_response else (
                "Loneliness can be so hard, but you're not truly alone. I'm here, and I'm happy to listen if you need me."
            )
        elif "burnout" in text_lower:
            return (
                "Burnout can leave you feeling drained and overwhelmed. It's okay to feel exhausted, and you don't have to carry that weight alone. "
                "Please remember that it's important to take a break and recharge. You've been working hard, and it's okay to pause."
            ) if is_first_response else (
                "I understand that burnout can be overwhelming. It's okay to step back and take time for yourself to rest and recharge."
            )
        else:
            return model.generate_content(text).text

    def get_response(self, user_input):
        user_input = user_input.strip().lower()

        if user_input in exit_commands:
            return "Goodbye! Take care of yourself.", True

        if self.is_mental_health_related(user_input):
            response = self.empathetic_response(user_input, self.first_response)
            self.first_response = False
            return response, False
        else:
            return "Sorry, I am here to have conversations related to your personal wellbeing only.", False

chatbot = ChatBot()
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    response, should_exit = chatbot.get_response(user_input)
    return jsonify({'response': response, 'should_exit': should_exit})

if __name__ == '__main__':
    app.run(debug=True)