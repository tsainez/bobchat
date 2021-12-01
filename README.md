# bobchat

Bobchat is a social media network for University of California, Merced students.
This was a project required as part of coursework for Database Systems (CSE 111), as well as Exploratory Computing (CSE 106).

## 📝 TODO:

- Load files in `./csv` into the appropriate database tables.
- Make this project [installable](https://flask.palletsprojects.com/en/2.0.x/tutorial/install/)
- Use Bootstrap for CSS
- Make the user's home page the main index page when logged in. (Going to have to change around the routing for `den.py`)
  - You can view what dens you are a part of, as well as the most recent popular posts from your followed dens and users
- Users should be allowed to update their account information as well as delete their account
- Relational database schema needs to be updated in several ways:
  - More fields for the `user` table
  - Flesh out relationships between users, dens and posts
- Users should be allowed to like posts, follow other users and join new dens

## 💥 Quickstart

To run this code:

1. Clone the repository::

   ```
   git clone https://github.com/tsainez/bobchat.git
   cd bobchat
   ```

2. **OPTIONAL**: Create and activate a virtual environment::

   ```
   virtualenv env
   source env/bin/activate
   ```

3. Install python requirements::

   ```
   pip install -r 'requirements.txt'
   ```

4. Run the application::

   ```
   export FLASK_APP=bobchat
   export FLASK_ENV=development
   flask init-db
   flask run
   ```

## 🔍 Troubleshooting

Some trouble we ran into on macOS BigSur: after running `brew upgrade sqlite` brew installed sqlite3 to `/usr/local/cellar/sqlite/3.36.0/bin/sqlite3`. You can either add this to the beginning of $PATH or move the brew installed sqlite3 file to `/usr/local/bin`

## 📚 Requirements

- Python 3.9 or higher
- Sqlite 3.36.0 or higher
