from flask import Flask, render_template, request, redirect, url_for
from models import db, User, Transaction
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/finance_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/onboarding')
def onboarding():
    return render_template('onboarding.html')

@app.route('/submit-onboarding', methods=['POST'])
def submit_onboarding():
    username = "John Doe"  # Replace this with actual user handling logic
    financial_goals = request.form.get('financial-goal') or request.form.get('predefined-goals')
    monthly_income = request.form.get('monthly-income')
    income_frequency = request.form.get('income-frequency')
    expense_categories = ','.join(request.form.getlist('expense-categories'))
    financial_priorities = ','.join(request.form.getlist('financial-priorities'))

    user = User(username=username, financial_goals=financial_goals, monthly_income=monthly_income,
                income_frequency=income_frequency, expense_categories=expense_categories,
                financial_priorities=financial_priorities)
    
    db.session.add(user)
    db.session.commit()

    return redirect(url_for('dashboard'))

@app.route('/transactions')
def transactions():
    # Get filter parameters from query string
    category = request.args.get('category')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    type_filter = request.args.get('type')
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # Query the database with filters
    query = Transaction.query
    if category:
        query = query.filter_by(category=category)
    if start_date:
        query = query.filter(Transaction.date >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(Transaction.date <= datetime.strptime(end_date, '%Y-%m-%d'))
    if type_filter:
        query = query.filter_by(type=type_filter)

    transactions = query.paginate(page, per_page, False)

    return render_template('transactions.html', transactions=transactions)

@app.route('/add-transaction', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        category = request.form['category']
        description = request.form['description']
        amount = float(request.form['amount'])
        type = request.form['type']

        # Replace with actual user handling logic
        user_id = 1  
        
        transaction = Transaction(user_id=user_id, date=date, category=category, description=description,
                                  amount=amount, type=type)
        db.session.add(transaction)
        db.session.commit()

        return redirect(url_for('transactions'))

    return render_template('add_transaction.html')

if __name__ == '__main__':
    app.run(debug=True)
