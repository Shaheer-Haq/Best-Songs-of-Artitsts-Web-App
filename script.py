from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Load the CSV file containing the songs data
songs_data = pd.read_csv("songs.csv", encoding="latin1")

# Function to store fetched data to the database
def store_data_to_database(artist_name, user_properties):
    # Connect to the SQLite database
    conn = sqlite3.connect('music_data.db')
    cursor = conn.cursor()

    # Get the current time
    fetched_time = datetime.now()

    # Insert the fetched data into the database
    cursor.execute('''INSERT INTO fetched_data (artist_name, fetched_time, user_properties)
                      VALUES (?, ?, ?)''', (artist_name, fetched_time, user_properties))
    
    # Commit the transaction
    conn.commit()

    # Print the stored data to the terminal
    print("Data stored in the database:")
    print("Artist:", artist_name)
    print("Fetched Time:", fetched_time)
    print("User Properties:", user_properties)
    
    # Close the connection
    conn.close()

# Function to authenticate user
def authenticate_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM users WHERE username = ? AND password = ?''', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# Route for login
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = authenticate_user(username, password)
        if user:
            # Redirect to the index page or any other page after successful login
            return redirect(url_for('index'))
        else:
            return render_template('login.html', message="Invalid username or password.")
    return render_template("login.html")

# Route for signup
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        # Check if the username is already taken
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM users WHERE username = ?''', (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            conn.close()
            return render_template('signup.html', message="Username already exists.")
        else:
            cursor.execute('''INSERT INTO users (username, password) VALUES (?, ?)''', (username, password))
            conn.commit()
            conn.close()
            # Redirect to the login page after successful signup
            return redirect(url_for('login'))
    return render_template("signup.html")

# Route for index page
@app.route("/index", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        artist_name = request.form.get("artist")
        user_properties = request.form.get("user_properties")
        
        # Remove rows containing NaN values
        songs_data_cleaned = songs_data.dropna(subset=['Artist', 'Song-Name'])
        
        # Filter the cleaned songs data to find rows where the artist is found
        filtered_songs = songs_data_cleaned[songs_data_cleaned['Artist'].str.contains(artist_name, case=False)]
        
        # If there are multiple artists for a song, return only the first occurrence
        unique_filtered_songs = filtered_songs.drop_duplicates(subset=['Song-Name'], keep='first')
        
        # Sort the songs by rating and select the top 10
        top_10_songs = unique_filtered_songs.sort_values(by='Rating', ascending=False).head(10)
        
        # Store the fetched data to the database
        store_data_to_database(artist_name, user_properties)
        
        return render_template("result.html", songs=top_10_songs)
    
    return render_template("index.html")

if __name__ == "__main__":
    # Create the fetched_data table in the SQLite database if it doesn't exist
    conn = sqlite3.connect('music_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS fetched_data
                      (artist_name TEXT, fetched_time TIMESTAMP, user_properties TEXT)''')
    conn.close()
    
    # Create the users table in the SQLite database if it doesn't exist
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)''')
    conn.close()
    
    app.run(debug=True)
