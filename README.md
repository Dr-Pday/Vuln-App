# Vulnerable Web Application Testbed

This repository contains a Flask-based web application designed as a testbed for practicing and understanding web vulnerabilities, such as XSS, file upload issues, and SQL injection.

## Features

- **XSS (Cross-Site Scripting)**: Five levels with increasing difficulty.
- **File Upload Vulnerabilities**: Three levels with stricter restrictions.
- **SQL Injection**: Two levels demonstrating insecure and secure database querying.

## Prerequisites

Ensure you have the following installed before proceeding:

1. Python 3.8 or higher
2. [pip](https://pip.pypa.io/en/stable/installation/)
3. Git
4. SQLite (for database)

## Installation and Setup

Follow these steps to set up the application on your local machine:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Dr-pday/Vuln-App.git
   cd Vuln-App
   
2. **Create a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # For Windows: venv\Scripts\activate
   
3. **Install Dependencies:**:
   ```bash
   pip install -r requirements.txt
   
      Then run the following commands:
   
     ```bash
      from app import db
      db.create_all()
      exit()

4. **Initialize the Database:**:
   Open Python in your terminal:
   ```bash
   python3

5. **Create the Uploads Directory:**:
   ```bash
   mkdir static/uploads

   
## Running the Application

1. **Start the Application** 
 ```bash
python3 app.py





