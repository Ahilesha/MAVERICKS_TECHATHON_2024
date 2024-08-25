from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import random
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a real secret key

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Sample user data (in a real app, this would come from a database)
users = {}
user_passwords = {}
password_reset_tokens = {}

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(user_id):
    return User(user_id) if user_id in users else None

# Sample suggestion data
def get_suggestions(mood):
    mood = mood.lower()
    suggestions = {
        # Example for some moods, add others as needed
        "fear": {
            "text": "😨 **Face Your Fear**",
            "details": "🌟 Acknowledge what scares you and try to face it in a controlled and safe manner. Breaking it down into manageable steps can help.",
            "action": "📝 Write down your fears and create a plan to tackle them step by step."
        },
        "sadness": {
            "text": "💔 **Allow Yourself to Feel**",
            "details": "🌧️ It's okay to feel sad. Allow yourself to express your emotions and seek comfort from loved ones.",
            "action": "📞 Reach out to a friend or family member to talk about how you're feeling."
        },
        "anger": {
            "text": "🔥 **Channel Your Anger**",
            "details": "💥 Physical activity can help release built-up anger. Try exercises or activities that allow you to let off steam.",
            "action": "🏃‍♂️ Engage in a workout, or try a stress-relief activity like hitting a punching bag."
        },
        "happiness": {
            "text": "😊 **Celebrate Your Joy**",
            "details": "🎉 Embrace your positive feelings and share them with others. Do something that makes you even happier.",
            "action": "🎂 Treat yourself to something special or plan a fun activity with friends."
        },
        "disgust": {
            "text": "🤢 **Reflect on the Source**",
            "details": "🧐 Understand what triggers your feelings of disgust and consider why it affects you this way. It might help to address the source directly.",
            "action": "🔍 Examine the situation and explore ways to minimize or avoid the cause of disgust."
        },
        "surprise": {
            "text": "😲 **Embrace the Unexpected**",
            "details": "🎈 Surprise can be exciting! Take a moment to enjoy the unexpected and explore the new possibilities it presents.",
            "action": "🎁 Use this surprise as an opportunity to try something new or appreciate a different perspective."
        },
        "anxiety": {
            "text": "🌪️ **Practice Grounding Techniques**",
            "details": "🌿 Ground yourself by focusing on the present moment. Try deep breathing, mindfulness, or progressive muscle relaxation.",
            "action": "📱 Use a grounding app or mindfulness exercise to help calm your nerves."
        },
        "joy": {
            "text": "🎉 **Savor Your Joy**",
            "details": "😊 Celebrate moments of joy and share them with others. Engaging in activities that bring you pleasure can enhance this feeling.",
            "action": "🧁 Indulge in a favorite hobby or spend quality time with loved ones."
        },
        "love": {
            "text": "❤️ **Nurture Your Relationships**",
            "details": "🌹 Love is about connection. Spend time with loved ones and show appreciation for them. It's also important to practice self-love.",
            "action": "💌 Write a heartfelt note or plan a special activity for someone you care about."
        },
        "amusement": {
            "text": "😂 **Enjoy the Moment**",
            "details": "🎭 Embrace activities that make you laugh and feel light-hearted. Amusement can be a great way to relieve stress.",
            "action": "🎬 Watch a comedy, read a funny book, or engage in a playful activity."
        },
        "anticipation": {
            "text": "⏳ **Channel Your Excitement**",
            "details": "🌟 Anticipation can be motivating. Use this time to prepare and plan for what you’re looking forward to.",
            "action": "📅 Make a checklist or plan activities related to your upcoming event."
        },
        "calmness": {
            "text": "🌿 **Maintain Your Serenity**",
            "details": "🧘‍♀️ Enjoy the peaceful state you’re in. Engage in relaxing activities to maintain your calmness.",
            "action": "🛀 Take a bath, meditate, or read a book to sustain your tranquility."
        },
        "shame": {
            "text": "😔 **Address Your Feelings**",
            "details": "🕊️ Shame can be tough to deal with. It’s important to understand the root of these feelings and practice self-compassion.",
            "action": "📖 Seek therapy or talk to a trusted person about your feelings to work through them."
        },
        "boredom": {
            "text": "😴 **Find New Activities**",
            "details": "🌈 Boredom can be a chance to discover new interests. Try something different or revisit an old hobby.",
            "action": "🎨 Pick up a new hobby, explore a new genre of books, or take an online course."
        },
        "contempt": {
            "text": "😒 **Reflect on Your Feelings**",
            "details": "🌟 Contempt often comes from dissatisfaction. Reflect on the source of these feelings and try to address them constructively.",
            "action": "🗣️ Consider discussing your feelings with someone you trust or finding ways to address the issue directly."
        },
        "empathy": {
            "text": "💖 **Connect with Others**",
            "details": "🤝 Use your understanding of others' feelings to build deeper connections and support those around you.",
            "action": "💬 Offer a listening ear or help someone who might be in need of support."
        },
        "envy": {
            "text": "🌱 **Cultivate Gratitude**",
            "details": "📝 Focus on what you have and appreciate your own strengths. Practice gratitude to shift focus from envy.",
            "action": "📒 Keep a gratitude journal or make a list of things you appreciate about yourself."
        },
        "kindness": {
            "text": "🌼 **Spread Kindness**",
            "details": "🤗 Acts of kindness can enhance your mood and create positive interactions with others.",
            "action": "💌 Do something kind for someone today, whether it’s a small gesture or a thoughtful note."
        },
        "pride": {
            "text": "🏆 **Celebrate Your Achievements**",
            "details": "🎉 Take time to acknowledge your accomplishments and feel proud of your efforts.",
            "action": "🎊 Share your achievements with others or reward yourself for your hard work."
        },
        "amazement": {
            "text": "🌟 **Savor the Wonder**",
            "details": "✨ Embrace moments of amazement and wonder. They can inspire you and bring joy to your life.",
            "action": "🌌 Reflect on what amazed you and explore more about it or share it with someone."
        },
        "annoyed": {
            "text": "😠 **Manage Your Irritation**",
            "details": "🔄 Annoyance can be managed by addressing the source of irritation or finding ways to cope.",
            "action": "🛠️ Identify what’s causing the annoyance and find constructive ways to address it or distract yourself."
        },
        "contentment": {
            "text": "😊 **Enjoy Your Satisfaction**",
            "details": "🌺 Contentment is a sign of peace. Enjoy this feeling and appreciate the current state of your life.",
            "action": "🧘‍♂️ Engage in activities that enhance your well-being and reinforce this positive feeling."
        },
        "doubt": {
            "text": "🤔 **Clarify Your Uncertainty**",
            "details": "🔍 Doubt can be unsettling. Seek information or advice to address uncertainties and make informed decisions.",
            "action": "📝 Write down your doubts and work through them, or consult a mentor or advisor."
        },
        "stress": {
            "text": "😫 **Manage Your Stress**",
            "details": "🛀 Stress can be overwhelming. Engage in activities that help you relax and manage your stress levels effectively.",
            "action": "🧘‍♂️ Try mindfulness exercises, deep breathing, or a relaxing hobby to alleviate stress."
        },
        "overwhelmed": {
            "text": "🌊 **Break Tasks into Smaller Steps**",
            "details": "🔍 Feeling overwhelmed can be eased by breaking tasks into smaller, more manageable steps. Prioritize and tackle one thing at a time.",
            "action": "📝 Create a to-do list and focus on completing one task at a time."
        },
        "depressed": {
            "text": "💭 **Seek Professional Help**",
            "details": "🌈 Depression is a serious condition. It’s important to reach out to a mental health professional for support and guidance.",
            "action": "📞 Contact a mental health professional or counselor to discuss your feelings and explore treatment options."
        },
        "down": {
            "text": "💔 **Engage in Uplifting Activities**",
            "details": "🌟 When feeling down, engage in activities that lift your spirits. Surround yourself with positive influences and support.",
            "action": "🎶 Listen to uplifting music or participate in activities that bring you joy."
        },
        "jealous": {
            "text": "😒 **Focus on Self-Improvement**",
            "details": "🌱 Jealousy often stems from personal insecurities. Use this feeling as motivation for self-improvement and growth.",
            "action": "📝 Set personal goals and work towards them, focusing on your own achievements."
        },
        "nostalgic": {
            "text": "🌟 **Cherish Fond Memories**",
            "details": "📜 Nostalgia can be comforting. Reflect on positive past experiences and use them as a source of motivation and warmth.",
            "action": "📷 Look through old photos or revisit places that hold special memories for you."
        },
        "sad": {
            "text": "🌟 **Inspirational Quote**",
            "details": "💬 Here's a motivational quote to lift your spirits: 'The only way to do great work is to love what you do.' - Steve Jobs. Reflect on your passions and what brings you joy.",
            "action": "🎨 Consider engaging in a hobby or activity that makes you happy and reconnects you with your interests."
        },
        "happy": {
            "text": "😊 **Celebrate Your Joy**",
            "details": "🎉 You're feeling great! Embrace your happiness and share it with others. Celebrate by doing something you love or spending time with friends and family.",
            "action": "🎂 Consider throwing a small get-together or treat yourself to something special. Keep spreading positivity!"
        },
	"stressed": {
            "text": "💔 **Allow Yourself to Feel**",
            "details": "🌧️ It's okay to feel sad. Allow yourself to express your emotions and seek comfort from loved ones.",
            "action": "📞 Reach out to a friend or family member to talk about how you're feeling."
        },
	"anxious": {
            "text": "🌪️ **Practice Grounding Techniques**",
            "details": "🌿 Ground yourself by focusing on the present moment. Try deep breathing, mindfulness, or progressive muscle relaxation.",
            "action": "📱 Use a grounding app or mindfulness exercise to help calm your nerves."
        },
	"jealousy": {
            "text": "😒 **Focus on Self-Improvement**",
            "details": "🌱 Jealousy often stems from personal insecurities. Use this feeling as motivation for self-improvement and growth.",
            "action": "📝 Set personal goals and work towards them, focusing on your own achievements."
        },
	"doubtful": {
            "text": "🤔 **Clarify Your Uncertainty**",
            "details": "🔍 Doubt can be unsettling. Seek information or advice to address uncertainties and make informed decisions.",
            "action": "📝 Write down your doubts and work through them, or consult a mentor or advisor."
        },
	"proud": {
            "text": "🏆 **Celebrate Your Achievements**",
            "details": "🎉 Take time to acknowledge your accomplishments and feel proud of your efforts.",
            "action": "🎊 Share your achievements with others or reward yourself for your hard work."
        },
	"amused": {
            "text": "🌟 **Savor the Wonder**",
            "details": "✨ Embrace moments of amazement and wonder. They can inspire you and bring joy to your life.",
            "action": "🌌 Reflect on what amazed you and explore more about it or share it with someone."
        },
	"angry": {
            "text": "🔥 **Channel Your Anger**",
            "details": "💥 Physical activity can help release built-up anger. Try exercises or activities that allow you to let off steam.",
            "action": "🏃‍♂️ Engage in a workout, or try a stress-relief activity like hitting a punching bag."
        },
	"disgusting": {
            "text": "🤢 **Reflect on the Source**",
            "details": "🧐 Understand what triggers your feelings of disgust and consider why it affects you this way. It might help to address the source directly.",
            "action": "🔍 Examine the situation and explore ways to minimize or avoid the cause of disgust."
        },
	"joyful": {
            "text": "🎉 **Savor Your Joy**",
            "details": "😊 Celebrate moments of joy and share them with others. Engaging in activities that bring you pleasure can enhance this feeling.",
            "action": "🧁 Indulge in a favorite hobby or spend quality time with loved ones."
        },
	"surprised": {
            "text": "😲 **Embrace the Unexpected**",
            "details": "🎈 Surprise can be exciting! Take a moment to enjoy the unexpected and explore the new possibilities it presents.",
            "action": "🎁 Use this surprise as an opportunity to try something new or appreciate a different perspective."
        },
	"loved": {
            "text": "❤️ **Nurture Your Relationships**",
            "details": "🌹 Love is about connection. Spend time with loved ones and show appreciation for them. It's also important to practice self-love.",
            "action": "💌 Write a heartfelt note or plan a special activity for someone you care about."
        }
        # Add more moods as needed
    }
    return suggestions.get(mood, {
        "text": "🤔 **Unknown Mood**: We're not sure how to help with this mood.",
        "details": "Try providing a mood from the list to receive a more tailored suggestion."
    })

@app.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        mood = request.form.get("mood", "")
        suggestion = get_suggestions(mood)
        return render_template("index.html", suggestion=suggestion)
    return render_template("index.html", suggestion={"text": "", "details": ""})

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        if username and password and email:
            if username in users:
                flash("Username already exists. Please choose a different username.")
                return redirect(url_for('register'))
            else:
                users[username] = email
                user_passwords[username] = password
                user = User(username)
                login_user(user)
                return redirect(url_for('home'))
        else:
            flash("All fields are required.")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in user_passwords and user_passwords[username] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password.")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        # Generate and send password reset link (not implemented here)
        if email in users.values():
            token = str(random.randint(100000, 999999))
            password_reset_tokens[token] = email
            flash("Password reset link has been sent to your email.")
            # In a real application, you would send an email with the reset link
        else:
            flash("Email not found.")
    return render_template("forgot_password.html")

@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if token not in password_reset_tokens:
        flash("Invalid or expired token.")
        return redirect(url_for('forgot_password'))
    if request.method == "POST":
        new_password = request.form.get("password")
        email = password_reset_tokens.pop(token, None)
        username = next((u for u, e in users.items() if e == email), None)
        if username and new_password:
            user_passwords[username] = new_password
            flash("Password has been reset successfully. You can now log in.")
            return redirect(url_for('login'))
        else:
            flash("Password reset failed.")
    return render_template("reset_password.html")

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")

if __name__ == "__main__":
    app.run(debug=True)
