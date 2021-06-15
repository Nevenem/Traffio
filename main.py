# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import flask

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return '''
    Hello, World!
    <a href="/stajenevena">sta je nevena?</a>
    '''

@app.route('/stajenevena')
def stajenevena():
    return '<h1> zlato najvece </h1>'

@app.route('/stajewebserver')
def stajewebserver():
    return '<h1> program koji slusa na nekom portu i obradjuje zahteve </h1>'

# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/
