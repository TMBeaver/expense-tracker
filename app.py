from flask import Flask, render_template
from models import db, Expense  # Import your database and model

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    expenses = Expense.query.all()  # Get all expenses from DB
    return render_template('index.html', expenses=expenses)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure DB tables exist
    app.run(debug=True)