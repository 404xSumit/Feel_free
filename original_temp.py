from my_api import API_KEY, genai
import nltk
from nltk.stem import PorterStemmer
# nltk.download('punkt_tab') 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize the NLTK stemmer
# nltk.download('punkt')  
stemmer = PorterStemmer()

mental_health_keywords = [
    "anxiety", "depression", "stress", "therapy", "mental health", "counseling",
    "panic", "sleep", "sad", "unmotivated", "lonely", "anger", "wellbeing",
    "self-esteem", "motivation", "overwhelmed", "confidence", "burnout",
    "self care", "mood", "trauma", "grief", "personal health", "feel", "emotions",
    "support", "talk", "mental", "how to cope","frustrated", "cry", "depressed", "anxious", "lonely", "alone", "unmotivated", "burnout",'sucide','suicide attempt','looser'
]

stemmed_keywords = [stemmer.stem(word.lower()) for word in mental_health_keywords]

exit_commands = ["bye", "thank you", "ok", "thanks"]

def is_mental_health_related(text):
    text = text.lower()
    # Tokenize and stem the user input
    words = nltk.word_tokenize(text)
    stemmed_input = [stemmer.stem(word) for word in words]
    return any(stemmed_word in stemmed_input for stemmed_word in stemmed_keywords)

print("Hi, I'm Jarvis. I'm here to support your personal wellbeing. Type 'bye', 'thank you', or 'ok' to exit.\n")
while True:
    user_input = input("You: ").strip().lower()

    if user_input in exit_commands:
        print("Jarvis: Goodbye! Take care of yourself.")
        break

    if is_mental_health_related(user_input):
        response = model.generate_content(user_input)
        print("Jarvis:", response.text)
    else:
        print("Jarvis: Sorry, I am here to have conversations related to your personal wellbeing only.")