# Bobchat

Bobchat is a social media network for University of California, Merced students.

## 💥 Quickstart

To run this code:

1. Clone the repository::

   ```
   git clone https://github.com/tsainez/bobchat.git
   cd bobchat
   ```

2. Create and activate a virtual environment::

   ```
   python3 -m venv venv
   . venv/bin/activate
   ```

3. Install Bobchat::

   ```
   pip install -e .
   ```

   This installs Bobchat as a Python package as well as all the dependencies needed.

4. Run the application::

   1. Initialize the database:

      ```
      flask init-db
      ```

   2. Run the application:

      ```
      gunicorn "bobchat:create_app()"
      ```

      Alternatively, to run in development mode using the Werkzeug WSGI:

      ```
      export FLASK_ENV=development
      flask run
      ```

5. View the Application::

   Navigate to `localhost:5000` or `127.0.0.1:5000` in a browser.

## 📚 Requirements

- Python 3.9 or higher
- Sqlite 3.36.0 or higher

## 🔍 Troubleshooting

Some trouble we ran into on macOS BigSur: after running `brew upgrade sqlite` brew installed sqlite3 to `/usr/local/cellar/sqlite/3.36.0/bin/sqlite3`. You can either add this to the beginning of $PATH or move the brew installed sqlite3 file to `/usr/local/bin`.

If your database is not as expected, try running `flask init-db` to reset the database to it's factory default (with sample data inserted).

## 🧱 Resources For Developers

This project was made to satisfy the final project requirements in the [CSE 106](http://catalog.ucmerced.edu/preview_course_nopop.php?catoid=20&coid=48046&) (Exploratory Computing) and [CSE 111](https://catalog.ucmerced.edu/preview_course_nopop.php?catoid=20&coid=48047&) (Database Systems).

Want to make an application like this? Here's some useful resources:

- This [tutorial](https://flask.palletsprojects.com/en/2.0.x/tutorial/) from the Flask official documentation was a great starting point for our project and for learning how to use Flask.
- Knowing what [Patterns for Flask](https://flask.palletsprojects.com/en/2.0.x/patterns/) are available is useful figuring out how you want to use Flask and organize your project before you begin...
- The [sqlite3](https://docs.python.org/3/library/sqlite3.html) API documentation was immensely helpful for figuring out exactly how to create, use and manage a database using Python's built-in sqlite3 package.
