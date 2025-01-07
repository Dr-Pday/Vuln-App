from flask import Flask, request, render_template, session, redirect, flash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Helper functions
def is_logged_in():
    return 'user' in session

def is_admin():
    return is_logged_in() and session.get('role') == 'admin'

# Authentication routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':
            session['user'] = username
            session['role'] = 'admin'
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

# File Upload Vulnerabilities
@app.route('/upload/level1', methods=['GET', 'POST'])
def upload_level1():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            result_message = (
                f"File uploaded to {os.path.join(app.config['UPLOAD_FOLDER'], filename)}"
            )
            return render_template('upload/level1.html', solved=False, result=result_message)
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

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
