from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blogs@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    
    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/blog', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']

        title_error = ''
        body_error = ''

        if blog_title == "":
            title_error = "Oops"

        if blog_body == "":
            body_error = "Yikes"

        if not title_error and not body_error:    

            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()

            blogs = Blog.query.all()

            return render_template('blog.html', title="Build A Blog", blogs = blogs)

        else:
            return render_template('newpost.html', title="Add Blog Entry", title_error=title_error, body_error=body_error)

    else:
        blogs = Blog.query.all()
        return render_template('blog.html', title="Build A Blog", blogs = blogs)

@app.route('/newpost')
def new_post():
    return render_template('newpost.html', title="Add Blog Entry")

if __name__ == '__main__':
    app.run()