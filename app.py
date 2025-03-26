import os
import streamlit as st
from g4f.client import Client  # Importing the chatbot client
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

# Initialize the AI client
client = Client()

# Get the SendGrid API Key from environment variables
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

# Setting page configuration
st.set_page_config(page_title="Terrakil Ping Pong Equipment", page_icon="🏓", layout="wide")

# Adding custom CSS for a more premium and high-tech aesthetic
st.markdown(
    """
    <style>
        body {
            background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
            color: #fff;
        }
        .css-1d391kg {  /* Override default sidebar styles */
            background-color: #1e293b !important;
            color: #fff;
        }
        .css-ffhzg2 {  /* Override the main content area */
            background-color: #2d3748;
            color: #fff;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.4);
        }
        .stButton>button {
            background-color: #e63946;
            color: white;
            font-weight: bold;
            border-radius: 10px;
            padding: 10px 20px;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #d62839;
            transform: scale(1.1);
        }
        .carousel-container {
            max-width: 100%;
            overflow: hidden;
            position: relative;
            border-radius: 15px;
            box-shadow: 0px 4px 10px rgba(255, 255, 255, 0.2);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar for Navigation
st.sidebar.title("🔥 Terrakil - Elevate Your Game 🔥")
st.sidebar.image("https://yourlogoimage.com/logo.png", width=200)
st.sidebar.markdown("## Navigation")
sidebar_options = ["🏠 Home", "🏓 Ping Pong Blades", "🎾 Ping Pong Rubbers", "⚡ Pre-Assembled Paddles", "🛒 Shopping Cart", "📞 Contact Us", "🤖 Chat with AI"]
selected_option = st.sidebar.radio("Select a page", sidebar_options)

# AI Chatbot Integration
if selected_option == "🤖 Chat with AI":
    st.title("Chat with Terrakil AI 🧠")
    if 'history' not in st.session_state:
        st.session_state.history = []
    for message in st.session_state.history:
        st.write(message["role"] + ": " + message["content"])
    user_message = st.text_input("You: ", "")
    if st.button("Send 📨"):
        if user_message:
            st.session_state.history.append({"role": "User", "content": user_message})
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": user_message}],
                web_search=False
            )
            ai_response = response.choices[0].message.content
            st.session_state.history.append({"role": "AI", "content": ai_response})
            st.experimental_rerun()

# Home page
if selected_option == "🏠 Home":
    st.title("🏓 Welcome to Terrakil - The Future of Ping Pong 🏓")
    st.markdown("""
    **Why settle for average when you can dominate the table?**
    At Terrakil, we provide cutting-edge ping pong gear designed for champions. 
    🚀 **Precision** | 🎯 **Speed** | 🔥 **Power**
    """)
    st.image("https://yourimage.com/hero.jpg", use_container_width=True)
    st.markdown("### 💥 Featured Products 💥")
    st.image("https://yourimage.com/product1.jpg", caption="Blade X - Maximum Power", use_container_width=True)
    st.image("https://yourimage.com/product2.jpg", caption="Rubber Z - Ultimate Spin", use_container_width=True)

# Shopping Cart Page
elif selected_option == "🛒 Shopping Cart":
    st.title("🛍️ Your Shopping Cart")
    st.write("View and manage your selected items.")
    if "cart" not in st.session_state:
        st.session_state.cart = []
    if st.session_state.cart:
        for item in st.session_state.cart:
            st.write(f"🛒 {item}")
        if st.button("Checkout 💳"):
            st.success("Thank you for your purchase!")
            st.session_state.cart = []
    else:
        st.write("Your cart is empty. Start shopping now!")

# Contact Us page
elif selected_option == "📞 Contact Us":
    st.title("📩 Get in Touch with Terrakil")
    with st.form("contact_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        message = st.text_area("Your Message")
        submit_button = st.form_submit_button("Send Message 📨")
        
    if submit_button:
        if name and email and message:
            # Compose the email
            from_email = Email("no-reply@terrakil.com")  # Your business email
            to_email = To("your-email@example.com")  # Your email address to receive messages
            subject = f"New message from {name}"
            content = Content("text/plain", f"Message from {name} ({email}):\n\n{message}")
            mail = Mail(from_email, to_email, subject, content)
            
            # Send the email
            try:
                response = sg.send(mail)
                if response.status_code == 202:
                    st.success(f"Thanks for reaching out, {name}! We will get back to you soon.")
                else:
                    st.error("Sorry, something went wrong. Please try again later.")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please fill out all fields before submitting.")
