from flask import Flask, request, render_template, redirect, url_for
from flaskext.mysql import MySQL
import os
import time

app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_DATABASE_HOST'] = os.getenv('DB_HOST')
app.config['MYSQL_DATABASE_USER'] = os.getenv('DB_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('DB_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = os.getenv('DB_NAME')

mysql = MySQL()
mysql.init_app(app)

# Wait for DB to be ready
while True:
    try:
        conn = mysql.connect()
        conn.autocommit(True)
        cursor = conn.cursor()
        break
    except:
        print("Waiting for MySQL...")
        time.sleep(2)

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS phonebook (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    number VARCHAR(100) NOT NULL
) ENGINE=InnoDB;
""")

# Routes
@app.route('/', methods=['GET'])
def index():
    cursor.execute("SELECT * FROM phonebook")
    persons = [{'id': r[0], 'name': r[1], 'number': r[2]} for r in cursor.fetchall()]
    return render_template('index.html', persons=persons)

@app.route('/add', methods=['POST'])
def add_person():
    name = request.form['name'].strip()
    number = request.form['number'].strip()
    cursor.execute("INSERT INTO phonebook (name, number) VALUES (%s, %s)", (name, number))
    return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update_person():
    person_id = request.form['id']
    name = request.form['name'].strip()
    number = request.form['number'].strip()
    cursor.execute("UPDATE phonebook SET name=%s, number=%s WHERE id=%s", (name, number, person_id))
    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete_person():
    person_id = request.form['id']
    cursor.execute("DELETE FROM phonebook WHERE id=%s", (person_id,))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

