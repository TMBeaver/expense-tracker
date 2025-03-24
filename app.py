from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from models import db, Expense, User
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a secure key
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'instance', 'expenses.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    expenses = Expense.query.filter_by(user_id=session['user_id']).all()
    return render_template('index.html', expenses=expenses)

#Regostering into the app

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Username already exists!", 400

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')


#Login in the app

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            return "Invalid username or password!", 401

    return render_template('login.html')

#Log out

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


#========ADD EXPENSE==============
@app.route('/add_expense', methods=['POST'])
def add_expense():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    name = request.form['name']
    category = request.form['category']
    amount = request.form['amount']
    date = request.form['date']

    new_expense = Expense(
        name=name,
        category=category,
        amount=float(amount),
        date=datetime.strptime(date, '%Y-%m-%d'),
        user_id=session['user_id']
    )

    db.session.add(new_expense)
    db.session.commit()
    return redirect(url_for('index'))

#========UPDATE EXPENSE==(after edit)============

#======== UPDATE EXPENSE ==============

@app.route('/update_expense', methods=['POST'])
def update_expense():
    expense_id = request.form['expense_id']
    name = request.form['name']
    category = request.form['category']
    amount = request.form['amount']
    date = request.form['date']

    expense = Expense.query.get(expense_id)
    if expense:
        expense.name = name
        expense.category = category
        expense.amount = float(amount)
        expense.date = datetime.strptime(date, '%Y-%m-%d')

        db.session.commit()
    
    return redirect(url_for('index'))


#========ADD EXPENSE==============

@app.route('/delete_expense/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    expense = Expense.query.get(expense_id)
    if expense and expense.user_id == session['user_id']:
        db.session.delete(expense)
        db.session.commit()
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Expense not found"}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
