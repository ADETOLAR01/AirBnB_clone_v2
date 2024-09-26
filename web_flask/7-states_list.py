#!/usr/bin/python3
"""A simple Flask web application to list states from storage"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)

# Route to display list of states
@app.route('/states_list', strict_slashes=False)
def states_list():
    """Displays a list of states sorted by name"""
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda state: state.name)
    return render_template('states_list.html', states=sorted_states)

# Method to remove SQLAlchemy session after each request
@app.teardown_appcontext
def teardown_db(exception):
    """Closes the storage on teardown"""
    storage.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
