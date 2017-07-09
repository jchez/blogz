from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    
    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/blog', methods=['POST', 'GET'])
def index():
    return render_template('blog.html', title="Build A Blog")

@app.route('/newpost')
def new_post():
    return render_template('newpost.html', title="Add Blog Entry")

if __name__ == '__main__':
    app.run()