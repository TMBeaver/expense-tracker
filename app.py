from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, Expense
from datetime import datetime
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'instance', 'expenses.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    expenses = Expense.query.all()
    return render_template('index.html', expenses=expenses)

#   ==================ADD  expense function of sqlalchemy==============
@app.route('/add_expense', methods=['POST'])

def add_expense():
    name = request.form['name']
    category = request.form['category']
    amount = request.form['amount']
    date = request.form['date']
    
    new_expense = Expense(
        name=name,
        category=category,
        amount=float(amount),
        date=datetime.strptime(date, '%Y-%m-%d')
            
    )

    db.session.add(new_expense)
    db.session.commit()
    return redirect(url_for('index'))

#==================== EDIT function in table=========================
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

#   ==================Delete function of sqlalchemy==============
@app.route('/delete_expense/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    expense = Expense.query.get(expense_id)
    if expense:
        db.session.delete(expense)
        db.session.commit()
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Expense not found"}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
