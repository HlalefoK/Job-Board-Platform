# from flask import Flask, render_template, request, redirect, url_for, session
# from models import User, Transaction

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your_secret_key'

# @app.route('/')
# def home():
#     if 'user_id' in session:
#         return redirect(url_for('dashboard'))
#     else:
#         return redirect(url_for('onboarding'))


# @app.route('dashboard/')
# def dashboard():
#     # Replace with actual user handling logic
#     user_id = 1
#     transactions = Transaction.get_transactions(user_id)
#     return render_template('dashboard.html', transactions=transactions)

# @app.route('/onboarding', methods=['GET','POST'])
# def onboarding():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         financial_goals = request.form.get('financial-goal') or request.form.get('predefined-goals')
#         monthly_income = request.form.get('monthly-income')
#         income_frequency = request.form.get('income-frequency')
#         expense_categories = ','.join(request.form.getlist('expense-categories'))
#         financial_priorities = ','.join(request.form.getlist('financial-priorities'))

#         conn = get_db_connection()
#         conn.execute('INSERT INTO User (username, financial_goals, monthly_income, income_frequency, expense_categories, financial_priorities) VALUES (?, ?, ?, ?, ?, ?)',
#                      (username, financial_goals, monthly_income, income_frequency, expense_categories, financial_priorities))
#         conn.commit()
#         user_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
#         conn.close()

#         session['user_id'] = user_id
#         return redirect(url_for('dashboard'))
#     return render_template('onboarding.html')

# @app.route('/add-transaction', methods=['GET', 'POST'])
# def add_transaction():
#     if request.method == 'POST':
#         user_id = 1  # Replace with actual user handling logic
#         category = request.form['category']
#         description = request.form['description']
#         amount = float(request.form['amount'])
#         transaction_type = request.form['type']
#         date = request.form['date']

#         transaction = Transaction(user_id=user_id, category=category, description=description,
#                                   amount=amount, type=transaction_type, date=date)
#         transaction.save()

#         return redirect(url_for('dashboard'))

#     return render_template('add_transaction.html')

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

def get_db_connection():
    conn = sqlite3.connect('db/finance_tracker.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('onboarding'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('onboarding'))

    user_id = session['user_id']
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM User WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return render_template('dashboard.html', user=user)

@app.route('/onboarding', methods=['GET', 'POST'])
def onboarding():
    if request.method == 'POST':
        username = request.form.get('username')
        financial_goals = request.form.get('financial-goal') or request.form.get('predefined-goals')
        monthly_income = request.form.get('monthly-income')
        income_frequency = request.form.get('income-frequency')
        expense_categories = ','.join(request.form.getlist('expense-categories'))
        financial_priorities = ','.join(request.form.getlist('financial-priorities'))

        conn = get_db_connection()
        conn.execute('INSERT INTO User (username, financial_goals, monthly_income, income_frequency, expense_categories, financial_priorities) VALUES (?, ?, ?, ?, ?, ?)',
                     (username, financial_goals, monthly_income, income_frequency, expense_categories, financial_priorities))
        conn.commit()
        user_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        conn.close()

        session['user_id'] = user_id
        return redirect(url_for('dashboard'))
    return render_template('onboarding.html')

@app.route('/transactions')
def transactions():
    if 'user_id' not in session:
        return redirect(url_for('onboarding'))

    user_id = session['user_id']
    category = request.args.get('category')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    type_filter = request.args.get('type')
    page = request.args.get('page', 1, type=int)
    per_page = 10

    query = 'SELECT * FROM "Transaction" WHERE user_id = ?'
    params = [user_id]

    if category:
        query += ' AND category = ?'
        params.append(category)
    if start_date:
        query += ' AND date >= ?'
        params.append(start_date)
    if end_date:
        query += ' AND date <= ?'
        params.append(end_date)
    if type_filter:
        query += ' AND type = ?'
        params.append(type_filter)

    conn = get_db_connection()
    transactions = conn.execute(query, params).fetchall()
    conn.close()

    return render_template('transactions.html', transactions=transactions, page=page, per_page=per_page)

@app.route('/add-transaction', methods=['GET', 'POST'])
def add_transaction():
    if 'user_id' not in session:
        return redirect(url_for('onboarding'))

    if request.method == 'POST':
        user_id = session['user_id']
        date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        category = request.form['category']
        description = request.form['description']
        amount = float(request.form['amount'])
        type = request.form['type']

        conn = get_db_connection()
        conn.execute('INSERT INTO "Transaction" (user_id, date, category, description, amount, type) VALUES (?, ?, ?, ?, ?, ?)',
                     (user_id, date, category, description, amount, type))
        conn.commit()
        conn.close()

        return redirect(url_for('transactions'))

    return render_template('add_transaction.html')



if __name__ == '__main__':
    app.run(debug=True)
