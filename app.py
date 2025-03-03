from flask import Flask, request, redirect, url_for, render_template
import sqlite3

app = Flask(__name__)

# Route for the form page
@app.route('/')
def form():
    return render_template('form.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        pickup_date = request.form['pickup-date']
        return_date = request.form['return-date']
        location = request.form['location']
        comments = request.form['comments']

        # Save data to database
        save_to_database(name, email, phone, pickup_date, return_date, location, comments)

        return redirect(url_for('success'))

# Route for success page
@app.route('/success')
def success():
    return "Thank you for your booking! We will contact you soon."

# Function to save data to database
def save_to_database(name, email, phone, pickup_date, return_date, location, comments):
    conn = sqlite3.connect('bookings.db')
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            pickup_date TEXT NOT NULL,
            return_date TEXT NOT NULL,
            location TEXT NOT NULL,
            comments TEXT
        )
    ''')

    # Insert data into table
    cursor.execute('''
        INSERT INTO bookings (name, email, phone, pickup_date, return_date, location, comments)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, email, phone, pickup_date, return_date, location, comments))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    app.run(debug=True)