import os
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

APP_TITLE = os.getenv("APP_TITLE", "Expense Tracker")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@expensetracker.com")

expenses = []

@app.route('/')
def home():
    return render_template(
        'index.html',
        expenses=expenses,
        app_title=APP_TITLE,
        admin_email=ADMIN_EMAIL
    )

@app.route('/add', methods=['POST'])
def add_expense():
    
    title = request.form['title']
    amount = request.form['amount']
    category = request.form['category']

    expenses.append({
        'title': title,
        'amount': amount,
        'category': category
    })

    return redirect('/')

@app.route('/delete/<int:index>')
def delete_expense(index):
    if 0 <= index < len(expenses):
        expenses.pop(index)

    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

