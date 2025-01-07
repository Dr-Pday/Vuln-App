from flask import Flask, request, render_template, session, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
import re

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='user')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

# Create database if not exists
db.create_all()

# Helper functions
def is_logged_in():
    return 'user' in session

def is_admin():
    return is_logged_in() and session.get('role') == 'admin'

# Authentication routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user'] = user.username
            session['role'] = user.role
            flash('Logged in successfully!', 'success')
            return redirect('/dashboard')
        flash('Invalid credentials.', 'danger')
    return render_template('login.html', action="Login")

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect('/login')

@app.route('/dashboard')
def dashboard():
    if not is_logged_in():
        flash('Please log in first.', 'warning')
        return redirect('/login')
    return render_template('dashboard.html', user=session['user'], role=session['role'])

# Vulnerabilities implementation
## XSS Vulnerabilities
@app.route('/xss/level1', methods=['GET', 'POST'])
def xss_level1():
    if request.method == 'POST':
        comment = request.form['comment']
        return render_template('xss/level1.html', comment=comment, solved=False)
    return render_template('xss/level1.html', comment=None, solved=False)

@app.route('/xss/level2', methods=['GET', 'POST'])
def xss_level2():
    if request.method == 'POST':
        content = request.form['comment']
        if '<script>' in content or '</script>' in content:
            return render_template('xss/level2.html', comments=None, solved=False)
        new_comment = Comment(content=content)
        db.session.add(new_comment)
        db.session.commit()
        comments = Comment.query.all()
        return render_template('xss/level2.html', comments=comments, solved=True)
    comments = Comment.query.all()
    return render_template('xss/level2.html', comments=comments, solved=False)

@app.route('/xss/level3', methods=['GET', 'POST'])
def xss_level3():
    if request.method == 'POST':
        comment = request.form['comment']
        sanitized_comment = re.sub(r'<.*?>', '', comment)
        return render_template('xss/level3.html', comment=sanitized_comment, solved=True)
    return render_template('xss/level3.html', comment=None, solved=False)

@app.route('/xss/level4', methods=['GET', 'POST'])
def xss_level4():
    if request.method == 'POST':
        comment = request.form['comment']
        sanitized_comment = re.sub(r'<.*?>', '', comment)
        return render_template('xss/level4.html', comment=sanitized_comment, solved=True)
    return render_template('xss/level4.html', comment=None, solved=False)

@app.route('/xss/level5', methods=['GET', 'POST'])
def xss_level5():
    csp = "default-src 'self'; script-src 'self';"
    response = app.make_response(render_template('xss/level5.html', solved=True))
    response.headers['Content-Security-Policy'] = csp
    return response

## File Upload Vulnerabilities
@app.route('/upload/level1', methods=['GET', 'POST'])
def upload_level1():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('upload/level1.html', solved=False, result=f"File uploaded to {os.path.join(app.config['UPLOAD_FOLDER'], filename)}")
    return render_template('upload/level1.html', solved=False, result=None)

@app.route('/upload/level2', methods=['GET', 'POST'])
def upload_level2():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            if not filename.endswith(('.jpg', '.png', '.gif')):
                flash('Only image files are allowed.', 'danger')
                return render_template('upload/level2.html', solved=False)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('upload/level2.html', solved=True, result=f"File uploaded: {filename}")
    return render_template('upload/level2.html', solved=False, result=None)

@app.route('/upload/level3', methods=['GET', 'POST'])
def upload_level3():
    return render_template('upload/level3.html')

## SQL Injection Vulnerabilities
@app.route('/sql/level1', methods=['GET', 'POST'])
def sql_level1():
    if request.method == 'POST':
        username = request.form['username']
        query = f"SELECT * FROM user WHERE username = '{username}'"
        try:
            result = db.session.execute(query).fetchall()
            if not result:
                return render_template('sql/level1.html', solved=False, result="No users found")
            return render_template('sql/level1.html', solved=True, result=result)
        except Exception as e:
            return render_template('sql/level1.html', solved=False, result=f"Error: {str(e)}")
    return render_template('sql/level1.html', solved=False, result=None)

@app.route('/sql/level2', methods=['GET', 'POST'])
def sql_level2():
    return render_template('sql/level2.html')

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
