# MAVERICKS_TECHATHON_2024
Mental stress relief chatbot
# Flask Mood Tracker Application

## Overview

The Flask Mood Tracker is a web application built with Flask that allows users to track their mood and receive personalized suggestions based on their emotional state. The app also includes user authentication features such as registration, login, password reset, and profile management.

## Features

- **Mood Suggestions**: Get personalized suggestions based on your current mood.
- **User Authentication**: Register, log in, and manage user sessions.
- **Password Reset**: Request a password reset via email.
- **Profile Management**: View your profile (coming soon).

## Technologies Used

- Python 3.x
- Flask
- Flask-Login

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/flask-mood-tracker.git
   cd flask-mood-tracker
2.**Set Up a Virtual Environment**
  python -m venv myenv
  
3.**Activate the Virtual Environment**
  venv\Scripts\activate
  
4.**Inatall flask**
  pip install flask
  
5.**Running the application**
  >Start the Flask Development Server
    python app.py
  >Access the Application
    Open your web browser and navigate to:
      http://127.0.0.1:5000


**Usage**
>Home Page: Submit your mood to receive tailored suggestions.
>Register: Create a new user account.
>Login: Access your account with your username and password.
>Forgot Password: Request a password reset link via email.
>Reset Password: Use the token sent to your email to reset your password.
>Profile: View and manage your user profile (coming soon).
**Templates**
>index.html: Displays mood suggestions.
>register.html: User registration form.
>login.html: User login form.
>forgot_password.html: Form for requesting a password reset.
>reset_password.html: Form for resetting the password.
>profile.html: User profile page (currently not implemented).

