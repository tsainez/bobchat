#
#   wsgi.py
#       This file allows us to simply run 'flask run' to start the app
#       instead of having to declare a new environment variables 
#       for the app every time. 
#       
#       You do still have to run 'export FLASK_ENV=development' though
#       in order to get the debug and reloader.
#

from bobchat import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
