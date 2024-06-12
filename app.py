from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# Database (replace with your preferred database implementation)
customers = [
    {'id': 1, 'name': 'Mohit', 'total_spends': 12000, 'last_visit': '2024-03-15'},
    {'id': 2, 'name': 'Anjali', 'total_spends': 18000, 'last_visit': '2024-06-10'},
    {'id': 3, 'name': 'Rishi', 'total_spends': 15000, 'last_visit': '2024-05-01'},
    # ... add more customer data
]

# Simple authentication (replace with a more secure method)
users = {'admin': 'password'}

@app.route('/')
def login():
    if 'username' in session:
        return redirect(url_for('create_audience'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username'] 
    password = request.form['password']
    if username in users and users[username] == password:
        session['username'] = username
        return redirect(url_for('create_audience'))
    return 'Invalid credentials'

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/create_audience', methods=['GET', 'POST'])
def create_audience():
    if 'username' not in session:
        return redirect(url_for('login'))

    rules = []
    audience_size = 0

    if request.method == 'POST':
        field = request.form['field']
        operator = request.form['operator']
        value = request.form['value']
        rules.append((field, operator, value))

        # Simulate audience size calculation based on rules
        audience_size = len(customers)  

        # Fetch all customer records from the database
        customer_records = customers  

        return render_template('create_audience.html', rules=rules, audience_size=audience_size, customer_records=customer_records)

    return render_template('create_audience.html', rules=rules, audience_size=audience_size)

@app.route('/add_customer_form')
def add_customer_form():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    return render_template('add_customer.html')

@app.route('/add_customer', methods=['POST'])
def add_customer():
    if 'username' not in session:
        return redirect(url_for('login'))

    name = request.form['name']
    total_spends = int(request.form['total_spends'])
    last_visit = request.form['last_visit']

    # Generate unique customer ID (replace with proper ID generation logic)
    customer_id = len(customers) + 1

    new_customer = {'id': customer_id, 'name': name, 'total_spends': total_spends, 'last_visit': last_visit}
    customers.append(new_customer)

    return redirect(url_for('create_audience'))

@app.route('/send_campaign', methods=['POST'])
def send_campaign():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Retrieve audience from session (or database for persistence)
    audience = []  # Placeholder for retrieving audience from session or database

    # Simulate sending campaign to dummy vendor API
    communication_logs = []
    for customer in audience:
        status = 'SENT' if random.random() > 0.1 else 'FAILED'  # 90% SENT, 10% FAILED
        communication_logs.append({'customer_id': customer['id'], 'status': status})

        # Simulate delivery receipt API (replace with actual API calls if needed)
        update_delivery_status(communication_logs[-1]['id'], status)

    return render_template('campaign_sent.html', communication_logs=communication_logs)

def update_delivery_status(communication_log_id, status):
    # Replace with actual database update or API call logic
    print(f'Communication log {communication_log_id} updated to status: {status}')

if __name__ == '__main__':
    app.run(debug=True)
