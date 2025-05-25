from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import mysql.connector
import bcrypt
import os
from dotenv import load_dotenv
from twilio.rest import Client

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback_secret_key")

# Twilio Configuration
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="01052004",
            database="sos_system"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return None

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()  # Ensures JSON is parsed correctly
        if not data:
            return jsonify({"error": "Invalid request data"}), 400

        name = data.get("name")
        phone = data.get("phone")
        email = data.get("email")
        password = data.get("password")

        if not all([name, phone, email, password]):
            return jsonify({"error": "All fields are required!"}), 400

        password_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO volunteers (name, phone, email, password) VALUES (%s, %s, %s, %s)",
                           (name, phone, email, password_hashed))
            conn.commit()
            conn.close()

            return jsonify({"message": "Registration successful!"})
        else:
            return jsonify({"error": "Database connection failed"}), 500

    return render_template("signup.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()  # Ensures JSON parsing
        if not data:
            return jsonify({"error": "Invalid request data"}), 400

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Both email and password are required!"}), 400

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, password FROM volunteers WHERE email = %s", (email,))
            user = cursor.fetchone()
            conn.close()

            if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
                session["user_id"] = user[0]
                return jsonify({"message": "Login successful!"})
            else:
                return jsonify({"error": "Invalid credentials!"}), 401
        else:
            return jsonify({"error": "Database connection failed"}), 500

    return render_template("login.html")

@app.route('/volunteers')
def volunteers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT name, phone, email FROM volunteers")
    volunteers = cursor.fetchall()
    conn.close()
    return render_template("volunteers.html", volunteers=volunteers)

@app.route('/send_sos', methods=['POST'])
def send_sos():
    try:
        data = request.json
        latitude, longitude = data["latitude"], data["longitude"]
        message = f"SOS Alert! Urgent Help Needed. Location: https://maps.google.com/?q={latitude},{longitude}"

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT phone FROM volunteers")
            volunteers = cursor.fetchall()
            conn.close()
        else:
            return jsonify({"error": "Database connection failed"}), 500

        # Send SMS using Twilio 
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        for volunteer in volunteers:
            client.messages.create(
                body=message,
                from_=TWILIO_PHONE_NUMBER,
                to=volunteer[0]
            )

        return jsonify({"success": True, "message": "SOS messages sent!"})

    except Exception as e:
        print(f"Error: {str(e)}")  # Debugging output
        return jsonify({"error": f"Server error: {str(e)}"}), 500  # Ensure JSON response

@app.route('/logout')
def logout():
    session.pop("user_id", None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)