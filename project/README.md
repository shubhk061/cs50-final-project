# MY PERSONAL AI AGENT — AI ChatNova

## Video Demo

[Watch My AI ChatNova Demo](https://youtu.be/HKyiLu1qtXs)

# Description

My Personal AI Agent, called AI ChatNova, is a web-based AI assistant that I created as my CS50 Final Project.
 AI ChatNova
 allows users to create an account, log in, ask questions to an AI assistant, and access their previous conversations. The application includes features such as registration, login, logout, conversation history, clear history, and password reset.

The application is designed to provide each user with a private account where their conversations are associated with their own user ID.

The application is built using Python and Flask for the backend and HTML and CSS for the frontend. SQLite and SQL are used to store user information and conversation history.

# How It Works

When a new user registers, their account information is stored in the SQLite database. The user's password is not stored as plain text. Instead, it is stored as a secure password hash.

After logging in, the user can type a question into the chat input box and submit it. The Flask application receives the question and sends it to the configured AI API. The API generates a response, which is then returned to the Flask application and displayed to the user.

One of the main features of AI ChatNova is conversation history. Each question and its corresponding AI-generated answer can be stored in the conversations table in the SQLite database. This allows users to access previous conversations even after leaving the chat page.

Each conversation is associated with a specific user through the user's database ID. Therefore, users can access their own conversation history through their account.



# Files and Folders

# app.py

app.py is the main Python file of the application. It creates and configures the Flask application and contains the routes that control the website.

These routes handle features such as:

* User registration
* Login
* Logout
* Password reset
* Asking questions to the AI
* Viewing conversation history
* Clearing conversation history

The file also handles the database connection and communication with the external AI API.

# init_db.py

init_db.py is used to initialize the SQLite database.

It creates the database tables required by the application, including the users and conversations tables.

# project.db

project.db is the SQLite database used by the application.

It stores information required by the application, including registered users and saved conversations.

# templates/

The templates directory contains the HTML files used by Flask to display the different pages of the application.

These templates include pages for:

* Login
* Registration
* AI chat
* Conversation history
* Password reset

# static/

The static directory contains the CSS used to style the application.

It controls the appearance, layout, spacing, buttons, forms, backgrounds, colors, and other visual elements of the website.


# Database Design

The application uses SQLite because it is lightweight, simple, and suitable for a small web application.

The database contains tables such as:

# users

The users table stores information about registered users. It also stores password hashes instead of plain-text passwords.

# conversations

The conversations table stores the questions asked by users and the corresponding AI-generated answers.

The table contains a user_id column that connects each conversation to the user who created it.

This relationship allows the application to display each user's own conversation history.


# Design Choices

# Flask

I chose Flask because it allowed me to use Python to build the backend while learning how web applications handle routes, forms, sessions, authentication, and databases.

Flask also made it easier to connect the application to the external AI API.

# SQLite

I chose SQLite because it is lightweight and easy to integrate with Flask.

It also allowed me to practice SQL and relational database concepts that I learned during CS50.

# Password Hashing

I used password hashing instead of storing plain-text passwords.

Storing passwords directly would be insecure because anyone with access to the database could potentially see the users' passwords.

The application stores password hashes instead and uses them to verify login attempts.

# Sessions

Flask sessions are used to keep track of the currently logged-in user.

This allows the application to know which user is making a request and which conversations belong to that user.

# Conversation History

I decided to save conversations in the database because an AI assistant is more useful when users can return to previous conversations.

The history feature allows users to view their previous questions and AI-generated answers.



# AI API

The application uses an external AI API to generate responses to user questions.

The API key is kept outside the source code using an environment variable instead of being directly written into the application.

This helps prevent the API key from being accidentally exposed when the source code is shared.

During development, I also used AI-based tools such as ChatGPT as a programming assistant. I used these tools to help me understand programming concepts, debug errors, and improve parts of my code.

The overall project idea, structure, design, and implementation were developed by me.



# Conclusion

This project allowed me to combine several concepts that I learned during CS50, including:

* Python
* Flask
* HTML
* CSS
* SQL
* SQLite
* Databases
* Authentication
* Sessions
* Password hashing
* APIs

Building AI ChatNova also gave me practical experience in connecting a web application to an external AI service and storing user data in a relational database.

The project represents my attempt to turn the concepts I learned throughout CS50 into a complete web application that I can continue improving after completing the course.
