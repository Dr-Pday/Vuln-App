
#Vulnerable Web Application 

This is a simple Flask-based web application designed as a testbed for practicing web security vulnerabilities such as XSS, file upload issues, and SQL injection.

Features

XSS (Cross-Site Scripting): Five levels of difficulty.
File Upload Vulnerabilities: Three levels of difficulty.
SQL Injection: Two levels of difficulty.
Prerequisites

Python 3.8 or higher
pip installed
Git installed
SQLite (for the default database)
Installation

Clone the repository:
git clone https://github.com/<your-username>/<your-repository>.git
cd <your-repository>
Create a virtual environment and activate it:
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\\Scripts\\activate
Install the required dependencies:
pip install -r requirements.txt
Initialize the database:
python
>>> from app import db
>>> db.create_all()
>>> exit()
Create the uploads directory:
mkdir static/uploads
Running the Application

Start the application:
python app.py
Open your browser and navigate to:
http://127.0.0.1:5000
Notes

This application is intentionally vulnerable. Do not deploy it to a production environment.
Use it only for educational purposes and in a controlled environment.
