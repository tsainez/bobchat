# Bobchat

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

3. Install Python requirements::

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

## 📚 Requirements

- Python 3.9 or higher
- Sqlite 3.36.0 or higher

## 🔍 Troubleshooting

Some trouble we ran into on macOS BigSur: after running `brew upgrade sqlite` brew installed sqlite3 to `/usr/local/cellar/sqlite/3.36.0/bin/sqlite3`. You can either add this to the beginning of $PATH or move the brew installed sqlite3 file to `/usr/local/bin`.

If your database is not as expected, try running `flask init-db` to reset the database to it's factory default (with sample data inserted).

## 🧱 Resources For Developers

This project was made to satisfy the final project requirements in the [CSE 106](http://catalog.ucmerced.edu/preview_course_nopop.php?catoid=20&coid=48046&) (Exploratory Computing) and [CSE 111](https://catalog.ucmerced.edu/preview_course_nopop.php?catoid=20&coid=48047&) (Database Systems).

Want to make an application like this? Here's some useful resources:

- Knowing what [Patterns for Flask](https://flask.palletsprojects.com/en/2.0.x/patterns/) are available is useful figuring out how you want to use Flask and organize your project before you begin...
- The [sqlite3](https://docs.python.org/3/library/sqlite3.html) API documentation was immensely helpful for figuring out exactly how to create, use and manage a database using Python's built-in sqlite3 package.
- This [tutorial](https://flask.palletsprojects.com/en/2.0.x/tutorial/) from the Flask official documentation was a great starting point for our project and for learning how to use Flask.
