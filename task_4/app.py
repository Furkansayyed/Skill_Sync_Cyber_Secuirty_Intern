from flask import Flask, request, render_template, redirect, session
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'secret_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # handle request
        errors = []
        username = request.form['name']
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if not user:
            new_user = User(username=username,email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/login')
        
        else:
            errors.append('Email already exists')
            return render_template('register.html', errors=errors)

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if session['username']:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('dashboard.html', user=user)
    
    return redirect('/login')
  
if __name__ == '__main__':
    app.run(debug=True)
