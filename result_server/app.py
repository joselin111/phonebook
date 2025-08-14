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

# Ensure table exists
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
    return render_template('result_index.html', persons=persons)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

