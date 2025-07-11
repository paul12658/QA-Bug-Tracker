from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import csv
import io

app = Flask(__name__)
app.secret_key = 'a4900da6dca4422ca9a5082eb6eefbdb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bugs.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class Bug(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    tag = db.Column(db.String(50))
    status = db.Column(db.String(50), default='Open')
    reported_by = db.Column(db.String(80))

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    bugs = Bug.query.all()
    return render_template('index.html', bugs=bugs)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match")
            return render_template('register.html')

        # Check if username already exists
        if User.query.filter_by(username=username).first():
            flash("Username already exists")
            return render_template('register.html')

        # Hash and save user
        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, password_hash=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful. Please log in.")
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        tag = request.form['tag']
        reporter = session.get('user_id')
        user = User.query.get(reporter)
        new_bug = Bug(title=title, description=description, tag=tag, reported_by=user.username)
        db.session.add(new_bug)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('report.html')

@app.route('/export')
def export():
    bugs = Bug.query.all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Title', 'Description', 'Tag', 'Status', 'Reported By'])
    for bug in bugs:
        writer.writerow([bug.id, bug.title, bug.description, bug.tag, bug.status, bug.reported_by])
    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode()), mimetype='text/csv', as_attachment=True, download_name='bug_report.csv')

if __name__ == '__main__':
    # Ensure tables are created within app context
    with app.app_context():
        db.create_all()
    
    # Start the server
    app.run(debug= True)

