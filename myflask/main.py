from flask import Flask

app = Flask(__name__)


# @app.route('/')
# def hello_world():
#     return 'hello world...'

@app.route('/')
def index():
    return 'index...'


@app.route('/world')
def hello_world():
    return 'hello world...'


@app.route('/<post_id>')
def myfun1(post_id):
    return f"hello post_id+2 is : {post_id}"
