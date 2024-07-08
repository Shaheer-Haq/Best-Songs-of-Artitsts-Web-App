# Best-Songs-of-Artitsts-Web-App

## Overview

The Music Data Application is a Flask-based web application designed to fetch and display top songs data based on user input. It allows users to log in, search for artists, fetch top-rated songs, and store user interactions in a database.

## Features

- **User Authentication:**
  - Users can log in with existing credentials or sign up for new accounts.
  
- **Song Data Fetching:**
  - Users can enter an artist's name to fetch top-rated songs data.
  
- **Data Storage:**
  - Fetched data including artist name, fetch time, and user properties are stored in SQLite databases (`music_data.db` for fetched data and `users.db` for user authentication).

## Project Structure

The project is structured as follows:

- `app.py`: Main Flask application file.
- `templates/`: Directory containing HTML templates.
- `static/`: Directory for static files (CSS, JS, etc.).
- `songs.csv`: CSV file containing songs data used for fetching.

## Dependencies

The application requires Python and the following Python packages:

- Flask
- pandas
- sqlite3

Dependencies are listed in `requirements.txt`.

## Installation and Setup

### Prerequisites

Ensure you have Python installed. If not, download and install it from [Python's official website](https://www.python.org/).

### Installation Steps

1. Clone the repository:
  git clone <repository-url>

2. Navigate into the project directory:
  cd <project-directory>

3. Install dependencies:
  pip install -r requirements.txt

## Usage

### Running the Application

1. Run the Flask application:
  python app.py

2. Open a web browser and go to `http://localhost:5000` to access the login/signup page.

### Functionality

- **Login:** Allows existing users to authenticate.
- **Signup:** Enables new users to create an account.
- **Index Page:** Search for an artist, fetch top songs, and store user interactions.

## Database Schema

### `music_data.db`

- **Table: `fetched_data`**
- `artist_name` TEXT
- `fetched_time` TIMESTAMP
- `user_properties` TEXT

### `users.db`

- **Table: `users`**
- `id` INTEGER PRIMARY KEY AUTOINCREMENT
- `username` TEXT UNIQUE
- `password` TEXT


## Authors

- Shaheer-E-Haq

## Notes

-Adjustments may be needed for different input formats or additional features.

Feel free to contact for any questions or suggestions!
