# 🚨 Alertify – Emergency SOS Web App

**Alertify** is a web application designed to instantly alert nearby volunteers and emergency contacts when someone is in danger. With one tap on the SOS button, help is on the way – including SMS notifications and real-time tracking.

---

## 🔥 Features

### 🏠 Home Page
- Tagline: _"Your Safety, Our Priority"_
- Central **SOS** button
- Confirmation popup before sending help
- Sends **SMS alerts to volunteers within 5 km**
- **Live location tracking** of the victim on a map
- Two blocks:
  - **Volunteers**: Profile & real-time alerts of victims
  - **Emergency Form**: Opens a Google Form for police/ambulance notification

### 🙋‍♂️ Volunteer Dashboard
- Shows volunteer details filled during login
- Displays list of active SOS alerts from victims
- Message if everyone is safe: _"Everyone is safe."_
- Interactive map showing victims in need

### 🚨 Emergency Form
- Google Form for **police/ambulance**
- Auto-alerts emergency services when filled

### 🔐 Login / Signup
- Fields:
  - Name
  - ID verification
  - Phone number
  - Emergency contacts:
    - Name
    - Phone number
    - Relationship
- Add **multiple emergency contacts**
- All contacts get SMS + live location on SOS

### ℹ️ About Us
- Describes mission, team, and functionality

---

## 💻 Tech Stack

- **Frontend**: HTML, CSS, JavaScript, GSAP/Lottie for animations
- **Backend**: Flask
- **Database**: MySQL
- **SMS Notifications**: Twilio API
- **Live Maps**: Google Maps / Leaflet.js
- **Location Access**: Geolocation API
- **Secrets Management**: `python-dotenv`

---

## ⚙️ Setup Instructions

```bash
# Clone the repository
git clone https://github.com/yourusername/alertify.git
cd alertify

# Create virtual environment (optional)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env  # Then add your keys

# Run the app
python3 app.py

```


### 📍 Live Location & SMS Flow

1.	User clicks SOS → Confirmation popup
	- 2.	On confirmation:
	-	Get user’s current geolocation
	-	Send SMS with message + location to:
	-	Volunteers in 5 km radius
	-	All emergency contacts
	-	Show real-time tracking on map to volunteers
