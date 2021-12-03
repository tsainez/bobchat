# bobchat

Bobchat is a social media network for University of California, Merced students.

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
