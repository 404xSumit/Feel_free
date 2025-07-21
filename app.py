from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from logic_test import questions, likert_score, analyze_responses
from werkzeug.security import generate_password_hash, check_password_hash
# from empathy_chatbot import FeelFreeChatbot
import re
import random
import string
from flask_mail import Mail, Message
from flask import jsonify
# import for sms
# from twilio.rest import Client
import os
from dotenv import load_dotenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

#load .env variables
load_dotenv()   


# # Twilio credentials from .env
# TWILIO_SID = os.getenv("TWILIO_SID")
# TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
# TWILIO_PHONE = os.getenv("TWILIO_PHONE")

# ADMIN_PHONE = os.getenv("ADMIN_PHONE") 
# client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
#sms ka code yaha tak tha
#yaha se om ka code start
from my_api import API_KEY, genai
import nltk
from nltk.stem import PorterStemmer
# Download NLTK data (only needed once)
# nltk.download('punkt')
app = Flask(__name__,template_folder = ".")

stemmer = PorterStemmer()
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
mental_health_keywords = [
      "anxiety", "depression", "stress", "therapy", "mental health", "counseling",
    "panic", "sleep", "sad", "unmotivated", "lonely", "anger", "wellbeing", "self-esteem",
    "motivation", "overwhelmed", "confidence", "burnout", "self care", "mood", "trauma",
    "grief", "personal health", "feel", "emotions", "support", "talk", "mental", "how to cope",
    "frustrated", "cry", "depressed", "anxious", "alone", "suicide", "loser", "embarrasing",
    "scold", "fight", "relative", "passed", "kill", "die", "fuck", "god", "evil", "yeah",
    "please", "solve", "love", "hate", "cheat", "Hi", "hey", "hello",

    # Extended keywords
    "bipolar", "OCD", "PTSD", "ADHD", "phobia", "addiction", "withdrawal", "intrusive thoughts",
    "hallucination", "delusion", "psychosis", "disorder", "episode", "relapse", "numb", "hopeless",
    "helpless", "worthless", "empty", "broken", "insecure", "shattered", "disconnected",
    "irritable", "restless",

    # Common expressions
    "I can't take it anymore", "I want to disappear", "I feel numb", "I hate myself", "I need help",
    "I don't matter", "why me", "no one understands", "life is hard", "I'm not okay", "it hurts",
    "please help", "am I normal", "I'm tired", "everything is dark", "my mind won't stop",

    # Relationship/trigger words
    "breakup", "heartbroken", "cheated", "abandoned", "trust", "divorce", "rejection", "bullied",
    "abuse", "violence", "toxic", "neglected", "scream", "yelled", "ignored",

    # Behaviors and habits
    "overthinking", "procrastination", "self-harm", "cut", "binge", "purge", "isolate", "insomnia",
    "nightmare", "overeat", "can't focus", "avoid", "skip", "lash out",

    # Emotions
    "scared", "nervous", "uneasy", "miserable", "exhausted", "defeated", "ashamed", "regret",
    "guilt", "sorrow", "confused",

    # Positive/help-seeking
    "healing", "safe space", "vent", "journaling", "mindfulness", "meditation", "calm", "breathe",
    "talk to someone", "mental peace", "positivity", "recovery", "let go", "happiness",
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
        return any(stemmed_word in stemmed_input for stemmed_word in stemmed_keywords) # checks whether any word in stemmed_input is in stemmed_keywords

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


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'evoljonny'
app.config['MYSQL_DB'] = 'chatbot_db'

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False  #ye false hona chahiye
app.config['MAIL_USERNAME'] = 'feelfree.team4u@gmail.com'         # Replace with your Gmail
app.config['MAIL_PASSWORD'] = 'wnvh yczi ccik lkxw'            # Replace with App Password (not Gmail password)
app.config['MAIL_DEFAULT_SENDER'] = 'feelfree.team4u@gmail.com'

mail = Mail(app)
mysql = MySQL(app)


def create_tables():
    cur = mysql.connection.cursor()

    # Create users table
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        age INT,
        phone VARCHAR(15),
        email VARCHAR(100) UNIQUE,
        password VARCHAR(255)
    )''')

    # Create emergency_contacts table
    cur.execute('''CREATE TABLE IF NOT EXISTS emergency_contacts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        contact_name VARCHAR(100),
        contact_phone VARCHAR(15),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')

    # Create conversations table
    cur.execute('''CREATE TABLE IF NOT EXISTS conversations (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        message TEXT,
        sender ENUM('user', 'bot'),
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')

    mysql.connection.commit()
    cur.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gratitudejournal', methods=['GET', 'POST'])
def gratitudejournal():
    return render_template('gratitudejournal.html')
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        #getting the form data
        name = request.form['name']
        age = request.form['age']
        phone = request.form['phone']
        email = request.form['email']

        #hashing the password
        password = generate_password_hash(request.form['password'])
        
        #getting contacts from form
        contact1_name=request.form['contact1_name']
        contact1_phone=request.form['contact1_phone']
        contact2_name=request.form['contact2_name']
        contact2_phone=request.form['contact2_phone']
        contact3_name=request.form['contact3_name']
        contact3_phone=request.form['contact3_phone']
        
        #creating a list of contacts as tuples so that it can be iterated and inserted in the database
        contacts = [
            (contact1_name, contact1_phone),
            (contact2_name, contact2_phone),
            (contact3_name, contact3_phone)
        ]

        #database insertion
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, age, phone, email, password) VALUES (%s, %s, %s, %s, %s)",
                    (name, age, phone, email, password))
        mysql.connection.commit()
        user_id = cur.lastrowid

        for contact in contacts:
            cur.execute("INSERT INTO emergency_contacts (user_id, contact_name, contact_phone) VALUES (%s, %s, %s)",
                        (user_id, contact[0], contact[1]))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('consent'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password_input = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT id, password FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[1], password_input):
            session['user_id'] = user[0]
            session.pop('guest', None)
            session.pop('guest_id', None)
            session.pop('free_prompts', None)
            session.pop('danger_count', None)
            session.pop('danger_flagged', None)

            # Migrate guest conversation if needed
            if 'guest_id' in session:
                guest_id = session['guest_id']
                cur = mysql.connection.cursor()
                cur.execute("UPDATE conversations SET user_id = %s WHERE user_id = %s", (user[0], guest_id))
                mysql.connection.commit()
                cur.close()

            return redirect(url_for('afterlogin'))
        else:
            return "Invalid credentials"
    return render_template('login.html')


@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        #fetching email
        email = request.form.get('email')
        #storing email in session (session will be a dictionary with reset_email as key) 
        session['reset_email'] = email

        #if email is valid (True), then generating otp and storing it in session 
        if email:
            otp = ''.join(random.choices(string.digits, k=6))
            session['otp'] = otp

            try:
                #sending otp in email
                msg = Message(
                    subject="Your One-Time Password (OTP) for Verification",
                    sender=("Feel Free Team", "feelfree.team4u@gmail.com"),
                    recipients=[email]
                )
                msg.body = f"""
Hello,

Thank you for using Feel Free.

Your One-Time Password (OTP) for password reset is: {otp}

Please enter this OTP in the website to continue. Do not share it with anyone.

This is an automated message. If you did not request this, please ignore it.

Best regards,  
Feel Free Support Team
"""
                mail.send(msg)
                print(f"OTP sent to {email}: {otp}")
                return redirect(url_for('verify_otp'))

            except Exception as e:
                print("Error sending email:", str(e))
                return "Failed to send OTP email. Please check your internet and email configuration."

        else:
            return "Please provide a valid email address."

    return render_template('forgot.html')


@app.route('/verify', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        otp_input = request.form['otp']

        # Initialize attempt counter if not present
        if 'otp_attempts' not in session:
            session['otp_attempts'] = 0

        # Compare OTP
        if otp_input == session.get('otp'):
            session.pop('otp_attempts', None)  # Reset counter on success
            return redirect(url_for('reset_password'))
        else:
            session['otp_attempts'] += 1

            if session['otp_attempts'] >= 5:
                session.pop('otp_attempts', None)  # Reset counter
                return render_template('forgot.html')  #redirect karega forgot me 

            #invalid_otp.html page me jo meta likhe he head section me uske karan 4 second baad yaha redirect ho jayega
            return render_template('invalid_otp.html') 

    return render_template('verify.html')

@app.route('/reset', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        new_password = generate_password_hash(request.form['password'])
        email = session.get('reset_email')
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET password = %s WHERE email = %s", (new_password, email))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('login'))
    return render_template('resetPassword.html')

exit_commands = ["exit", "quit", "bye", "goodbye"]

# first response check hoga
first_response_flag = {"first": True}

def is_mental_health_related(text): # speciall for first response
    keywords = ['depression', 'anxiety', 'stress', 'sad', 'mental', 'lonely']
    return any(kw in text for kw in keywords)
def empathetic_response(user_input, is_first):
    if is_first:
        return "I'm here to listen. You're not alone. Tell me more about what you're feeling."
    return "That sounds tough. I'm here for you. Please share more if you're comfortable."

@app.route('/afterlogin', methods=["GET", "POST"]) 
def afterlogin():
    return render_template('AfterLogin.html')

@app.route('/consent', methods=['GET', 'POST'])
def consent():
    if request.method == 'POST':
        consent = request.form['consent']
        if consent == 'yes':
            print('yes mila')
            session['consent'] = True
            print('session me store hogya, consent', session['consent'])
            return redirect(url_for('login'))
        else:
            session['consent'] = False
            return redirect(url_for('login'))

    return render_template('consent.html')
    
@app.route("/maybe", methods=["GET", "POST"])
def check_maybe():
    if request.method == "POST":
        choice = request.form.get("choice")
        if choice not in likert_score:
            return redirect(url_for("index"))
        
        session['responses'].append(likert_score[choice])
        session['q_index'] += 1
        if session['q_index'] >= len(questions):

            conclusion = analyze_responses(session['responses'])
            return render_template("probable.html", done=True, conclusion=conclusion)

    else:
        session['q_index'] = 0
        session['responses'] = []

    q_num = session['q_index']
    current_q = questions[q_num]['q']
    return render_template("probable.html", question=current_q, q_num=q_num + 1, total=len(questions))

@app.route('/chat', methods=["GET", "POST"]) 
def chatbot_page():
    if request.method == 'GET':
        return render_template('chatbox.html')

    # === Guest Session Initialization ===
    if 'user_id' not in session and 'guest_id' not in session:
        session['guest'] = True
        session['guest_id'] = random.randint(100000, 999999)
        session['free_prompts'] = 5
        session['danger_count'] = 0
        print(" Guest Session Initialized:", session['guest_id'], "Free Prompts:", session['free_prompts'])

    user_id = session['guest_id'] if session.get('guest') else session.get('user_id')
    print(" Current user_id:", user_id)

    # === Input Parsing ===
    user_input = ""
    if request.is_json:
        user_input = request.json.get('message', '').strip().lower()
    else:
        user_input = request.form.get('user_input', '').strip().lower()

    if not user_input:
        return jsonify({'response': "Please enter a message.", 'should_exit': False})

    # === Exit Command Check ===
    if user_input in exit_commands:
        return jsonify({'response': "Goodbye! Take care of yourself.", 'should_exit': True})

    # === Free Prompt Limiting (Only for Guests) ===
    if session.get('guest', False):
        print("👤 Guest Detected - Free Prompts Left:", session['free_prompts'])
        if session['free_prompts'] <= 0:
            print("Guest prompt limit reached.")
            return jsonify({
                'response': "You've used all your free prompts. Please sign up or log in to continue chatting.",
                'should_exit': True
            })
        session['free_prompts'] -= 1  # Decrease prompt count
        print(" Guest Prompt Count Decreased:", session['free_prompts'])

    # === Generate Chatbot Response ===
    if is_mental_health_related(user_input):
        response = empathetic_response(user_input, first_response_flag["first"])
        first_response_flag["first"] = False
        should_exit = False
    else:
        response_data = chatbot.get_response(user_input)
        response = response_data[0]
        should_exit = response_data[1]

    # === Emergency Phrase Detection (Same for Guests and Users) ===
    print('session bellow')
    print(session)
    danger_keywords = r"\b(suicide|kill myself|harm myself|self-harm|die|death|overdose|poison)\b"
    if re.search(danger_keywords, user_input, re.IGNORECASE):
        print(" Danger Keyword Detected in Input")
        session['danger_count'] = session.get('danger_count', 0) + 1
        print(" Danger Count:", session['danger_count'])

        if session['danger_count'] >= 5:
            print(" Threshold Reached. Initiating Alert")
            with app.app_context():
                user_identity = "Unknown"
                if not session.get("guest"):  # Registered user
                    user_id=session.get('user_id')
                    print('user id mil gayi, ', user_id)
                    cur = mysql.connection.cursor()
                    cur.execute("SELECT name, email, phone FROM users WHERE id = %s", (user_id,))
                    user = cur.fetchone()
                    cur.close()
                    user_name = session.get("name", "Unknown")
                    user_email = session.get("email", "Unknown")
                    user_identity = f"Registered User Alert\nName: {user[0]}\nEmail: {user[1]}\nContact: {user[2]}"
                else:
                    user_identity = f"Guest User ID: {user_id}"

                print(" Sending Alert For:", user_identity)

                try:
                    # Check for consent
                    if session.get("consent", True):
                        # Send SMS (for registered users)
                        sms_body = (
                            " Emergency Alert \n"
                            f"Hey I think your friend is feeling very low recently, we recommend you to call or meet them ASAP.\n"
                            f"User: {user_identity}\n"
                            f"Message: {user_input}"
                        )
                        message = client.messages.create(
                            body=sms_body,
                            from_=TWILIO_PHONE,
                            to=ADMIN_PHONE
                        )
                        print(f"SMS sent (SID: {message.sid})")
                    else:
                        # Send Email (when consent is False)
                        msg = Message(
                            subject="Emergency Alert: Suicidal Intent Detected (5 Mentions)",
                            sender="feelfree.team4u@gmail.com",
                            recipients=["sumit942538@gmail.com"],
                            body=(
                                f"Dear Team,\n\n"
                                f"The following user has been flagged for potentially harmful content:\n\n"
                                f"User Identity: {user_identity}\n"
                                f"Number of flagged instances: 5\n\n"
                                f"Most recent message:\n"
                                f"{user_input}\n\n"
                                f"Please review the user's activity and take any necessary action.\n\n"
                                f"Regards,\n"
                                f"Your Automated Monitoring System"
                            )
                        )
                        mail.send(msg)
                        print("Email sent successfully.")
                except Exception as e:
                    print("Error sending alert:", e)
                finally:
                    session.clear()

    return jsonify({'response': response, 'should_exit': should_exit})

        
def chatbot_page():
    """
    This endpoint is responsible for rendering the chat interface and
    storing the conversation in the database. It handles both GET and
    POST requests.

    If the user is not logged in (i.e., 'user_id' is not in the session),
    it sets up a guest session with a random guest ID and 5 free prompts.
    If the user is logged in, it uses their user ID.

    When a POST request is received, it checks if the user has used up all
    their free prompts. If so, it redirects them to the prompt limit page.
    Otherwise, it stores the conversation in the database and returns the
    response from the chatbot.

    If the user types something that matches the emergency regex, it
    sends an alert to the emergency contacts stored in the database.
    """
    cur = mysql.connection.cursor()

    if 'user_id' not in session:
        # Set up a guest session
        if 'guest_id' not in session:
            session['guest'] = True
            session['guest_id'] = random.randint(100000, 999999)
            session['free_prompts'] = 5
        user_id = session['guest_id']
    else:
        # Use the user's ID
        session['guest'] = False
        user_id = session['user_id']

    if request.method == 'POST':
        # Get user input from form
        user_input = request.form['user_input']

        # Check if the guest user has free prompts left
        if session.get('guest') and session['free_prompts'] <= 0:
            return jsonify({'response': "You've used all your free prompts.", 'should_exit': True})

        # Decrease prompt count for guests
        if session.get('guest'):
            session['free_prompts'] -= 1

        # Get chatbot response
        response_data = chatbot.get_response(user_input)
        response = response_data[0]
        should_exit = response_data[1]

        # Save chat to database
        cur.execute("INSERT INTO conversations (user_id, message, sender) VALUES (%s, %s, 'user')", (user_id, user_input))
        cur.execute("INSERT INTO conversations (user_id, message, sender) VALUES (%s, %s, 'bot')", (user_id, response))
        mysql.connection.commit()

        # Check for emergency signals
        if re.search(r"suicide|kill myself", user_input, re.IGNORECASE):
            cur.execute("SELECT contact_phone FROM emergency_contacts WHERE user_id = %s", (user_id,))
            contacts = cur.fetchall()
            for c in contacts:
                print(f"⚠️ ALERT SENT TO: {c[0]}")  # Placeholder for SMS or email logic

        # Return chatbot response as JSON
        return jsonify({'response': response, 'should_exit': should_exit})

    # Render chat interface on GET
    return render_template('chatbox.html')



@app.route('/api/chat', methods=['POST'])
def chat():
    if 'first_response' not in session:
        session['first_response'] = True

    user_input = request.json.get('message', '').strip()
    is_first = session['first_response']

    response_data = chatbot.get_response(user_input, is_first)

    # Mark first response as done
    session['first_response'] = False

    return jsonify(response_data)

@app.route('/prompt-limit')
def prompt_limit():
    return "You have used all free prompts. Please sign up or log in to continue."

if __name__ == '__main__':
    with app.app_context():
        create_tables()
    app.run(debug=True)

