#pylint: disable=missing-module-docstring,invalid-name

from flask import Flask
from covinfo import main

app = Flask('__main__')

app.route('/')(main.get_daily_data)

if __name__ == '__main__':
    app.run('0.0.0.0', port='5000')
