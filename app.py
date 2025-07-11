# Import necessary Flask modules and libraries
from flask import Flask, render_template, request, redirect, url_for, session, send_file
from flask_sqlalchemy import SQLAlchemy
from flask import flash
from werkzeug.security import generate_password_hash, check_password_hash
import csv
import io
import os

# Initialize Flask app
app = Flask(__name__)

# Set a secret key for session handling (uses environment variable or fallback key)
app.secret_key = os.getenv('SECRET_KEY', 'fallback_dev_key')

# Configure SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bugs.db'

# Initialize SQLAlchemy with the Flask app
db = SQLAlchemy(app)

# Define User model/table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique user ID
    username = db.Column(db.String(80), unique=True, nullable=False)  # Username must be unique
    password_hash = db.Column(db.String(128), nullable=False)  # Hashed password

# Define Bug model/table
class Bug(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique bug ID
    title = db.Column(db.String(200), nullable=False)  # Short bug title
    description = db.Column(db.Text, nullable=False)  # Detailed description
    tag = db.Column(db.String(50))  # Optional tag (e.g., UI, Backend)
    status = db.Column(db.String(50), default='Open')  # Bug status
    reported_by = db.Column(db.String(80))  # Username of the reporter

# Homepage route (dashboard)
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not authenticated
    bugs = Bug.query.all()  # Fetch all bugs from the database
    return render_template('index.html', bugs=bugs)  # Display dashboard

# User registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']
        # Hash the password
        hashed_pw = generate_password_hash(password)
        # Create and save new user
        new_user = User(username=username, password_hash=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))  # Redirect to login after registration
    return render_template('register.html')  # Show registration form

# Logout route
@app.route('/logout')
def logout():
    # Clear user session
    session.clear()
    return redirect(url_for('login'))  # Redirect to login page


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Extract submitted credentials
        username = request.form['username']
        password = request.form['password']

        # Retrieve user from the database
        user = User.query.filter_by(username=username).first()

        # Authenticate user
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id  # Store user ID in session
            return redirect(url_for('index'))  # Redirect to dashboard
        else:
            flash('Invalid username or password')  # Feedback for authentication failure

    return render_template('login.html')  # Render login form on GET or failed login


# Bug reporting route
@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        # Collect bug report data from form
        title = request.form['title']
        description = request.form['description']
        tag = request.form['tag']
        reporter = session.get('user_id')
        user = User.query.get(reporter)
        # Create and save new bug report
        new_bug = Bug(title=title, description=description, tag=tag, reported_by=user.username)
        db.session.add(new_bug)
        db.session.commit()
        return redirect(url_for('index'))  # Redirect to dashboard
    return render_template('report.html')  # Show bug report form

# Export bugs as CSV
@app.route('/export')
def export():
    bugs = Bug.query.all()  # Fetch all bugs
    output = io.StringIO()
    writer = csv.writer(output)
    # Write CSV header
    writer.writerow(['ID', 'Title', 'Description', 'Tag', 'Status', 'Reported By'])
    # Write each bug as a row
    for bug in bugs:
        writer.writerow([bug.id, bug.title, bug.description, bug.tag, bug.status, bug.reported_by])
    output.seek(0)
    # Send the CSV as a downloadable file
    return send_file(io.BytesIO(output.getvalue().encode()), mimetype='text/csv', as_attachment=True, download_name='bug_report.csv')

# Main entry point
if __name__ == '__main__':
    # Create database tables within the Flask app context
    with app.app_context():
        db.create_all()
    
    # Start Flask development server
    app.run(debug=True)
# Note: This code is intended for test purposes and may require additional security measures for production use.