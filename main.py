from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'f9eujGjai8&gjk'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True)
    password = db.Column(db.String(25))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'list_blogs', 'index', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            return redirect('/newpost')
        if user and user.password != password:
            flash('Password is incorrect', 'error')
            return redirect('/login')
        else:
            flash('Username does not exist', 'error')
            return redirect('/login')

    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        if " " in username or len(username) < 3 or len(username) > 25:
            flash('Invalid username', 'error')
            return redirect('/signup')

        if " " in password or len(password) < 3 or len(password) > 25:
            flash('Invalid password', 'error')
            return redirect('/signup')

        if not username or not password or not verify:
            flash('One or more fields are invalid', 'error')
            return redirect('/signup')

        if password != verify:
            flash('Passwords do not match', 'error')
            return redirect('/signup')

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        else:
            flash('Username already exists', 'error')
            return redirect('/signup')

    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')


@app.route('/blog')
def list_blogs():
    blog_id = request.args.get('id')
    blogs = Blog.query.all()
    if blog_id:
        post = Blog.query.get(blog_id)
        blog_title = post.title
        blog_body = post.body
        return render_template('blogpost.html', title="Blog " + blog_id, blog_title = blog_title, blog_body = blog_body)
    else:
        return render_template('blog.html', title="Build A Blog", blogs = blogs)

@app.route('/newpost')
def new_post():
    return render_template('newpost.html', title="Add Blog Entry")

@app.route('/newpost', methods=['POST'])
def verify_post():

    owner = User.query.filter_by(username=session['username']).first()

    blog_title = request.form['title']
    blog_body = request.form['body']
    title_error = ''
    body_error = ''

    if blog_title == "":
        title_error = "Please fill in the title"
    if blog_body == "":
        body_error = "Please fill in the body"
    
    if not title_error and not body_error:
        new_blog = Blog(blog_title, blog_body, owner)
        db.session.add(new_blog)
        db.session.commit()
        blog = new_blog.id
        return redirect('/blog?id={0}'.format(blog))
    else:
        return render_template('newpost.html', title="Add Blog Entry", blog_title = blog_title, blog_body = blog_body, title_error = title_error, body_error = body_error)

if __name__ == '__main__':
    app.run()