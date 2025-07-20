from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import re
import random
import string
from flask_mail import Mail, Message
from flask import jsonify

# Try to import the actual chatbot, fall back to our implementation if it fails
try:
    from empathy_chatbot import FeelFreeChatbot
    print("Successfully imported the original FeelFreeChatbot")
except ImportError:
    print("Could not import original FeelFreeChatbot, using fallback implementation")
    # Fallback implementation
    class FeelFreeChatbot:
        def get_response(self, message):
            return {
                "response": f"I received your message: '{message}'. This is a fallback response as the main chatbot might not be working correctly."
            }

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'harsh@29292929'
app.config['MYSQL_DB'] = 'chatbot_db'

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'         # Replace with your Gmail
app.config['MAIL_PASSWORD'] = 'your_app_password'            # Replace with App Password (not Gmail password)

mail = Mail(app)

mysql = MySQL(app)
chatbot = FeelFreeChatbot()

# Modify the create_tables function to add a guest user table
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

    # Create a special guest user if it doesn't exist
    cur.execute("SELECT id FROM users WHERE email = 'guest@system.local'")
    guest_user = cur.fetchone()
    if not guest_user:
        cur.execute("INSERT INTO users (name, age, phone, email, password) VALUES (%s, %s, %s, %s, %s)",
                   ("Guest User", 0, "0000000000", "guest@system.local", "guest"))
        mysql.connection.commit()
        print("Created guest user")

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

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        phone = request.form['phone']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        contacts = [
            (request.form['contact1_name'], request.form['contact1_phone']),
            (request.form['contact2_name'], request.form['contact2_phone']),
            (request.form['contact3_name'], request.form['contact3_phone'])
        ]

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

        return redirect(url_for('login'))
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

            # If guest conversation exists, transfer it to user
            if 'guest_id' in session:
                guest_id = session['guest_id']
                cur = mysql.connection.cursor()
                cur.execute("UPDATE conversations SET user_id = %s WHERE user_id = %s", (user[0], guest_id))
                mysql.connection.commit()
                cur.close()

            return redirect(url_for('chatbot_page'))
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        email = request.form['email']
        session['reset_email'] = email
        otp = ''.join(random.choices(string.digits, k=6))
        session['otp'] = otp
        
        # Send OTP via Flask-Mail
        try:
            msg = Message('Your OTP Code',
                          sender='your_email@gmail.com', #yaha email daalna he 
                          recipients=[email])
            msg.body = f'Your OTP for password reset is: {otp}'
            mail.send(msg)
            print("OTP sent to email:", email)
        except Exception as e:
            print("Error sending email:", e)
            return "Failed to send OTP email. Try again later."
      
        return redirect(url_for('verify_otp'))
    return render_template('forgot.html')

@app.route('/verify', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        otp_input = request.form['otp']
        if otp_input == session.get('otp'):
            return redirect(url_for('reset_password'))
        else:
            return "Invalid OTP"
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
    return render_template('reset.html')

# Also update the chatbot_page function to use the same guest user approach
@app.route('/chat', methods=['GET', 'POST'])
def chatbot_page():
    cur = mysql.connection.cursor()

    if 'user_id' not in session:
        # Get the guest user ID from the database
        cur.execute("SELECT id FROM users WHERE email = 'guest@system.local'")
        guest_user = cur.fetchone()
        if guest_user:
            user_id = guest_user[0]
            if 'guest_id' not in session:
                session['guest'] = True
                session['guest_id'] = user_id
                session['free_prompts'] = 5
        else:
            # Fallback if guest user doesn't exist
            return "System error. Please try again later."
    else:
        session['guest'] = False
        user_id = session['user_id']

    if request.method == 'POST':
        user_input = request.form['message']

        if session.get('guest') and session.get('free_prompts', 0) <= 0:
            return redirect(url_for('prompt_limit'))

        if session.get('guest') and 'free_prompts' in session:
            session['free_prompts'] -= 1

        bot_response = chatbot.get_response(user_input)

        try:
            # Store conversation whether the user is guest or logged in
            cur.execute("INSERT INTO conversations (user_id, message, sender) VALUES (%s, %s, 'user')", (user_id, user_input))
            cur.execute("INSERT INTO conversations (user_id, message, sender) VALUES (%s, %s, 'bot')", (user_id, bot_response['response']))
            mysql.connection.commit()
        except Exception as db_error:
            print(f"Database error in chatbot_page: {str(db_error)}")

        # Emergency detection
        if re.search(r"suicide|kill myself", user_input, re.IGNORECASE):
            cur.execute("SELECT contact_phone FROM emergency_contacts WHERE user_id = %s", (user_id,))
            contacts = cur.fetchall()
            for c in contacts:
                print(f"ALERT SENT TO: {c[0]}")  # Demo print

        return render_template('chatbox.html', response=bot_response['response'])

    return render_template('chatbox.html')


# Modify the api_chat function to use the guest user ID from the database
@app.route('/api/chat', methods=['POST'])
def api_chat():
    try:
        cur = mysql.connection.cursor()

        # Identify user/guest
        if 'user_id' not in session:
            # Get the guest user ID from the database
            cur.execute("SELECT id FROM users WHERE email = 'guest@system.local'")
            guest_user = cur.fetchone()
            if guest_user:
                user_id = guest_user[0]
                if 'guest_id' not in session:
                    session['guest'] = True
                    session['guest_id'] = user_id
                    session['free_prompts'] = 5
            else:
                # Fallback if guest user doesn't exist
                print("Error: Guest user not found in database")
                return jsonify({"response": "System error. Please try again later."}), 500
        else:
            session['guest'] = False
            user_id = session['user_id']

        # Get the message from the request
        data = request.json
        if not data or 'message' not in data:
            print("Error: No message in request data")
            return jsonify({"response": "No message provided"}), 400

        user_input = data.get('message')
        print(f"Received message: {user_input}")

        if session.get('guest') and session.get('free_prompts', 0) <= 0:
            return jsonify({"response": "limit_reached"})

        if session.get('guest') and 'free_prompts' in session:
            session['free_prompts'] -= 1

        # Get response from chatbot
        try:
            bot_response = chatbot.get_response(user_input)
            print(f"Bot response: {bot_response}")
            
            # Check if bot_response is a dictionary with 'response' key
            if isinstance(bot_response, dict) and 'response' in bot_response:
                response_text = bot_response['response']
            else:
                # If not, convert the response to a string
                response_text = str(bot_response)
            
            try:
                # Store conversation in database
                cur.execute("INSERT INTO conversations (user_id, message, sender) VALUES (%s, %s, 'user')", (user_id, user_input))
                cur.execute("INSERT INTO conversations (user_id, message, sender) VALUES (%s, %s, 'bot')", (user_id, response_text))
                mysql.connection.commit()
            except Exception as db_error:
                print(f"Database error: {str(db_error)}")
                # Continue even if database storage fails
                
            return jsonify({"response": response_text})
        except Exception as e:
            print(f"Error getting chatbot response: {str(e)}")
            return jsonify({"response": f"I'm sorry, I couldn't process your request at this time."}), 500

    except Exception as e:
        print(f"Unexpected error in api_chat: {str(e)}")
        return jsonify({"response": "An unexpected error occurred"}), 500

@app.route('/prompt-limit')
def prompt_limit():
    return "You have used all free prompts. Please sign up or log in to continue."

if __name__ == '__main__':
    with app.app_context():
        create_tables()
    app.run(debug=True)
