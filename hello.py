import streamlit as st
from email_validator import validate_email, EmailNotValidError
import random
import smtplib
import json
import os

# Path to the JSON file for storing user data
USER_DATA_FILE = "user_data.json"

# Function to load user data
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    return {}

# Function to save user data
def save_user_data(data):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(data, f)

# Initialize user database
user_db = load_user_data()

# Function to send OTP
def send_otp(email, otp):
    try:
      

# Replace with your email and password (Use App Passwords if needed)
        sender_email = "ka9190430@gmail.com"
        sender_password = "gswn pebh qxiq ndiv"
        receiver_email = email

        subject = "Your OTP Code"
        body = f"Your OTP for signup is: {otp}"

        message = f"Subject: {subject}\n\n{body}"

        # Connect to the SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Error sending OTP: {e}")
        return False

# App Logic
def main():
    global user_db

    # Session state for tracking signup and login
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user_email = None

    if not st.session_state.logged_in:
        # Tabs for Signup and Login
        tab = st.tabs(["Sign Up", "Login"])
        
        # SIGNUP TAB
        with tab[0]:
            st.title("Sign Up")
            email = st.text_input("Email Address", key="signup_email")
            password = st.text_input("Create Password", type="password", key="signup_password")
            otp = st.text_input("Enter OTP", type="password", key="signup_otp")
            generated_otp = None

            if st.button("Send OTP", key="send_otp"):
                try:
                    # Validate email
                    valid = validate_email(email).email
                    generated_otp = str(random.randint(100000, 999999))
                    if send_otp(valid, generated_otp):
                        st.session_state.generated_otp = generated_otp
                        st.success("OTP sent to your email!")
                except EmailNotValidError as e:
                    st.error(f"Invalid Email: {e}")

            if st.button("Sign Up", key="signup_button"):
                if otp == st.session_state.get("generated_otp"):
                    if email in user_db:
                        st.error("User already exists. Please login.")
                    else:
                        # Save user to the JSON database
                        user_db[email] = {"password": password}
                        save_user_data(user_db)  # Persist data
                        st.session_state.logged_in = True
                        st.session_state.user_email = email
                        st.success("Signup successful!")
                else:
                    st.error("Invalid OTP")

        # LOGIN TAB
        with tab[1]:
            st.title("Login")
            email = st.text_input("Email Address", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")

            if st.button("Login"):
                if email in user_db:
                    stored_password = user_db[email]["password"]
                    if stored_password == password:
                        st.session_state.logged_in = True
                        st.session_state.user_email = email
                        st.success("Logged in successfully!")
                    else:
                        st.error("Invalid email or password.")  # Password mismatch
                else:
                    st.error("Invalid email or password.")  # Email not found

    else:
        # Main Website after Login
        st.title("Welcome to Faisal Alam")
        st.subheader("A coding enthusiast dedicated to making things work!")
        st.image(
            "https://source.unsplash.com/featured/?technology,coding",
            caption="Embracing technology and coding",
            use_container_width=True,  # Updated parameter
        )

        # Show free HTML code
        st.markdown("### Here's some free HTML code:")
        html_code = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Free HTML Code</title>
        </head>
        <body>
            <h1>Welcome to Web Development</h1>
            <p>This is a simple HTML example!</p>
            <ul>
                <li>Learn HTML</li>
                <li>Learn CSS</li>
                <li>Learn JavaScript</li>
            </ul>
        </body>
        </html>
        """
        st.code(html_code, language="html")

        # Sidebar
        with st.sidebar:
            st.header("Menu")
            if st.button("Account"):
                st.info(f"Logged in as: {st.session_state.user_email}")
            if st.button("Log Out"):
                st.session_state.logged_in = False
                st.success("Logged out!")
            if st.button("About Us"):
                st.info(
                    """
                    **About Faisal Alam**  
                    - I am Faisal Alam from India, a passionate programmer and developer.  
                    - I believe in continuous learning and love to create impactful software solutions.  
                    - This demo app showcases a simple signup and login system built using Streamlit.
                    """
                )
            if st.button("Privacy Policy"):
                st.info("Your privacy is important to us.")

if __name__ == "__main__":
    main()
     
















