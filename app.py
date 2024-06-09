from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector
import json, datetime

app = Flask(__name__)

# Load database configuration from config.json
with open('config.json', 'r') as config_file:
    db_config = json.load(config_file)
@app.route('/budget')
def budget():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Execute query
    cursor.execute("SELECT name FROM account order by name")
    accounts = cursor.fetchall()

    # Close connection
    cursor.close()
    conn.close()

    return render_template('budget.html', accounts=accounts)

@app.route('/')
def finapp():
    return render_template('finapp.html')

@app.route('/create_budget', methods=['POST'])
def create_budget():
    selected_month = request.form.get('month')  # Get the selected month from the form
    selected_accounts = request.form.getlist('selected_accounts[]')  # Get the selected accounts from the form
    # Now you can do whatever you want with the selected month and accounts
    # For example, you can insert them into a MySQL table

    # Print the selected month and accounts for demonstration
    print("Selected Month:", selected_month)
    print("Selected Accounts:", selected_accounts)

    # Add your database insertion logic here
    data_to_insert = [(selected_month, account) for account in selected_accounts]

    # Insert data into the budget table
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    print("creating new budget")
    print(data_to_insert)

    cursor.executemany("INSERT INTO budget (month, name,status) VALUES (%s, %s, 'new')", data_to_insert)

    conn.commit()
    cursor.close()
    conn.close()


    return "Budget created successfully!"

@app.route('/show_budget')
def show_budget():
    selected_month = request.args.get('selected_month')
    if selected_month == None or selected_month == "Select" :
        print("default selection")
        current_date = datetime.datetime.now()
        selected_month = current_date.strftime("%B")
    print("---showing budget for -"+selected_month+"----")
    # Connect to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Execute query
    cursor.execute("SELECT month,name,estimated_amount from budget where month = '"+selected_month+"' and status = 'new'")
    accounts = cursor.fetchall()
    print(accounts)
    # Close connection
    cursor.close()
    conn.close()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify(accounts)
    else:
        return render_template('update_budget.html', budget=accounts)
    

#TODO working on below code.
@app.route('/update_budget', methods=['POST','GET'])
def update_budget():
    updated_budget = request.form.to_dict(flat=False)
    print(updated_budget)
    # Update the database with the new values
    try:
        # Insert data into the budget table
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        values = []
        selected_month = ""
        for i in range(len(updated_budget['month[]'])):
            selected_month = updated_budget['month[]'][i]
            month = updated_budget['month[]'][i]
            name = updated_budget['name[]'][i]
            estimated_amount = float(updated_budget['estimated_amount[]'][i])  # Assuming it's a float
            values.append((month, name, estimated_amount))
        print("updating previous budget for ")
        print(selected_month)
        current_date = datetime.datetime.now()
        uniq = current_date.strftime("%m%d%H%M%S")


        cursor.execute("update budget set status = 'updated on "+uniq+"' where month = '"+ selected_month +"' and status = 'new'")
        print("inserting new budget for "+ selected_month)
        cursor.executemany("INSERT INTO budget (month, name, estimated_amount, status) VALUES (%s, %s, %s, 'new')", values)

        conn.commit()
        cursor.close()
        conn.close()
        print("Updated successfully")
        return 'Budget updated successfully!'
    except Exception as e:
        # Generic catch-all block for any other exception
        print("An unexpected error occurred:", e)

@app.route('/accounts')
def show_accounts():
    # Connect to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Execute query
    cursor.execute("SELECT name FROM account order by name")
    accounts = cursor.fetchall()

    # Close connection
    cursor.close()
    conn.close()

    if request.headers.get('X-Requested-With') == 'Fetch':
        print("Fetch Request for accounts")
        return jsonify(accounts)
    else:
        print("rendering for accounts")
        return render_template('accounts.html', accounts=accounts)


@app.route('/transaction')
def transaction():
    today_date = datetime.date.today().strftime('%Y-%m-%d')
    return render_template('transaction.html',today_date=today_date)

@app.route('/add_account', methods=['POST'])
def add_account():
    name = request.form['name']
    
    # Connect to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Execute insert query
    cursor.execute("INSERT INTO account (name) VALUES (%s)", (name,))
    conn.commit()

    # Close connection
    cursor.close()
    conn.close()

    return redirect(url_for('show_accounts'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
