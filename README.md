# bobchat

Social media network for University of California, Merced students.

Project required as part of coursework for Database Systems (CSE 111).

To run this repository:

1. Clone the repository::

   ```
   git clone https://github.com/tsainez/bobchat.git
   cd bobchat
   ```

2. Create and activate a virtual environment::

   ```
   virtualenv env
   source env/bin/activate
   ```

3. Install requirements::

   ```
   pip install -r 'requirements.txt'
   ```

4. Run the application::

   ```
   python app.py
   ```

The first time you run this example, a sample sqlite database gets populated automatically. To suppress this behaviour,
comment the following lines in app.py:::

```
if not os.path.exists(database_path):
   build_sample_db()
```

notes from nate:

to populate the database with the csv file given.csv run

```
sqlite3 example.sqlite < populate.sql
```

sqlite 3.33.0 is the minimum requirement. Some trouble I ran into on macOS BigSur: after running `brew upgrade sqlite` brew installed sqlite3 to `/usr/local/cellar/sqlite/3.36.0/bin/sqlite3`. you can either add this to the beginning of $PATH or move the brew installed sqlite3 file to `/usr/local/bin`
