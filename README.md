# Personal Finance Tracker

A personal finance tracker web application built with Flask, SQLite, and HTML/CSS. This application helps users to track their income, expenses, financial goals, and budgets.

## Project Structure


Sure, let's create a README file for your Personal Finance Tracker project.

README.md
markdown
Copy code
# Personal Finance Tracker

A personal finance tracker web application built with Flask, SQLite, and HTML/CSS. This application helps users to track their income, expenses, financial goals, and budgets.

## Project Structure

finance_tracker/
├── app.py
├── init_db.py
├── models.py
├── static/
│ ├── styles.css
│ └── script.js
├── templates/
│ ├── dashboard.html
│ ├── onboarding.html
│ ├── transactions.html
│ └── add_transaction.html
└── db/


## Features

- **User Onboarding**: Collect user financial goals, income information, expense categories, and financial priorities.
- **Dashboard**: Display an overview of income vs. expenses, net worth, and quick links to common actions.
- **Add Transaction**: Form to add new transactions with date, category, description, amount, and type (income/expense).
- **Transaction List**: Display and filter transactions with pagination support.
