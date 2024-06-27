import sqlite3
from flask import Flask, request, jsonify, g, render_template
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with a secure random key
login_manager = LoginManager(app)
login_manager.login_view = 'login'

DATABASE = 'finance.db'

# User Model for Login Management
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def modify_db(query, args=()):
    db = get_db()
    cur = db.execute(query, args)
    db.commit()
    cur.close()

@login_manager.user_loader
def load_user(user_id):
    user = query_db('SELECT * FROM user WHERE id = ?', [user_id], one=True)
    if user:
        return User(id=user['id'], username=user['username'], password=user['password'])
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400
    
    existing_user = query_db('SELECT * FROM user WHERE username = ?', [username], one=True)
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 400

    modify_db('INSERT INTO user (username, password) VALUES (?, ?)', [username, password])
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = query_db('SELECT * FROM user WHERE username = ? AND password = ?', [username, password], one=True)
    if user:
        user_obj = User(id=user['id'], username=user['username'], password=user['password'])
        login_user(user_obj)
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/user', methods=['GET'])
@login_required
def get_user():
    return jsonify({'username': current_user.username}), 200

@app.route('/transactions', methods=['GET'])
@login_required
def get_transactions():
    transactions = query_db('SELECT * FROM transaction WHERE user_id = ?', [current_user.id])
    return jsonify([{
        'id': transaction['id'],
        'date': transaction['date'],
        'description': transaction['description'],
        'amount': transaction['amount'],
        'type': transaction['type']
    } for transaction in transactions])

@app.route('/transactions', methods=['POST'])
@login_required
def create_transaction():
    data = request.get_json()
    date = data.get('date')
    description = data.get('description')
    amount = data.get('amount')
    type_ = data.get('type')

    modify_db('INSERT INTO transaction (user_id, date, description, amount, type) VALUES (?, ?, ?, ?, ?)',
              [current_user.id, date, description, amount, type_])
    return jsonify({'message': 'Transaction created successfully'}), 201

@app.route('/transactions/<int:id>', methods=['PUT'])
@login_required
def update_transaction(id):
    data = request.get_json()
    date = data.get('date')
    description = data.get('description')
    amount = data.get('amount')
    type_ = data.get('type')

    transaction = query_db('SELECT * FROM transaction WHERE id = ? AND user_id = ?', [id, current_user.id], one=True)
    if transaction:
        modify_db('UPDATE transaction SET date = ?, description = ?, amount = ?, type = ? WHERE id = ?',
                  [date, description, amount, type_, id])
        return jsonify({'message': 'Transaction updated successfully'}), 200
    else:
        return jsonify({'error': 'Transaction not found'}), 404

@app.route('/transactions/<int:id>', methods=['DELETE'])
@login_required
def delete_transaction(id):
    transaction = query_db('SELECT * FROM transaction WHERE id = ? AND user_id = ?', [id, current_user.id], one=True)
    if transaction:
        modify_db('DELETE FROM transaction WHERE id = ?', [id])
        return jsonify({'message': 'Transaction deleted successfully'}), 200
    else:
        return jsonify({'error': 'Transaction not found'}), 404

@app.route('/goals', methods=['GET'])
@login_required
def get_goals():
    goals = query_db('SELECT * FROM financial_goal WHERE user_id = ?', [current_user.id])
    return jsonify([{
        'id': goal['id'],
        'goal_name': goal['goal_name'],
        'target_amount': goal['target_amount'],
        'current_amount': goal['current_amount'],
        'target_date': goal['target_date']
    } for goal in goals])

@app.route('/goals', methods=['POST'])
@login_required
def create_goal():
    data = request.get_json()
    goal_name = data.get('goal_name')
    target_amount = data.get('target_amount')
    target_date = data.get('target_date')

    modify_db('INSERT INTO financial_goal (user_id, goal_name, target_amount, target_date) VALUES (?, ?, ?, ?)',
              [current_user.id, goal_name, target_amount, target_date])
    return jsonify({'message': 'Goal created successfully'}), 201

@app.route('/goals/<int:id>', methods=['PUT'])
@login_required
def update_goal(id):
    data = request.get_json()
    current_amount = data.get('current_amount')

    goal = query_db('SELECT * FROM financial_goal WHERE id = ? AND user_id = ?', [id, current_user.id], one=True)
    if goal:
        modify_db('UPDATE financial_goal SET current_amount = ? WHERE id = ?',
                  [current_amount, id])
        return jsonify({'message': 'Goal updated successfully'}), 200
    else:
        return jsonify({'error': 'Goal not found'}), 404

@app.route('/goals/<int:id>', methods=['DELETE'])
@login_required
def delete_goal(id):
    goal = query_db('SELECT * FROM financial_goal WHERE id = ? AND user_id = ?', [id, current_user.id], one=True)
    if goal:
        modify_db('DELETE FROM financial_goal WHERE id = ?', [id])
        return jsonify({'message': 'Goal deleted successfully'}), 200
    else:
        return jsonify({'error': 'Goal not found'}), 404

if __name__ == '__main__':
    with app.app_context():
        modify_db('''
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        modify_db('''
            CREATE TABLE IF NOT EXISTS transaction (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                description TEXT NOT NULL,
                amount REAL NOT NULL,
                type TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES user(id)
            )
        ''')
        modify_db('''
            CREATE TABLE IF NOT EXISTS financial_goal (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                goal_name TEXT NOT NULL,
                target_amount REAL NOT NULL,
                current_amount REAL NOT NULL DEFAULT 0,
                target_date TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES user(id)
            )
        ''')
    app.run(debug=True)
